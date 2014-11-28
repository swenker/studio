package encoding;

import java.util.prefs.AbstractPreferences;

/**
 * Created with IntelliJ IDEA.
 * User: samsung
 * Date: 14-8-19
 * Time: 上午11:33
 * To change this template use File | Settings | File Templates.
 */
public class StreamEncoding {

    public static void main(String args[]){
        int a =0x8b;
        int c = 0x8b&0xff;
        byte b = (byte) a;

        //System.out.println(b);

        int a1=1001;

        byte bb[]=new byte['\u0080'];
        byte bbb[]=new byte[0];
        char c128=128;
        System.out.println(c128);
        System.out.println(bbb.length);

    }
}
