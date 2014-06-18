package com.interview.careerup;

/**
 * User: gjkv86
 * Date: 13-4-8 16:08
 */
public class StringTest {

    public static void main(String args[]) {
/*
        char c=97;
        System.out.println(c);
*/
        String s = "abcdefga";
//        System.out.println(s.toCharArray());
        System.out.println(isUniqueChars("abd"));
    }


    public static boolean isUniqueChars(String str) {
        int checker = 0;
        for (int i = 0; i < str.length(); ++i) {
            int val = str.charAt(i) - 'a';
            System.out.print(str.charAt(i)+":"+Integer.toBinaryString(val));
            if ((checker & (1 << val)) > 0){
                return false;
            }
            System.out.print("--"+Integer.toBinaryString(val));
            checker |= (1 << val);
            System.out.print("--"+Integer.toBinaryString(val)+"-\n");
        }
        return true;
    }



    public boolean hasDuplication(char s[]) {
        if (s == null || s.length < 2) return false;
        char tmp;
        for (int i = 0; i < s.length; i++) {
            int ci = (int) s[i];
            int cmod = ci % 10;
            if (s[cmod] == s[i]) return true;
            else {
                tmp = s[cmod];
                s[cmod] = s[i];

            }
        }
        return false;
    }
}
