package opensource;

import org.apache.http.conn.ClientConnectionManager;
import org.apache.http.impl.conn.tsccm.ThreadSafeClientConnManager;


/**
 * Created with IntelliJ IDEA.
 * User: samsung
 * Date: 14-6-23
 * Time: 上午11:41
 * To change this template use File | Settings | File Templates.
 */
public class HttpComponents {

    public static void main(String args[]){

    }

    public void hc41(){

        ThreadSafeClientConnManager ccm = new ThreadSafeClientConnManager();
//        ccm.setMaxTotal();
    }

}
