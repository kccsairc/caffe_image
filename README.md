Caffe Image
===

Deploy scripts of caffe.

Example
---
    $ source /opt/caffe/caffe.bashrc 
    $ caffe.bin 
    caffe.bin: command line brew
    usage: caffe <command> <args>

    commands:
      train           train or finetune a model
      test            score a model
      device_query    show GPU diagnostic information
      time            benchmark model execution time
    
      Flags from tools/caffe.cpp:
        -gpu (Run in GPU mode on given device ID.) type: int32 default: -1
        -iterations (The number of iterations to run.) type: int32 default: 50
        -model (The model definition protocol buffer text file..) type: string
          default: ""
        -snapshot (Optional; the snapshot solver state to resume training.)
          type: string default: ""
        -solver (The solver definition protocol buffer text file.) type: string
          default: ""
        -weights (Optional; the pretrained weights to initialize finetuning. Cannot
          be set simultaneously with snapshot.) type: string default: ""
    $ python
    Python 2.7.6 (default, Mar 22 2014, 22:59:56) 
    [GCC 4.8.2] on linux2
    Type "help", "copyright", "credits" or "license" for more information.
    >>> import caffe
    >>> exit()
    $ 
    
Utility
---
    $ ls model/
    caffemodel  deploy.prototxt  export.py  label.json  labellio.json  mean.binaryproto
    $ ls image/
    cat1.jpg  cat2.jpg  dog1.jpg  dog2.jpg  lion1.jpg  lion2.jpg  wolf1.jpg  wolf2.jpg
    $ bin/classify model/  image/ > results.txt
    $ cat results.txt
    image/wolf2.jpg dog     [  9.80339944e-04   9.98520672e-01   1.10457813e-05   4.87920537e-04]
    image/lion1.jpg dog     [ 0.04076573  0.76182348  0.08646383  0.11094711]
    image/dog1.jpg  lion    [ 0.08353562  0.18364988  0.64138454  0.09142993]
    image/cat2.jpg  dog     [  1.24202315e-02   9.15666461e-01   7.88990583e-04   7.11244121e-02]
    image/lion2.jpg cat     [ 0.92806995  0.0217264   0.00815737  0.04204625]
    image/cat1.jpg  dog     [ 0.25713155  0.6934157   0.00243184  0.047021  ]
    image/wolf1.jpg cat     [  9.81454432e-01   5.84143971e-04   1.61686055e-02   1.79276010e-03]
    image/dog2.jpg  cat     [ 0.90410995  0.07049562  0.00874097  0.01665348]
