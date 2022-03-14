import shutil
import os
from PIL import Image
import warnings
import argparse

def get_date_taken_folder(path):
    # https://www.awaresystems.be/imaging/tiff/tifftags/privateifd/exif.html
    # date digitized
    dt = Image.open(path)._getexif()[36868]

    # look in gps data
    if 29 in Image.open(path)._getexif()[34853].keys() and Image.open(path)._getexif()[34853][29]:
        dt = Image.open(path)._getexif()[34853][0]

    if dt == None:
        warnings.warn("WARNING: {} does not contain date metadata. Not copying file".format(path))
        return dt
    
    return dt[:4] + dt[5:7]

def parse_args():
    parser = argparse.ArgumentParser()
    
    parser.add_argument('--src', type=str, required=True)
    parser.add_argument('--dest', type=str, required=True)
    parser.add_argument('--err_file', type=str, required=True)

    return parser.parse_args()

if __name__ == "__main__":
    args = parse_args()
    src = args.src
    dest = args.dest
    err_file = args.err_file

    f = open(err_file, 'a')

    for img_name in os.listdir(src):
        src_file = os.path.join(src, img_name)
        dt = get_date_taken_folder(src_file)

        if not dt:
            f.write(src_file)
            f.write("\n")
            continue

        dest_folder = os.path.join(dest, dt)
        if not os.path.isdir(dest_folder):
            print("creating destination folder [{}] in dir [{}]".format(dt, dest))
            os.mkdir(dest_folder)
        
        print("copying file [{}] from src: [{}] to dest: [{}]".format(img_name, src, dest_folder))
        shutil.copy2(src_file, dest_folder, follow_symlinks = True)



