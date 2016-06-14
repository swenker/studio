
import java.awt.*;

/**
 * @author : Sun Wenju
 *         Date: Apr 5, 2008 2:19:08 PM
 *         text stamp added to image
 * sample font:new Font("Times New Roman", Font.PLAIN, 18)
 */
public class TextStamp {
    /**
     * text used to as stamp
     * */
    private String text;
    private Font font;

    public TextStamp(String text, Font font) {
        this.text = text;
        this.font = font;
    }

    public String getText() {
        return text;
    }

    public void setText(String text) {
        this.text = text;
    }

    public Font getFont() {
        return font;
    }

    public void setFont(Font font) {
        this.font = font;
    }
}
