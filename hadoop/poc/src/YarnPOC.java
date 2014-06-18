
import org.apache.commons.logging.Log;
import org.apache.commons.logging.LogFactory;
import org.apache.hadoop.conf.Configuration;
import org.apache.hadoop.fs.FileStatus;
import org.apache.hadoop.fs.Path;
import org.apache.hadoop.net.NetUtils;
import org.apache.hadoop.security.SecurityInfo;
import org.apache.hadoop.yarn.api.ApplicationClientProtocol;
import org.apache.hadoop.yarn.api.ApplicationConstants;
import org.apache.hadoop.yarn.api.protocolrecords.GetNewApplicationRequest;
import org.apache.hadoop.yarn.api.protocolrecords.GetNewApplicationResponse;
import org.apache.hadoop.yarn.api.protocolrecords.SubmitApplicationRequest;
import org.apache.hadoop.yarn.api.records.*;
import org.apache.hadoop.yarn.conf.YarnConfiguration;
import org.apache.hadoop.yarn.security.client.ClientRMSecurityInfo;
import org.apache.hadoop.yarn.util.ConverterUtils;
import org.apache.hadoop.yarn.util.Records;

import java.net.InetSocketAddress;
import java.util.ArrayList;
import java.util.HashMap;
import java.util.List;
import java.util.Map;

/**
 * Created with IntelliJ IDEA.
 * User: samsung
 * Date: 14-4-8
 * Time: 下午1:38
 * To change this template use File | Settings | File Templates.
 */


public class YarnPOC {
    Log log = LogFactory.getLog(getClass());

    public static void main(String args[]) {

        YarnPOC ypoc = new YarnPOC();


    }


    public void yarnCall() throws Exception {
        ApplicationClientProtocol applicationsManager;
        YarnConfiguration yarnConf = new YarnConfiguration(conf);

        InetSocketAddress rmAddress = NetUtils.createSocketAddr(yarnConf.get(YarnConfiguration.RM_ADDRESS, YarnConfiguration.DEFAULT_RM_ADDRESS));

        log.info("Connecting to ResourceManager at " + rmAddress);
        Configuration appsManagerServerConf = new Configuration(conf);
        appsManagerServerConf.setClass(YarnConfiguration.YARN_SECURITY_INFO, ClientRMSecurityInfo.class, SecurityInfo.class);
        applicationsManager = ((ApplicationClientProtocol) rpc.getProxy(ApplicationClientProtocol.class, rmAddress, appsManagerServerConf));


        GetNewApplicationRequest request = Records.newRecord(GetNewApplicationRequest.class);

        GetNewApplicationResponse response = applicationsManager.getNewApplication(request);
        LOG.info("Got new ApplicationId=" + response.getApplicationId());


        //submit application
        ApplicationId appId = response.getApplicationId();
        ApplicationSubmissionContext applicationSubmissionContext = Records.newRecord(ApplicationSubmissionContext.class);

        applicationSubmissionContext.setApplicationId(appId);
        applicationSubmissionContext.setApplicationName("appname");

        ContainerLaunchContext containerLaunchContext = Records.newRecord(ContainerLaunchContext.class);

        Map<String, LocalResource> localResourceMap = new HashMap<String, LocalResource>();
        Path jarPath;

        FileStatus jarStatus = fs.getFileStatus(jarPath);

        LocalResource amJarRsrc = Records.newRecord(LocalResource.class);
        amJarRsrc.setType(LocalResourceType.FILE);
        amJarRsrc.setVisibility(LocalResourceVisibility.APPLICATION);
        amJarRsrc.setResource(ConverterUtils.getYarnUrlFromPath(jarPath));
        amJarRsrc.setTimestamp(jarStatus.getModificationTime());
        amJarRsrc.setSize(jarStatus.getLen());

        containerLaunchContext.setLocalResources(localResourceMap);

        Map<String, String> env = new HashMap<String, String>();
        String classPathEnv = "$CLASSPATH:./*:";
        env.put("CLASSPATH", classPathEnv);
        containerLaunchContext.setEnvironment(env);
        String command = "${JAVA_HOME}" + "/bin/java" + " MyAppMaster" + " arg1 arg2 arg3" +
                " 1>" + ApplicationConstants.LOG_DIR_EXPANSION_VAR + "/stdout" +
                " 2>" + ApplicationConstants.LOG_DIR_EXPANSION_VAR + "/stderr";

        List<String> commands = new ArrayList<String>();
        commands.add(command);

        containerLaunchContext.setCommands(commands);

        Resource capability = Records.newRecord(Resource.class);
        capability.setMemory(100);
        containerLaunchContext.setResource(capability);

        applicationSubmissionContext.setAMContainerSpec(containerLaunchContext);

        SubmitApplicationRequest applicationRequest = Records.newRecord(SubmitApplicationRequest.class);

        applicationRequest.setApplicationSubmissionContext(applicationSubmissionContext);
        applicationsManager.submitApplication(applicationRequest);

    }


}
