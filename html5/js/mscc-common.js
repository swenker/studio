
//get params from current url
function gup( name ){
  name = name.replace(/[\[]/,"\\\[").replace(/[\]]/,"\\\]");
  var regexS = "[\\?&]"+name+"=([^&#]*)";
  var regex = new RegExp( regexS );
  var results = regex.exec( window.location.href );
  if( results == null )
    return "";
  else
    return results[1];
}

//There is a dedicated server for production
var checkinService="http://vpck.svc.mcitech.cn/3mini/wx";
var currentDomain=window.location.hostname;

if (currentDomain!="dl-mas-oss.svc.mcitech.cn") {
    checkinService="http://checkin.qasvc.mcitech.cn/3mini/wx";
}
 
var pk=gup("pk");
var sc=gup("sc");
if (sc==null || sc=="") {
    sc="qr1";
}

var site="minisite";
var timewait=100;

var checkin=function(page,op){    
    document.getElementById("img-cph").src=checkinService+"?sc="+sc+"&site="+site+"&page="+page+"&op="+op+"&pk="+pk;
}

var click_download=function(page){
    checkin(page,"download");
    //window.open('http://223.6.251.186/content-deliverer-1.0/rs/appdl/sm/121',"_new");
    //alert("download");
    setTimeout(function(){
        window.location="http://223.6.251.186/content-deliverer-1.0/rs/appdl/sm/121";
    },timewait);
    return false;
}

var click_trial=function(page){
    //checkin(page,"trial");
    //setTimeout(function(){
        window.location="http://"+currentDomain+"/mini/3m/weikan/index.html"+"?sc="+sc+"&pk="+pk;
    //},timewait);
    return false;
}

var click_video=function(page){
    checkin(page,"video");
    //setTimeout(function(){
    //    window.location="http://dl-mas-oss.svc.mcitech.cn/mini/3m/video/3m_TabS_0723final.mp4";
    //},timewait);

}
