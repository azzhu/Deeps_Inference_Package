
使用说明：

1，下载程序文件，包括：
    可执行文件：main.exe；
    配置文件：config.yaml；
    预训练模型文件：model文件夹。

2，修改和设置配置文件config.yaml：
    img_path：单张图像路径、多张图像所在文件夹路径。暂不支持中文路径；
    model_path：模型路径。每个模型有两个文件，例如：
        model_68900.data-00000-of-00001
        model_68900.index
        则该模型路径为：{所在文件夹路径}\model_68900
    sr_or_os：可选值：sr、os。处理哪种任务，是sr还是os。注意：该值跟model_path是对应的，不可以这里设置os，模型却选的是sr的模型。

3，运行：
    双击main.exe开始运行，同时会弹出命令行窗口显示运行信息。