import argparse
import os
import sys
import shutil
import re

def find_txt(dirs,out_dir,video_file):
    for l_s in os.listdir(dirs):
        label_dirs=os.path.join(dirs,l_s)
        if os.path.isdir(label_dirs):
            for name in os.listdir(label_dirs):
                name_dirs=os.path.join(label_dirs,name)
                try:
                    txt=os.listdir(name_dirs)[0]
                    txt_name=txt.split('.')[0]
                    with open(os.path.join(name_dirs,txt),'r',encoding='utf-8') as f:
                        class_txt=f.read()
                        class_num=re.findall('\d',class_txt)[0]
                    out_path=os.path.join(out_dir,str(class_num))
                    target_dir=os.path.join(video_file,txt_name.split('_')[0],txt_name.split('_')[1])
                    shutil.copytree(target_dir,os.path.join(out_path,txt_name[:8]))
                except:
                    pass



def main(argv):
    for i in range(8):
        if os.path.exists(os.path.join(argv.outpath,str(i))):
            shutil.rmtree(os.path.join(argv.outpath,str(i)))
        os.mkdir(os.path.join(argv.outpath,str(i)))
    out_dir=argv.outpath
    label_dir=argv.label_dir
    video_file=argv.video_file
    find_txt(label_dir,out_dir,video_file)



def parse_arguments(argv):
    parser=argparse.ArgumentParser()

    parser.add_argument('video_file',type=str,help='video directory')
    parser.add_argument('label_dir',type=str,help='label directory')
    parser.add_argument('outpath',type=str,help='save path')

    return parser.parse_args(argv)
if __name__ == '__main__':
    main(parse_arguments(sys.argv[1:]))