from fabric.api import sudo, cd, path, shell_env
from fabric.operations import reboot
from fabric.contrib.files import exists, append
import sys

"""
References
--

http://caffe.berkeleyvision.org/install_apt.html
https://github.com/BVLC/caffe/wiki/Ubuntu-14.04-VirtualBox-VM
"""

PREFIX = "/opt/caffe"


def _add_bashrc(path):
    with open("/etc/bash.bashrc", "a") as fp:
        fp.write("export PATH={0}:$PATH\n".format(path))


def _install_depends():
    sudo("apt-get update")
    sudo("apt-get upgrade -y")
    sudo("apt-get install -y linux-generic")
    reboot()

    sudo("apt-get install -y linux-headers-`uname -r`")

    sudo("apt-get install -y build-essential")
    sudo("apt-get install -y git")
    sudo("apt-get install -y wget")
    sudo("apt-get install -y libjpeg-dev libblas-dev libatlas-dev libatlas-base-dev liblapack-dev gfortran")
    sudo("apt-get install -y libprotobuf-dev libleveldb-dev libsnappy-dev libopencv-dev libboost-all-dev")
    sudo("apt-get install -y libhdf5-serial-dev bc libgflags-dev libgoogle-glog-dev liblmdb-dev protobuf-compiler")
    sudo("apt-get install -y python-pip")


def _unload_nouveau():
    lines = []
    lines.append("blacklist vga16fb")
    lines.append("blacklist nouveau")
    lines.append("blacklist rivafb")
    lines.append("blacklist nvidiafb")
    lines.append("blacklist rivatv")
    append("/etc/modprobe.d/blacklist.conf", lines, use_sudo=True)

    sudo("update-initramfs -u")
    reboot()


def _install_cuda():
    cuda_path = "{0}/cuda.tmp".format(PREFIX)
    if exists(cuda_path):
        return cuda_path

    _unload_nouveau()

    with cd("/opt/archives"):
        if not exists("/opt/archives/cuda_7.0.28_linux.run"):
            sudo("wget http://developer.download.nvidia.com/compute/cuda/7_0/Prod/local_installers/cuda_7.0.28_linux.run")
        sudo("chmod 755 cuda_7.0.28_linux.run")
        sudo("./cuda_7.0.28_linux.run -silent --driver --toolkit --toolkitpath={0}".format(cuda_path))

    if not exists(cuda_path):
        sudo("cat /tmp/cuda* 1>&2")
        sudo("false")

    return cuda_path


def _install_pydepends():
    sudo("pip install six")
    sudo("apt-get install -y python-numpy python-scipy")


def _install_caffe():
    caffe_path = "{0}/src".format(PREFIX)
    if exists("{0}/build".format(caffe_path)):
        return caffe_path

    if not exists(caffe_path):
        sudo("git clone https://github.com/BVLC/caffe.git {0}".format(caffe_path))
    with cd(caffe_path):
        sudo("cp Makefile.config.example Makefile.config")
        sudo("make -j`nproc` all")
        sudo("make -j`nproc` test")
        sudo("make -j`nproc` runtest")
        sudo("make -j`nproc` pycaffe")

    with cd("{0}/python".format(caffe_path)):
        sudo("pip install -r requirements.txt")

    return caffe_path


def _configure_paths(caffe_path, python_path, cuda_path):
    lines = []

    lines.append("export PATH={0}:$PATH".format(caffe_path))
    lines.append("export PYTHONPATH={0}:$PYTHONPATH".format(python_path))
    lines.append("export LD_LIBRARY_PATH={0}:$LD_LIBRARY_PATH".format(cuda_path))

    append("{0}/caffe.bashrc".format(PREFIX), lines, use_sudo=True)


def deploy():
    _install_depends()
    _install_pydepends()

    sudo("mkdir -p /opt/archives")

    cuda_path = _install_cuda()

    cuda_lib = "{0}/cuda/lib64/".format(PREFIX)
    sudo("mkdir -p {0}/cuda".format(PREFIX))
    sudo("cp -pr {0}/lib64 {1}".format(cuda_path, cuda_lib))
    with path("{0}/bin".format(cuda_path), behavior="prepend"):
        with shell_env(LIBRARY_PATH=cuda_lib, LD_LIBRARY_PATH=cuda_lib, CPATH="{0}/include".format(cuda_path)):
            caffe_path = _install_caffe()

    sudo("rm -rf /opt/archives")
    sudo("rm -rf {0}".format(cuda_path))
    sudo("rm -rf /usr/local/cuda")
    sudo("ln -fs {0}/build {1}/build".format(caffe_path, PREFIX))
    sudo("ln -fs {0}/python {1}/python".format(caffe_path, PREFIX))

    # supress: libdc1394 error: Failed to initialize libdc1394
    if not exists("/dev/raw1394"):
        sudo("ln -s /dev/null /dev/raw1394")
        sudo("sed --in-place -e \"/^exit 0$/i ln -s /dev/null /dev/raw1394\" /etc/rc.local")

    _configure_paths("{0}/build/tools".format(PREFIX), "{0}/python".format(PREFIX), "{0}/cuda/lib64".format(PREFIX))


def local_deploy():
    from contextlib import contextmanager
    from fabric.api import local, lcd
    import os

    def local_sudo(cmd):
        # assuming this code will run as root
        if "apt-get" in cmd:
            if "linux-headers" in cmd:
                local(cmd)
        elif "--driver" in cmd:
          local(cmd.replace("--driver ", ""))
        else:
            local(cmd)

    @contextmanager
    def local_cd(p):
        with lcd(p):
            yield

    def local_exists(p):
        return os.path.exists(p)

    def local_append(p, text, use_sudo):
        if isinstance(text, list):
            text = "\n".join(text)
            text += "\n"

        with open(p) as fp:
            context = fp.read()
            if text in context:
                return None

        with open(p, "a") as fp:
            fp.write(text)

        return text

    def local_reboot():
        pass

    sys.modules[__name__].sudo = local_sudo
    sys.modules[__name__].cd = local_cd
    sys.modules[__name__].exists = local_exists
    sys.modules[__name__].append = local_append
    sys.modules[__name__].reboot = local_reboot

    deploy()
