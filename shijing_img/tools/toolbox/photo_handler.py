__author__ = 'wenjusun'
import os
import shutil
from multiprocessing.pool import ThreadPool
from PIL import Image
import time


def get_current_time():
    return int(round(time.time()*1000))

class PhotoSelector():
    """ copy specified photo to destination"""
    def __init__(self,src_folder,dest_folder):
        self.src_folder = src_folder
        self.dest_folder = dest_folder
        if not os.path.exists(dest_folder):
            os.makedirs(dest_folder)
            print "Destination does not exist,created."
        else:
            print "Photos will be copied to an existing folder."

    def copy_photo(self,src):
        shutil.copy2(src,self.dest_folder)

    ''' selected list is a file contains string separated by comma '''
    def copy_selected_photos(self,selected_list_file):
        #get file content
        id_str = ''
        with open(selected_list_file) as f:
            id_str += f.readline()

        photo_name_list = id_str.split(',')

        src_photos = []
        for photo in photo_name_list:
            # shutil.copy(file_pattern %(src_folder,photo),dest_folder)
            src_photos.append(os.path.join(self.src_folder,photo))

        pool = ThreadPool(4)

        print pool.map(self.copy_photo,src_photos)
        pool.close()
        pool.join()
        print "%d photos are copied to %s" %(len(photo_name_list),self.dest_folder)


class PhotoShop():
    def __init__(self,src_folder,dest_folder,final_size):
        self.src_folder = src_folder
        self.dest_folder = dest_folder
        self.final_size = final_size

        if not os.path.exists(dest_folder):
            os.makedirs(dest_folder)
            print "Destination does not exist,created."
        else:
            print "Photos will be copied to an existing folder."

    def compress_photo(self,photo_file):
        image = Image.open(os.path.join(self.src_folder,photo_file))
        om = image.copy()
        ox,oy = om.size
        n_size=self.final_size,int(float(self.final_size)/ox*oy)
        om.thumbnail(n_size,Image.ANTIALIAS)
        om.save(os.path.join(self.dest_folder,photo_file))

    def batch_compress_photos(self):
        pool = ThreadPool(4)

        photos = os.listdir(self.src_folder)
        print "%d photos founded in %s" %(len(photos),self.src_folder)
        pool.map(self.compress_photo,photos)

        pool.close()
        pool.join()
        print "%d photos compressed to width:%d" %(len(photos),self.final_size)


    def batch_compress_photos2(self):
        "This takes double time of the Threadpool one."
        photos = os.listdir(self.src_folder)
        print "%d photos founded in %s" %(len(photos),self.src_folder)
        for photo in photos:
            self.compress_photo(photo)
        print "%d photos compressed to width:%d" %(len(photos),self.final_size)


def copy_photo(src):
    shutil.copy2(src,dest_folder)

if __name__ == '__main22__':
    start_time =get_current_time()

    dest_folder = r"c:\ZZZZZ\abc"
    src_folder = r"C:\Users\wenjusun\Pictures\2016_02_10"
    ps = PhotoSelector(src_folder,dest_folder)
    ps.copy_selected_photos(r"c:\ZZZZZ\0-sunwj\simglist.txt")

    end_time =get_current_time()

    print "%d seconds used " % ((end_time-start_time)/1000)

if __name__ == '__main__':
    start_time =get_current_time()

    dest_folder = r"c:\ZZZZZ\abc3"
    src_folder = r"C:\Users\wenjusun\Pictures\timages"
    src_folder = r"C:\ZZZZZ\1-photo\2"
    ps = PhotoShop(src_folder,dest_folder,600)
    ps.batch_compress_photos2()

    end_time =get_current_time()

    print "%d seconds used " % ((end_time-start_time)/1000)

