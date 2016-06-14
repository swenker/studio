import java.io.*;
import java.nio.channels.FileChannel;
import java.util.ArrayList;
import java.util.List;
import java.util.StringTokenizer;

/**
 * Created by wenjusun on 10/18/2015.
 */
public class PhotoTool {

    public static void main(String args[]) {
        if (args.length<3) {
            System.out.println("not enough args");
            System.exit(0);
        }

        String srcPath = args[0];
        String destPath =args[1];

        String selectedImgs = args[2];

        StringBuilder sb = new StringBuilder();
        try (BufferedReader br = new BufferedReader(new FileReader(selectedImgs))) {

            String line = br.readLine();
            while(line!=null && line.length()>0){
                sb.append(line);
                sb.append(" ");
                line = br.readLine();
            }
        } catch (IOException e) {
            e.printStackTrace();
        }

        List<String> selectImgList = new ArrayList<String>();
        System.out.println(sb.toString());
        StringTokenizer st = new StringTokenizer(sb.toString(), " ");
        while (st.hasMoreTokens()) {
            String img = st.nextToken();

            if (img.length() > 0) {
                selectImgList.add(img);
            }

        }

        System.out.printf("total get %d selected imgs \n", selectImgList.size());

        String sourceFileFormat = "%s\\%s";
        String destFileFormat = "%s\\%s";

        int okCounter = 0;
        int failCounter = 0;
        for (String img : selectImgList) {
            String sourceFile = String.format(sourceFileFormat, srcPath, img);
            String destFile = String.format(destFileFormat, destPath, img);

            System.out.printf("copying %s......", sourceFile);
            if (copyFile(sourceFile, destFile)) {
                System.out.printf("copied \n");
                okCounter++;
            } else {
                System.out.printf("Failed \n");
                failCounter++;
            }
        }

        System.out.printf("OK:%d,Failed:%d \n", okCounter, failCounter);


    }

    static boolean copyFile(String src, String dest) {

        try (FileInputStream fis = new FileInputStream(src);
             FileOutputStream fos = new FileOutputStream(dest);
             FileChannel fic = fis.getChannel();
             FileChannel foc = fos.getChannel()) {

            fic.transferTo(0, fis.available(), foc);

            return true;
        } catch (IOException e) {
            e.printStackTrace();
        }
        return false;

    }
}
