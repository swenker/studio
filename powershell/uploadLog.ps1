#upload log file to remote server

function logit([string]$loginfo)
{    
  $curentTime=[DateTime]::Now.toString("yyyy-MM-dd HH:mm:ss")  
  $logString="$curentTime - $loginfo"
  out-file -append -filepath d:\roller\das.log   -inputobject $logString 
  echo "$logString"
}

 
$yesterday=[DateTime]::Now.AddDays(-1).ToString('yyyyMMdd')
$localServerName=cmd /c hostname

$Log_File="D:\log\api\Log\LogInfo\$yesterday*"
$TMP_Log_Files="D:\roller\$yesterday*"
$baseZippedName="d:\roller\$localServerName"+"_"+"$yesterday"
$allZippedLogfile="d:\roller\$localServerName"+"_"+"$yesterday*.zip"

logit "---------log collector started abcdefg-------------"

$fileStatus=Test-Path $Log_File

if(-not $fileStatus) 
{ 
     logit "$Log_File not exist,exit now"
     return
}     


function Add-Zip([string]$baseZipName)
{
    
    $shellApplication = new-object -com shell.application

    $i=0
    foreach($file in $input) 
    {
       try
       {
        $i=$i+1        
        $finalZipName="$baseZipName"+"$i"+".zip" 
        if(test-path($finalZipName))
        {
            logit "$finalZipName already exists,delete it...... "
            Remove-Item  $finalZipName        
        }
    
        #create the target empty zip file 
        if(-not (test-path($finalZipName)))
        {
            set-content $finalZipName ("PK" + [char]5 + [char]6 + ("$([char]0)" * 18))
            (dir $finalZipName).IsReadOnly = $false        
        }
        
        $zipPackage = $shellApplication.NameSpace($finalZipName)
        $zipPackage.CopyHere($file.FullName)        
        logit "$finalZipName created."
        
        Start-sleep -milliseconds 60000
        
        Remove-Item $file.FullName        
        logit "remove the temporary file:$file"
      }Catch [Exception]{
          logit "any other undefined errors"
          logit $error[0]
        }
          
    }
}

function Upload-Log ([string]$logfile)
{

    if(-not (test-path($logfile)))
    {
        logit "$logfile doesn't exist!"
    }
    else
    {
        $targetPath="/home/clog/mcilog"
        $pscpPath="D:\roller\pscp"
        
        try{
          $execArgs=" -pw nov4096  $logfile clog@das.svc.mscc.cn:$targetPath"
          $status = & $pscpPath $execArgs.Split()     
          logit "---$status"       
        }Catch {
          logit "any other undefined errors"
          logit $error[0]
        }

    }        
}

logit "starting copying log file"
copy-item $Log_File -destination D:\roller\
$tmp_file_list= dir $TMP_Log_Files
logit "copied log files:$tmp_file_list"

logit "starting zipping file"
dir $TMP_Log_Files | Add-Zip $baseZippedName
logit "file zipped"

logit "starting upload log"
Upload-Log $allZippedLogfile

Start-sleep -milliseconds 10000
logit "log uploaded "



