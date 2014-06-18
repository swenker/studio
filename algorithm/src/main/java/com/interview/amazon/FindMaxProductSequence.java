package com.interview.amazon;

/**
 * User: gjkv86
 * Date: 13-4-7 00:41
 */
public class FindMaxProductSequence {
    public static void main(String args){
        FindMaxProductSequence maxProductSequence=new FindMaxProductSequence();

        int a[]=new int[]{6,7,8,1,2,3,9,10};
        maxProductSequence.getResult(a);

    }

    /**
     * Given a sequence of non-negative integers find a subsequence of length 3 having maximum product with the numbers of the subsequence being in ascending order.
     Example:
     Input: 6 7 8 1 2 3 9 10
     Output: 8 9 10
     The subsequence has to be in ascending order. Consider {4, 7, 9, 8, 2} as your input.
     In this case, the three max numbers are {7, 9, 8} but this isn't a valid subsequence. The output in this case should be {4, 7, 9}
     * */
    public void getResult(int []a){

    }
}
