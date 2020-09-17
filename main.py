#!/GPFS/zhangli_lab_permanent/zhuqingjie/env/py3_tf2/bin/python
'''
@Time    : 20/09/11 下午 02:43
@Author  : zhuqingjie 
@User    : zhu
@FileName: main.py
@Software: PyCharm
'''
import traceback

try:
    import yaml, os, cv2
    from pathlib import Path
    import numpy as np
    import tensorflow as tf
    import tensorflow.contrib

    tf.get_logger().setLevel('ERROR')


    def kvprint(k, v, k_len=15):
        k = k + ':'
        if len(k) >= k_len:
            print(f'{k}{v}')
        else:
            print(f'{k}{" " * (k_len - len(k))}{v}')


    kvprint("Tensorflow version", tf.__version__)

    # load config file
    cfg_path = 'config.yaml'
    if not Path(cfg_path).exists():
        print(f'the {cfg_path} file in the same folder is not exists!')
        os.system('pause')
        exit()
    cfg = yaml.safe_load(open('config.yaml', 'r'))

    # print config file
    print(f'\n{"+" * 20} config {"+" * 20}')
    for k, v in cfg.items():
        kvprint(k, v)
    print(f'{"+" * 20} config {"+" * 20}\n')

    # import module
    if cfg['sr_or_os'] == 'sr':
        from model import UNET_sr as unet
    elif cfg['sr_or_os'] == 'os':
        from model import UNET_os as unet
    else:
        print('please set a right value of param sr_or_os in config.yaml, option values: sr, os.')


    def load_img(img_dir):
        img_dir = Path(img_dir)
        if img_dir.is_dir():
            files = list(img_dir.iterdir())
            # 过滤掉上次预测产生的结果
            files = [f for f in files if not f.stem.endswith('_predict')]
            for f in files:
                img = cv2.imread(str(f))
                if img is not None:
                    yield img, str(f)
        else:
            img = cv2.imread(str(img_dir))
            if img is not None:
                yield img, str(img_dir)


    def inference():
        # load img
        if not Path(cfg['img_path']).exists():
            print('please check if the path of image is exists or not.')
            return
        imgs_and_paths = load_img(cfg['img_path'])

        # load model and run
        model = unet(predict_flag=True)
        with tf.Session(graph=model.graph) as sess:
            saver = tf.train.Saver()
            try:  # 这一步如果报错，很有可能是os、sr模型没有对应正确
                saver.restore(sess, cfg['model_path'])
                print(f'load model from: {cfg["model_path"]}')
            except Exception:
                traceback.print_exc()
                print('''
                    please check if the param "model_path" and "sr_or_os" are correct or not!
                    "model_path" and "sr_or_os" must be corresponding.
                    ''')

            is_has_imgs = False
            for img, img_path in imgs_and_paths:
                is_has_imgs = True
                print('-' * 100)
                kvprint('Input', img_path)
                # convert data
                if ((img[:, :, 0] == img[:, :, 1]) *
                    (img[:, :, 0] == img[:, :, 2])).all():  # gray img
                    x = img[np.newaxis, :, :, :1]
                    kvprint('Channel', '1')
                else:  # color img
                    x = np.transpose(img, [2, 0, 1])
                    x = x[:, :, :, np.newaxis]
                    kvprint('Channel', '3')
                x = x.astype(np.float16) / 255

                res = sess.run(model.prd, feed_dict={model.x: x})

                # save result
                if len(res) == 1:
                    res = res[0, :, :, 0]
                else:
                    res = res[:, :, :, 0]
                    res = np.transpose(res, [1, 2, 0])
                res = np.round(res * 255).astype(np.uint8)
                src_path = Path(img_path)
                dst_path = str(Path(src_path.parent, f'{src_path.stem}_predict.tif'))
                cv2.imwrite(dst_path, res)
                kvprint('Output', dst_path)

            if not is_has_imgs:
                print('No eligible images were found!')


    if __name__ == '__main__':
        inference()
        os.system('pause')


except Exception as e:
    print(e)
    traceback.print_exc()
    os.system('pause')

'''
更新内容：
1，异常参数的判断；
2，彩色图像的支持；
3，批处理图像的支持（必须要求同一文件夹下的图像具有相同分辨率，有待改进）；
4，解决了上一条的问题，允许同一批次下有不同分辨率的图像；
'''
