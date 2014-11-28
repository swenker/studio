package algorithm;

import java.security.SecureRandom;
import java.util.Collections;
import java.util.Random;

/**
 * Created with IntelliJ IDEA.
 * User: samsung
 * Date: 14-11-19
 * Time: 下午4:29
 * To change this template use File | Settings | File Templates.
 */
public class Algorithm {

    public static void main(String args[]) {
        Algorithm algorithm = new Algorithm();

//        algorithm.stringToInt();
//        algorithm.reverseString();
        algorithm.shuffle();
    }


    public void reverseString(){
        String s="123456";
        s="12345";
        s="i am a boy";
        char tmp[] = s.toCharArray();

        for (int i=0,j=tmp.length-1;i<tmp.length/2;i++,j--){
            char t = tmp [i];
            tmp[i] = tmp[j];
            tmp[j] = t;
        }

        System.out.println(new String(tmp));

    }
    public void stringToInt() {
        String abc = "-88135";
        long result = 0;

        char tmp[] = abc.toCharArray();

        boolean minus = false;
        if (tmp[0] == '-')
            minus = true;
        int i = 0;
        if (minus) i = 1;
        for (; i < tmp.length; i++) {
            int digit = Character.digit(tmp[i], 10);

            System.out.print(digit);
            result = result * 10;
            result += digit;
        }
        if (minus)
            result = 0 - result;
        System.out.println(result);
    }

    public void stringToInt2() {
        String abc = "-88135";
        long result = 0;

        char tmp[] = abc.toCharArray();

        boolean minus = false;
        if (tmp[0] == '-')
            minus = true;

        int end = 0;
        if (minus) end = 1;
        for (int i = tmp.length - 1; i >= end; i--) {
            int digit = Character.digit(tmp[i], 10);
            System.out.print(digit);

            result = digit * 10;
            result += digit;
        }
        if (minus)
            result = 0 - result;
        System.out.println(result);
    }

    public void shuffle(){
        Random random =  new Random();

        System.out.println(random.nextInt(1));
        System.out.println(random.nextInt(1));
        System.out.println(random.nextInt(1));
        System.out.println(random.nextInt(1));
        char[]s = "ab".toCharArray();

        int i=s.length-1;
        for (;i>0;i--){
            char t = s[i];
            int target = random.nextInt(i);
            s[i]=s[target];
            s[target] = t;
        }
        System.out.println(new String(s));
    }

}
