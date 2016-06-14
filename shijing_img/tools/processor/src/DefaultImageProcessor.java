
import java.io.*;
import java.awt.image.BufferedImage;
import java.awt.*;

import com.sun.image.codec.jpeg.JPEGImageDecoder;
import com.sun.image.codec.jpeg.JPEGCodec;
import com.sun.image.codec.jpeg.JPEGImageEncoder;
import com.sun.image.codec.jpeg.JPEGEncodeParam;

/**
 * @author : Sun Wenju
 *         Date: Apr 5, 2008 12:40:02 PM
 *         todo how to compress images?
 */
public class DefaultImageProcessor {

    private TextStamp textStamp;


    public static void main(String args[]) {
        DefaultImageProcessor imageProcessor = new DefaultImageProcessor();

        //imageProcessor.testBatchZoom();

        if(args.length!=3){
            System.out.println("source,target,width");
        }
        else{
//            System.out.println(args[0]);
            imageProcessor.batchProcess(args[0],args[1],Integer.parseInt(args[2]));
        }
    }

    void testBatchZoom(){
        String source = "C:\\ZZZZZ\\projects\\001_shijing\\processor\\test\\input";
        String target = "C:\\ZZZZZ\\projects\\001_shijing\\processor\\test\\output2";

        batchProcess(source,target,1024);
    }

    void testSingleZoom(){
        try {
            String originPath = "C:\\ZZZZZ\\projects\\001_shijing\\processor\\test\\input\\IMG_1365.jpg";
            String zoomedPath = "C:\\ZZZZZ\\projects\\001_shijing\\processor\\test\\output\\IMG_5531.JPG";
            zoom(originPath, zoomedPath, 1024);

        } catch (Exception e) {
            e.printStackTrace();
        }
    }
    public DefaultImageProcessor() {

        if (System.getProperty("java.awt.headless") == null) {
            System.setProperty("java.awt.headless", "true");
        }
    }

    public void batchProcess(String source, String target,int sizeLimit) {
        File srcFolder = new File(source);
        int counter = 0;
        if (srcFolder.exists() && srcFolder.isDirectory()) {
            File targetFolder = new File(target);
            targetFolder.mkdir();

            File[] subfiles = srcFolder.listFiles();
            System.out.println("--------------------Files Found:"+subfiles.length);

            for (File f :subfiles) {
                //System.out.println(f.getName());
                if(f.isFile()) {
                    try {
                        File targetFile = new File(targetFolder,f.getName());
                        String originPath = f.getCanonicalPath();
                        String zoomedPath = targetFile.getCanonicalPath();
                        zoom(originPath, zoomedPath,sizeLimit);

                        counter++;

                    } catch (Exception e) {
                        e.printStackTrace();
                    }
                }
            }

        }

        System.out.println("--------------------Files processed:"+counter);

    }

    public void setTextStamp(TextStamp textStamp) {
        this.textStamp = textStamp;
    }

    /**
     * 传入原图，生成小图，目前，只支持jpg。
     *
     * @param originPath full path
     * @param zoomedPath full path
     * @param sizeLimit
     */
    public void zoom(final String originPath, String zoomedPath,int sizeLimit) throws Exception {
        File fileIn = new File(originPath);
        boolean operateOriginal = false;
        //render the same image and output to same path.
        if (zoomedPath == null) {
            zoomedPath = originPath;
            operateOriginal = true;
        }
        File fileOut = new File(zoomedPath);

        if (!operateOriginal && fileOut.exists()) fileOut.delete();

        if (!fileOut.getParentFile().exists()) {
            fileOut.getParentFile().mkdirs();
        }

        fileOut.createNewFile();


        InputStream input = new FileInputStream(fileIn);
        if (operateOriginal) {
            //this is a byte arrayStream;
            input = this.getInputStream(input);
        }
        OutputStream output = new FileOutputStream(fileOut);

        String fileExt = parseFileExtension(originPath);
        if (guessImageType(fileExt).equals(RenderSpecification.IMAGE_TYPE_JPEG)) {
            zoomJPG(input, output, sizeLimit);
        } else {
            throw new Exception("not supported type:" + fileExt);
        }

        input.close();
        output.close();

    }

    //get the bytes first,then overwrite the file using the rendered bytes
    private InputStream getInputStream(InputStream sourceInputStream) throws IOException {
        byte tempByte[] = new byte[1024];
        ByteArrayOutputStream baos = new ByteArrayOutputStream(sourceInputStream.available());
        int read = -1;
        while ((read = sourceInputStream.read(tempByte)) > -1) {
            baos.write(tempByte, 0, read);
        }
        sourceInputStream.close();
        return new ByteArrayInputStream(baos.toByteArray());
    }

    /**
     * todo use the other implementation
     * sun's implementation, will not workable when run on other jdk.
     *
     * @param input
     * @param output
     * @param sizeLimit
     */
    private void zoomJPG(InputStream input, OutputStream output, int sizeLimit) throws java.io.IOException {
        JPEGImageDecoder decoder = JPEGCodec.createJPEGDecoder(input);
        JPEGImageEncoder encoder = JPEGCodec.createJPEGEncoder(output);

        BufferedImage imageSrc = decoder.decodeAsBufferedImage();

        int width = imageSrc.getWidth();
        int height = imageSrc.getHeight();


        RenderSpecification spec = new RenderSpecification(RenderSpecification.SIZE_TYPE_WIDTH,sizeLimit,1.0f);
        boolean isPortrait = width < height;

        if(isPortrait)
            spec.setSizeType(RenderSpecification.SIZE_TYPE_HEIGHT);

        //if it's null,orignal size is used
        if (spec.getSizeType() != null) {
            ImageSize imageSize = calculateTargetSize(width, height, spec.getSizeType(), spec.getSize());
            width = imageSize.getWidth();
            height = imageSize.getHeight();
        }
        Image img = imageSrc.getScaledInstance(width, height, Image.SCALE_SMOOTH);

        BufferedImage outBufferedImage = new BufferedImage(width, height, BufferedImage.TYPE_INT_RGB);

        JPEGEncodeParam jpegEncodeParam = JPEGCodec.getDefaultJPEGEncodeParam(outBufferedImage);

        if (spec.getQuality() != null) {
            jpegEncodeParam.setQuality(spec.getQuality(), true);
        }
        encoder.setJPEGEncodeParam(jpegEncodeParam);

        Graphics2D biContext = outBufferedImage.createGraphics();
        biContext.drawImage(img, 0, 0, null);

        if (this.textStamp != null) {
            //todo set color
            biContext.setFont(textStamp.getFont());

            biContext.drawString(textStamp.getText(),
                    width - biContext.getFontMetrics().stringWidth(textStamp.getText()) - 10,
                    height - textStamp.getFont().getSize() + 10);

        }

        encoder.encode(outBufferedImage);
        biContext.dispose();

    }


    private String guessImageType(String fileExt) {
        if ("jpg".equalsIgnoreCase(fileExt) || ("jpeg").equalsIgnoreCase(fileExt)) {
            return RenderSpecification.IMAGE_TYPE_JPEG;
        } else {
            return RenderSpecification.IMAGE_TYPE_GIF;
        }
    }

    /**
     * 图像尺寸处理
     */
    private class ImageSize {
        private int width;
        private int height;

        public ImageSize(int width, int height) {
            this.width = width;
            this.height = height;
        }


        public int getWidth() {
            return width;
        }

        public void setWidth(int width) {
            this.width = width;
        }

        public int getHeight() {
            return height;
        }

        public void setHeight(int height) {
            this.height = height;
        }

    }

    private ImageSize calculateTargetSize(int width, int height, String sizeType, int targetSize) {

        //todo 这里有误差：整数丢失精度
        //todo support ratio
        if (RenderSpecification.SIZE_TYPE_WIDTH.equals(sizeType)) {
            float div = 1.0f * width / targetSize;
            Float wbigDecimal = new Float(Math.ceil(width / div));
            width = wbigDecimal.intValue();
            Float hbigDecimal = new Float(Math.ceil(height / div));
            height = hbigDecimal.intValue();
        } else if (RenderSpecification.SIZE_TYPE_HEIGHT.equals(sizeType)) {
            float div = 1.0f * height / targetSize;
            Float wbigDecimal = new Float(Math.ceil(width / div));
            width = wbigDecimal.intValue();
            Float hbigDecimal = new Float(Math.ceil(height / div));
            height = hbigDecimal.intValue();
        }

        return new ImageSize(width, height);
    }


    /**
     * @param path file name with path,such as /usr/hello.java
     * @return return the parsed file extension
     */
    public static String parseFileExtension(String path) {
        if (path != null && path.contains(".")) {
            return path.substring(path.lastIndexOf(".") + 1);
        }
        return "";
    }
}
