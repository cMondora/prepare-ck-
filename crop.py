import dlib
import argparse
import os
import sys
from glob import glob
import cv2
import numpy as np
import shutil

this_path = os.path.dirname(__file__)

def main(argv):
    predictor_path = this_path + "/dlib_models/shape_predictor_68_face_landmarks.dat"
    detector = dlib.get_frontal_face_detector()

    for l_s in os.listdir(argv.images_dir):
        label_dirs=os.path.join(argv.images_dir,l_s)
        if os.path.exists(os.path.join(argv.save_dir, l_s)):
            shutil.rmtree(os.path.join(argv.save_dir, l_s))
        os.mkdir(os.path.join(argv.save_dir, l_s))
        for name in os.listdir(label_dirs):
            name_dirs=os.path.join(label_dirs,name)

            if os.path.exists(os.path.join(argv.save_dir,l_s,name)):
                shutil.rmtree(os.path.join(argv.save_dir,l_s,name))
            os.mkdir(os.path.join(argv.save_dir,l_s,name))

            images_file=glob(name_dirs+os.sep+'*.png')
            for image in images_file:
                image_name=os.path.basename(image)
                img=cv2.imread(image)
                faces=detector(img,1)

                for k,d in enumerate(faces):

                    height = d.bottom() - d.top()

                    width = d.right() - d.left()

                    img_blank = np.zeros((height, width, 3), np.uint8)



                    for i in range(height):
                        for j in range(width):
                            img_blank[i][j] = img[d.top() + i][d.left() + j]

                    img_re=cv2.resize(img_blank,(240,240))


                    cv2.imwrite(os.path.join(argv.save_dir,l_s,name,image_name),img_re)







def parse_arguments(argv):
    parser=argparse.ArgumentParser()

    parser.add_argument('images_dir',type=str,help='the images directory')
    parser.add_argument('save_dir', type=str, help='the save directory')

    return parser.parse_args(argv)

if __name__ == '__main__':
    main(parse_arguments(sys.argv[1:]))