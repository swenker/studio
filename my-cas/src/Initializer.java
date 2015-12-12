import org.springframework.session.web.context.AbstractHttpSessionApplicationInitializer;

/**
 * Created by wenjusun on 12/3/2015.
 */
public class Initializer extends AbstractHttpSessionApplicationInitializer { // <1>
//public class Initializer{ // <1>

    public Initializer() {
        super(Config.class);
    }
}