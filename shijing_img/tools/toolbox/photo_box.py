__author__ = 'wenjusun'

import sys

def batch_compress_photos(src_folder,dest_folder,size):
    pass

def copy_files(src_folder,dest_folder):
    pass

if __name__ == '__main__':
    args = sys.argv

    request_type = args[1]

    if request_type=='cp':
        src_folder = args[2]
        dest_folder = args[3]
        copy_files(src_folder,dest_folder)

    elif request_type == 'compress':
        src_folder = args[2]
        dest_folder = args[3]

        size = int(args[4])
        batch_compress_photos(src_folder,dest_folder,size)

