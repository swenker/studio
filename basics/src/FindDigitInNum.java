
public class FindDigitInNum {

    int countAll2InNumbers(int n) {
        int numberWidth = String.valueOf(n).length();
        int counter = 0;

        //occurrence times on every position
        for (int i = 0; i < numberWidth; i++) {
            int powOf10 = (int) Math.pow(10, i);
            int nextPowOf10 = powOf10 * 10;

            int low = n - n % nextPowOf10;
            int high = low + nextPowOf10;

            int currentDigit = (n / powOf10) % 10;

            if (currentDigit < 2) {
                counter += low / 10;
            } else if (currentDigit == 2) {
                int numberOnRight = n % powOf10;
                counter += low / 10 + numberOnRight + 1;

            } else {
                counter += high / 10;
            }
        }
        return counter;
    }

    static void printResult(FindDigitInNum finder, int bound) {
        System.out.printf("digit %d occurs:%d times from 0..%d \n", 2, finder.countAll2InNumbers(bound), bound);
    }

    public static void main(String args[]) {
        FindDigitInNum finder = new FindDigitInNum();

/*
        printResult(finder,0);
        printResult(finder,1);
        printResult(finder,2);
        printResult(finder,11);
        printResult(finder,12);
        printResult(finder,20);
        printResult(finder,220);
*/
/*
        printResult(finder,10);
        printResult(finder,100);
        printResult(finder,1000);
        printResult(finder,10000);
*/
        printResult(finder, 100);
        printResult(finder, 1413);
        printResult(finder, 3321);
        printResult(finder, 111);
        printResult(finder, 211);
        printResult(finder, 311);

        printResult(finder, 121);
        printResult(finder, 221);
        printResult(finder, 231);

        printResult(finder, 212);
        printResult(finder, 222);
        printResult(finder, 232);

        printResult(finder, 213);
        printResult(finder, 223);
        printResult(finder, 233);

        printResult(finder, 311);
        printResult(finder, 312);
        printResult(finder, 313);

        printResult(finder, 321);
        printResult(finder, 322);
        printResult(finder, 323);

    }
}
