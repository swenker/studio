package algorithm;


public class CalLineDistance {

    static class Line {
        int start;
        int end;

        Line(int start, int end) {
            this.start = start;
            this.end = end;
        }
    }

    /**
     * note: start of line is in ascend order
     */
    public int calLineDistance(Line[] lines) {
        int sum = 0;

        Line lastValid = null;
        for (Line currentLine : lines) {
            if (currentLine == null) continue;

            if (lastValid == null) {//first
                sum += currentLine.end - currentLine.start;
            } else {
                if (currentLine.end <= lastValid.end)
                    continue;

                else if(currentLine.start<=lastValid.end)
                    sum += currentLine.end-lastValid.end;
                else
                    sum += currentLine.end-currentLine.start;
            }
            lastValid = currentLine;

        }
        return sum;
    }

    public static void main(String args[]) {
        Line[]lines = {new Line(1,10),new Line(5,7),new Line(6,15),new Line(15,16),new Line(17,18) };
        CalLineDistance cal = new CalLineDistance();
        System.out.println(cal.calLineDistance(lines));
    }
}
