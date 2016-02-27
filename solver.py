import caffe
import skimage.io
import numpy as np

imgname = 'test10.png'
modelname = 'lenet_gesture64/deploy.prototxt'
pretrained_file = 'lenet_gesture64/snapshot_iter_210.caffemodel'


# NVIDIA/caffe-0.14 load_image 'color=False' does not work.
# img = caffe.io.load_image(imgname, color=False)
def load_image_as_gray():
    img = skimage.img_as_float(skimage.io.imread(imgname, as_grey=True)).astype(np.float32)
    if img.ndim == 2:
        img = img[:, :, np.newaxis]
    elif img.shape[2] == 4:
        img = img[:, :, :3]
    return caffe.io.resize_image(img, (64, 64))


caffe.set_mode_cpu()
net = caffe.Classifier(modelname, pretrained_file, image_dims=(64, 64))
scores = net.predict([load_image_as_gray()], oversample=False)
print(scores)
