package algorithm;

/**
 * Created with IntelliJ IDEA.
 * User: samsung
 * Date: 14-11-21
 * Time: 上午8:33
 * To change this template use File | Settings | File Templates.
 */
public class DynamicProgramming {
    public static void main(String args[]) {

        DynamicProgramming dp = new DynamicProgramming();

        dp.test1();

    }


    public void maxSub() {
        int[]a = {1,2,5};
        int []k = new int[a.length];
        int target = 10;

        for(int i = 0;i<a.length;i++){
            k[i] = target/a[i];
        }

    }


    //give coins and print the subsequence summed to 10.
    public void countCoins() {
        int[] coins = {1, 2, 5};


    }

    public void test1() {
        String s = "a b c c d x f g g g h a";

        char ca[] = s.toCharArray();

        StringBuffer sb = new StringBuffer();
        boolean hasLeft = false;

        if (ca[2] == ca[0]) {
            sb.append('(');
            hasLeft = true;
        }
        sb.append(ca[0]);

        int i = 1, j = i + 2;
        for (; j < ca.length; ) {
            if (sb.charAt(sb.length() - 1) == ')' && ca[i] == ' ') {
                i++;
                j++;
                continue;
            }

            sb.append(ca[i]);

            if (ca[i] != ' ') {
                if (ca[j] == ca[i]) {
                    if (hasLeft) {
                        i += 1;
                        j += 1;

                        continue;
                    } else {
                        sb.replace(sb.length() - 2, sb.length() - 1, "(");
                        hasLeft = true;
                    }

                } else {
                    if (hasLeft) {
                        sb.append(')');
                        hasLeft = false;
                    }
                }
                i += 1;
                j += 1;

            } else {
                i += 1;
                j += 1;
            }
        }

        sb.append(ca[j - 2]);
        sb.append(ca[j - 1]);
        if (hasLeft)
            sb.append(")");
        System.out.println(s);
        System.out.println(sb.toString());

    }

    public void test2() {
        String s = "a b c c d x f g g g h a";

        char ca[] = s.toCharArray();

        char[] r = new char[ca.length + 2];
        boolean has = false;
        int k = 0;
        if (ca[2] == ca[0]) {
            r[k] = '(';
            has = true;
            k++;
        }
        r[k] = (ca[0]);
        int i = 1, j = i + 2;
        for (; j < ca.length; ) {
            if (r[k - 1] == ')' && ca[i] == ' ') {
                i++;
                j++;
                continue;
            }
            r[++k] = ca[i];

            if (ca[i] != ' ') {
                if (ca[j] == ca[i]) {
                    if (has) {
                        i += 1;
                        j += 1;

                        continue;
                    } else {
                        r[k - 1] = '(';
                        has = true;
                    }

                } else {
                    if (has) {
                        r[++k] = ')';
                        has = false;
                    }
                }
                i += 1;
                j += 1;

            } else {
                i += 1;
                j += 1;
            }
        }

        r[++k] = ca[j - 1];
        if (has)
            r[++k] = ')';
        System.out.println(s);
        System.out.println(new String(r));

    }
}
