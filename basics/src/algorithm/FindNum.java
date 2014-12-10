package algorithm;

public class FindNum {

    void bubbleSort(int a[]) {
        if (a != null && a.length > 1) {

            for (int i = 0; i < a.length; i++) {
                for (int j = i + 1; j < a.length; j++) {
                    int min = a[i];
                    if (a[j] < min) {
                        a[i] = a[j];
                        a[j] = min;
                    }
                }
            }
        }
    }

    //based on bubble sort
    int findMaxK(int a[], int k) {
        if (a == null || a.length < 1 || a.length < k)
            return -1;
        else {
            if (k <= a.length / 2) {
                //ascend
                for (int i = 0; i < k; i++) {
                    for (int j = i + 1; j < a.length; j++) {
                        int min = a[i];
                        if (a[j] < min) {
                            a[i] = a[j];
                            a[j] = min;
                        }
                    }
                }
                return a[k - 1];
            } else {
                //descend
                for (int i = 0; i < a.length - k + 1; i++) {
                    for (int j = i + 1; j < a.length; j++) {
                        int max = a[i];
                        if (a[j] > max) {
                            a[i] = a[j];
                            a[j] = max;
                        }
                    }
                }
                return a[a.length - k];
            }

        }

    }

    static void printArray(int a[]) {
        for (int i : a) {
            System.out.print(i);
            System.out.print(" ");
        }

    }

    public static void main(String args[]) {
//        int a[] = {3, 5, 4, 2, 6, 1, 8, 9,7};
        int a[] = {3, 2, 1};

        FindNum findNum = new FindNum();

        //k :1..a.length
        int numK = findNum.findMaxK(a, 10);
        System.out.println(numK);
        printArray(a);
    }
}
