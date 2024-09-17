@echo off

set _debug_=

for /f "tokens=1-2 delims=: " %%a in ('time /t') do set _hhmm_=%%a%%b

if "%1"=="%_hhmm_%" goto :continue

echo.
echo Please supply the current time: %_hhmm_%
echo.

goto :end

:continue
echo.
echo --------------------------------------------------------------------------
echo removing db
echo.
%_debug_% del instance\divescheduling.db
echo --------------------------------------------------------------------------
echo run reinit_db.py
echo.
%_debug_% python reinit_db.py
echo --------------------------------------------------------------------------
echo python run.py
echo.
%_debug_% python run.py
echo.
echo Finished...
echo --------------------------------------------------------------------------
echo.

:end
