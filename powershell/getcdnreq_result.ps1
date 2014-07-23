
#get content of the given file and parsed the string.
#  0#OK-zipreq:22897,31716,54613

$Status_File="d:\scripts\output\cdnreq.status"

$STATE_UNKNOWN=3 
$exit_code=$STATE_UNKNOWN

$fileStatus=Test-Path $Status_File

if(-not $fileStatus) 
{ 
     logit "$Status_File not exist,exit now"
     exit 1
}     

$fcontent=Get-Content -Path $Status_File 

Write-Output $fcontent.substring(2) 
$exit_code =$fcontent.substring(0,1) 

exit $exit_code





