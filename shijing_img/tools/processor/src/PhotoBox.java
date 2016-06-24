/**
 * Created by wenjusun on 6/24/16.
 */

/**
 * Facade for photo utilities
 * */
public class PhotoBox {
    public static void main(String args[]){
        if (args.length<2){
            System.out.println("Invalid arguments");
            System.exit(0);
        }

        String requestType = args[0];

        PhotoBox photoBox = new PhotoBox();
        if(Request.valueOf(requestType)==Request.compressPhoto){

            String sourcePhotoFolder = args[1];
            String destPhotoFolder = args[2];
            String size = args[3];
            photoBox.compressPhotos(sourcePhotoFolder,destPhotoFolder,size);

        }
        else if(Request.valueOf(requestType)==Request.copyFiles){

            photoBox.copyFiles();

        }else {
            System.out.println("Unknow request:"+requestType);
        }

    }

    enum Request{
        compressPhoto("compress"),
        copyFiles("copy");

        private String value;
        Request(String value) {
            this.value = value;
        }

    }

    public void copyFiles(){

    }

    public void compressPhotos(String sourcePhotoFolder,String destPhotoFolder,String size){

    }
}
