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