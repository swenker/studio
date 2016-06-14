
/**
 * @author : Sun Wenju
 *         Date: Apr 5, 2008 2:31:24 PM
 */
public class RenderSpecification {
    public static final String SIZE_TYPE_WIDTH = "width";
    public static final String SIZE_TYPE_HEIGHT = "height";

    public static final String IMAGE_TYPE_JPEG = "JPEG";
    public static final String IMAGE_TYPE_GIF = "GIF";


    private String sizeType;
    private String imageType;

    /**
     * size of this dimension
     * */
    private int size;
    /**
     * larger than 0 and less than or equal 1,if it's null,the deault value is 0.75<br/>
     * which is determined by the implementation
     * */
    private Float quality;


    public RenderSpecification(String type, int size, Float quality) {
        this.sizeType = type;
        this.size = size;
        this.quality = quality;
    }

    public String getSizeType() {
        return sizeType;
    }

    public void setSizeType(String sizeType) {
        this.sizeType = sizeType;
    }

    public String getImageType() {
        return imageType;
    }

    public void setImageType(String imageType) {
        this.imageType = imageType;
    }

    public int getSize() {
        return size;
    }

    public void setSize(int size) {
        this.size = size;
    }

    public Float getQuality() {
        return quality;
    }

    public void setQuality(Float quality) {
        this.quality = quality;
    }
}
