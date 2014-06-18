import java.io.File;
import java.net.URL;
import java.net.URLClassLoader;
import java.util.Enumeration;
import java.util.Properties;

public class JavaEnv {
    public static void main(String args[]){
        Properties properties=System.getProperties();
        Enumeration names=properties.propertyNames();
/*
        while (names.hasMoreElements()){
            String pname=(String)names.nextElement();
            System.out.printf("%s:%s",pname,properties.getProperty(pname));
        }
*/

//        printClassPath();
//          printObjectAddress();

        System.out.println(JavaEnv.class.getInterfaces()[0]);
    }

    static void printObjectAddress(){
        String a="ab";
        String b="a"+"b";

//        System.out.println(a==b);

        Integer ia=402;
        Integer ib=402;

        System.out.println(ia==ib);

    }
    static void printClassPath(){
        StringBuffer buffer = new StringBuffer();
        for (URL url :
                ((URLClassLoader) (Thread.currentThread()
                        .getContextClassLoader())).getURLs()) {
            buffer.append(new File(url.getPath()));
            buffer.append(System.getProperty("path.separator"));
        }
        String classpath = buffer.toString();
        System.out.println(classpath);

    }
}
