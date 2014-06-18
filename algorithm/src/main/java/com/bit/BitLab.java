package com.bit;

/**
 * User: gjkv86
 * Date: 13-5-22 00:35
 */
public class BitLab {
    public static void main(String args[]){
        int max=~0;

        int i=2,j=6;

        System.out.println("max:"+Integer.toBinaryString(max));

        System.out.println("jj:"+Integer.toBinaryString(((1<<j)-1)));
        int left=max-((1<<(j+1))-1);

        System.out.println(Integer.toBinaryString(left));
        int right=((1<<i)-1);

        System.out.println(Integer.toBinaryString(right));

        int mask = left|right;

        System.out.println("mask:"+Integer.toBinaryString(mask));

        int n=Integer.parseInt("10000000000",2), m = Integer.parseInt("10101",2);
        int r=(n & mask) | (m << i);

        System.out.println("r:"+Integer.toBinaryString(r));
    }
}
