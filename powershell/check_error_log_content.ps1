#check log content to get if there is something with the given keyword

$STATE_OK=0
$STATE_WARNING=1
$STATE_CRITICAL=2
$STATE_UNKNOWN=3 
$exit_code=$STATE_UNKNOWN

$today=[DateTime]::Now.ToString('yyyyMMdd')

$Log_File="D:\log\api\Log\LogError\$today*"

$KeyString="mysql"

$fileStatus=Test-Path $Log_File

if(-not $fileStatus) 
{ 
     #Write-Output "$Log_File not exist,exit now"
     Write-Output ("OK-Log_File not exist:0|'mysql_kc'=0")
     exit 0
}     

$status = Select-String -path $Log_File $KeyString | Measure-Object -line
$KC = $status.Lines

if($KC -lt 1) 
{
   Write-Output ("OK-mysql:$KC|'mysql_kc'=$KC")
   $exit_code =$STATE_OK 
}
elseif($KC -gt 0)
{
   Write-Output ("Critical-mysql:$KC|'mysql_kc'=$KC")
   $exit_code =$STATE_CRITICAL 
}

exit $exit_code

