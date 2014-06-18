package com.interview.asurion;

/**
 * User: gjkv86
 * Date: 13-4-8 15:54
 */
public class Asurion {

    public static void main(String args[]) {

        Asurion asurion = new Asurion();
//        int a[] = new int[]{-1, 7, 3, 2, 4};
        int a[] = new int[]{-1, 7, 3, 2, 4, 3};
        int rs = asurion.equai_2(a);
        System.out.println(rs);


    }

    public int equai_1(int a[]) {
        if (a == null || a.length < 5) return -1;

        for (int i = 0; i < a.length - 2; i++) {
            int leftSum = 0, rightSum = 0;
            for (int j = 0; j < i; j++)
                leftSum += a[j];

            for (int j = i + 1; j < a.length; j++)
                rightSum += a[j];

            if (leftSum == rightSum) return i;
        }

        return -1;
    }

    public int equai_2(int a[]) {
        int left = 0, right = a.length - 1;
        int leftSum = a[left], rightSum = a[right];

        while (left < right-1 && left < a.length - 2 && right > 1) {

            int diff = leftSum - rightSum;
            if (diff > 0) {
                right--;
                rightSum += a[right];
            } else if (diff < 0) {
                left++;
                leftSum += a[left];
            }
            else { //==0
                if(left==right-2) break;
            }

        }
        if (left < a.length - 2) return left + 1;
        else return -1;
    }


}
