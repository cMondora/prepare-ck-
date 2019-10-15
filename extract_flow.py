import cv2
import argparse
import numpy as np
import sys
import os
import copy
import time
import shutil
from glob import glob

bound = 10
xFlowFile = 'x_flow'
yFlowFile = 'y_flow'
imgFile = 'img'

def cast(v, L, H):
    r = 0
    if v > H:
        r = 255
    elif v < L:
        r = 0
    else:
        r = np.round(255 * (v - L) / (H - L))

    return r


def convertFlowToImage(flowx, flowy, imgX, imgY, lowerBound, higherBound):
    for i in range(flowx.shape[0]):
        for j in range(flowy.shape[1]):
            x = flowx[i, j]
            y = flowy[i, j]
            imgX[i, j] = cast(x, lowerBound, higherBound)
            imgY[i, j] = cast(y, lowerBound, higherBound)
    return imgX, imgY



def main(argv):


    for l_s in os.listdir(argv.images_dir):
        label_dirs = os.path.join(argv.images_dir, l_s)
        if os.path.exists(os.path.join(argv.save_dir, l_s)):
            shutil.rmtree(os.path.join(argv.save_dir, l_s))
        os.mkdir(os.path.join(argv.save_dir, l_s))
        print("dealing with {}".format(l_s))
        for name in os.listdir(label_dirs):
            name_dirs = os.path.join(label_dirs, name)

            if os.path.exists(os.path.join(argv.save_dir, l_s, name)):
                shutil.rmtree(os.path.join(argv.save_dir, l_s, name))
            save_path=(os.path.join(argv.save_dir, l_s, name))
            os.mkdir(save_path)


            image_files=sorted(os.listdir(name_dirs))
            if os.path.exists(os.path.join(save_path,xFlowFile)):
                shutil.rmtree(os.path.join(save_path,xFlowFile))
            os.mkdir(os.path.join(save_path,xFlowFile))
            if os.path.exists(os.path.join(save_path,yFlowFile)):
                shutil.rmtree(os.path.join(save_path,yFlowFile))
            os.mkdir(os.path.join(save_path,yFlowFile))
            for i in range(len(image_files)-1):
                prev_image = cv2.imread(os.path.join(name_dirs,image_files[i]))
                prev_gray = cv2.cvtColor(prev_image, cv2.COLOR_BGR2GRAY)
                image = cv2.imread(os.path.join(name_dirs,image_files[i+1]))
                gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
                flow = cv2.calcOpticalFlowFarneback(prev_gray, gray, None, 0.702, 5, 10, 2, 7, 1.5,cv2.OPTFLOW_FARNEBACK_GAUSSIAN)

                flow0, flow1 = cv2.split(flow)
                imgX, imgY = copy.copy(flow0), copy.copy(flow1)

                imgX, imgY = convertFlowToImage(flow0, flow1, imgX, imgY, -1. * bound, bound)
                # print('_%04d.jpg'.format(frame_num))
                frame_name=os.path.basename(save_path)
                tmp = frame_name+'_'+'%08d.png' % (i+1)
                cv2.imwrite(os.path.join(save_path, xFlowFile, tmp), imgX)
                cv2.imwrite(os.path.join(save_path, yFlowFile, tmp), imgY)

                sys.stdout.write('\r%s%%' % int(i / (len(image_files)-1) * 100))
                sys.stdout.flush()
                time.sleep(0.1)






def parse_arguments(argv):
    parser=argparse.ArgumentParser()

    parser.add_argument('images_dir',type=str,help='the images directory')
    parser.add_argument('save_dir', type=str, help='the save directory')

    return parser.parse_args(argv)

if __name__ == '__main__':
    main(parse_arguments(sys.argv[1:]))