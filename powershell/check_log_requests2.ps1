#check log request
param (
  [int]    $w = 1000,
  [int]    $c = 2000,
  [string] $k = "zip"
)

$min=0
$max=10000
$STATE_OK=0
$STATE_WARNING=1
$STATE_CRITICAL=2
$STATE_UNKNOWN=3 

$VALVE_WARN=$w
$VALVE_CRITICAL=$c                 
$KeyString=$k

$zipAll=0
$zipBack=0
$zipIMS=0

#Write-Host "$VALVE_WARN,$VALVE_CRITICAL,$KeyString"

function logit([string]$loginfo)
{    
  $curentTime=[DateTime]::Now.toString("yyyy-MM-dd HH:mm:s`s")  
  $logString="$curentTime - $loginfo"
  echo "$logString"
}

 
$today=[DateTime]::Now.ToString('yyMMdd')

$Log_File="D:\log\inetpub\W3SVC2\U_in$today*"
#$LOG_File="D:\work\log\u_in140331.log"
$TMP_Log_Files="D:\roller\tmp\$today*"

$fileStatus=Test-Path $Log_File

if(-not $fileStatus) 
{ 
     logit "$Log_File not exist,exit now"
     exit 1
}     

#zipAll
$status = Select-String -path $Log_File $KeyString | Measure-Object -line
$zipAll = $status.Lines


#request for IMS (304 status code)
$status = Select-String -path $Log_File $KeyString | Select-String ' 304,'| Measure-Object -line
$zipIMS = $status.Lines



#logit '---$status.Lines'       

$exit_code=$STATE_UNKNOWN
$zipBack =$zipAll - $zipIMS

if ($zipBack -lt $VALVE_WARN)
{
   Write-Output ("OK-zipreq:$zipBack,$zipIMS,$zipAll|'zipBack'=$zipBack")
   $exit_code =$STATE_OK 
}   
elseif ($zipBack -ge $VALVE_WARN -and $zipBack -lt $VALVE_CRITICAL)      
{
   Write-Output "WARN-zipreq:$zipBack,$zipIMS,$zipAll|'zipBack'=$zipBack"
   $exit_code =$STATE_WARNING 
}
elseif ($zipBack -ge  $VALVE_CRITICAL)  
{
   Write-Output "Critical-zipreq:$zipBack,$zipIMS,$zipAll|'zipBack'=$zipBack"
   #Write-Output "Critical-zipreq:$zipBack,$zipIMS,$zipAll|'zipBack'=$zipBack;$w;$c"
   $exit_code =$STATE_CRITICAL  
}

exit $exit_code



