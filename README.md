#Deeps Server Inference Package
A released inference package of deeps server. use this package you can process your datas in you loacal computer easily.
![avatar](imgs/img.bmp)

##Instructions

###Download Files
Download files from [here](http://119.90.33.35:3557/sharing/wJWmfODpQ), the files include:
    
    Executable file: main.exe;
    Config file: config.yaml;
    Pre-trained model file: model/.

###Config
Modify the config file: *config.yaml*.

    img_path: A path of single image, or a folder path of many images；
    model_path: Model path. one model has two files, for example:
            model_68900.data-00000-of-00001
            model_68900.index
        So parameter 'model_path' should be set to '{current directory}\model_68900'
    sr_or_os: Option:sr,os. If your purpose is image super-resolution, you should select 'sr',
    conversely, you should select 'os'. But it's important to note, parameter 'sr_or_os' and 'model_path' should be corresponding.

###Run:
Double-click *main.exe* to run, a cmd window will pop up and print the output text during the executive process.
