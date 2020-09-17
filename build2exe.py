#!/GPFS/zhangli_lab_permanent/zhuqingjie/env/py3_tf2/bin/python
'''
@Time    : 20/09/11 下午 05:02
@Author  : zhuqingjie 
@User    : zhu
@FileName: build2exe.py
@Software: PyCharm
'''
import PyInstaller.__main__

PyInstaller.__main__.run([
    '--onefile',  # 生成单独一个exe文件，而不是一个文件夹
    '--clean',  # 清除上次运行的缓存
    '--noupx',  # 不压缩，快速发布，正式发布的时候还是可以压缩
    'main.py'
])
