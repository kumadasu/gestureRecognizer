import caffe


caffe.set_mode_cpu()
net = caffe.Classifier('lenet_gesture64/deploy.prototxt', 'lenet_gesture64/snapshot_iter_210.caffemodel', image_dims=(64, 64))
scores = net.predict([caffe.io.load_image('triangle.png', color=False)], oversample=False)
print(scores)
