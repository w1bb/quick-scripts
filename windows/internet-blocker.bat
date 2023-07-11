@ setlocal enableextensions 
@ cd /d "[INSERT PATH HERE]"

for /R %%f in (*.exe) do (
  netsh advfirewall firewall add rule name="Blocked: %%f" dir=in program="%%f" action=block
  netsh advfirewall firewall add rule name="Blocked: %%f" dir=out program="%%f" action=block
)

pause
