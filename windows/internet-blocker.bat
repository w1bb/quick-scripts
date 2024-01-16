@setlocal enableextensions 
@cd /d "[INSERT PATH HERE]"
@cls
@echo Here is a list of the files that will be modified:
@for /R %%f in (*.exe) do @ (
	echo - %%f
)
@ echo.

:confirm
@set /p DUMMY=Type Y to proceed or N to cancel. 
@if %DUMMY% == Y goto startjob
@if %DUMMY% == N goto canceljob
@goto confirm

:startjob
@echo.
@for /R %%f in (*.exe) do @ (
 	echo Altering %%f
	netsh advfirewall firewall add rule name="Blocked: %%f" dir=in program="%%f" action=block
	netsh advfirewall firewall add rule name="Blocked: %%f" dir=out program="%%f" action=block
)
@goto end

:canceljob
@echo.
@echo No rule was added.
@goto end


:end
@pause
@echo.
