package algorithm;

public class FindDigitInNumbers {

    //find how many specified digits are contained in the given 0 to bound sequence
    int find(int bound, final int DIGIT) {

        if (bound / 10 < 1) {
            if (bound < DIGIT)
                return 0;
            else return 1;
        }
        int numberOfDigits = String.valueOf(bound).length();

        //two parts: 0..9999, 10000..bound
        int power10a=power(10,numberOfDigits-1);
        int basicCounter = (bound/power10a) * getBasicCounter(numberOfDigits - 1);

        int extra = bound % power10a;
        int digits[] = getDigits(bound,numberOfDigits);
        //special cases
        if(digits[0]==2){
            basicCounter +=extra+1;
        }
        else if(digits[0]>2){
            basicCounter += power10a;
        }

        int extraCounter = find(extra, DIGIT);
        //System.out.printf("basic:%d,extra:%d \n", basicCounter, extraCounter);
        return basicCounter + extraCounter;
    }

    //up to 9,99,999.
    int getBasicCounter(int numberOfDigits) {
        if (numberOfDigits < 1) return 0;

        int basicCounter = 0;
        for (int i = 0; i < numberOfDigits; i++) {
            if (i == 0) {
                basicCounter = 1;
            } else {
                basicCounter += 9 * i * power(10, i - 1) + power(10, i);
            }
        }
        return basicCounter;
    }

    //123 as {1,2,3}
    int[] getDigits(int n, int numberOfDigits) {
        int[] digits = new int[numberOfDigits];

        for (int i = digits.length-1; i >=0; i--) {
            digits[i] = n % 10;
            n = n / 10;
        }
        return digits;
    }

    int power(int x, int y) {
        return (int) Math.pow(x, y);
    }


    static void printResult(int digit, FindDigitInNumbers finder, int bound) {
        System.out.printf("digit %d occurs:%d times from 0..%d \n\n", digit, finder.find(bound, digit), bound);
    }

    void testGetBasicCounter() {
        System.out.println(getBasicCounter(1));
        System.out.println(getBasicCounter(2));
        System.out.println(getBasicCounter(3));
        System.out.println(getBasicCounter(4));
    }

    public static void main(String args[]) {
        FindDigitInNumbers finder = new FindDigitInNumbers();

//        finder.testGetBasicCounter();

        final int DIGIT = 2;
        printResult(DIGIT, finder, 0);
        printResult(DIGIT, finder, 2);
        printResult(DIGIT, finder, 3);

        printResult(DIGIT, finder, 10);
        printResult(DIGIT, finder, 12);
        printResult(DIGIT, finder, 13);

        printResult(DIGIT, finder, 21);
        printResult(DIGIT, finder, 22);
        printResult(DIGIT, finder, 23);

        printResult(DIGIT, finder, 31);
        printResult(DIGIT, finder, 32);
        printResult(DIGIT, finder, 33);

        printResult(DIGIT,finder,100);
        printResult(DIGIT,finder,111);
        printResult(DIGIT,finder,211);
        printResult(DIGIT,finder,311);

        printResult(DIGIT,finder,121);
        printResult(DIGIT,finder,221);
        printResult(DIGIT,finder,231);

        printResult(DIGIT,finder,212);
        printResult(DIGIT,finder,222);
        printResult(DIGIT,finder,232);

        printResult(DIGIT,finder,213);
        printResult(DIGIT,finder,223);
        printResult(DIGIT,finder,233);

        printResult(DIGIT,finder,311);
        printResult(DIGIT,finder,312);
        printResult(DIGIT,finder,313);

        printResult(DIGIT,finder,321);
        printResult(DIGIT,finder,322);
        printResult(DIGIT,finder,323);

    }
}
