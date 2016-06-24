__author__ = 'wenjusun'
import os
import shutil

class PhotoShop():
    def __init__(self):
        pass

    ''' selected list is a file contains string separated by comma '''
    def copy_selected_photos(self,selected_list,src_folder,dest_folder):

        if not os.path.exists(dest_folder):
            os.mkdir(dest_folder)


        #get file content
        id_str = ''
        with os.open(selected_list,'r') as f:
            id_str += f.readline()


        photo_list = id_str.split(',')

        file_pattern="%s/%s"
        counter = 0

        for photo in photo_list:
            shutil.copy(file_pattern %(src_folder,photo),dest_folder)
            counter += 1

        print "%d photos copied to %s" %(counter,dest_folder)

         

    def compress_photo(self,src_folder,dest_folder):




    def batch_compress_photos(src_folder,dest_folder,size):
        pass

