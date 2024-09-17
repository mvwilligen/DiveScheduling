@echo off

c:
cd data\Python\DiveScheduling

rem 0:mwi:20:source M-> 1:mwi20:_backups_ M-> 2:mwi20:onedrive A-> 3:cloud:onedrive A-> 4:local:nas01 M-> 5:local:nas02

set comment=_savepoint
if not "%1"=="" set comment=_%1

for /f "tokens=1-4 delims=-/ " %%a in ('date /t') do set _yyyymmdd_=%%c%%b%%a
for /f "tokens=1-2 delims=: "  %%a in ('time /t') do set _hhmm_=%%a%%b
for /f "tokens=1-2 delims=: "  %%a in ('time /t') do set _hh_=%%a
for /f "tokens=3   delims=:, " %%a in ("%time%")  do set _ss_=%%a

set folder=C:\Data\Python\DiveScheduling
set folder2=%folder%\Export2Website\%_yyyymmdd_%_%_hhmm_%%comment%

echo.
echo date:%_yyyymmdd_% time:%_hhmm_% hour:%_hh_% sec:%_ss_%
echo folder:%folder%
echo folder2:%folder2%
echo.

if not exist %folder%\Export2Website      md %folder%\Export2Website
if not exist %folder2%                    md %folder2%
if not exist %folder2%\Package            md %folder2%\Package
if not exist %folder2%\Package\templates  md %folder2%\Package\templates
if not exist %folder2%\instance           md %folder2%\instance
if not exist %folder2%\Package\static             md %folder2%\Package\static
if not exist %folder2%\Package\static\images      md %folder2%\Package\static\images

copy %folder%\*.py                        %folder2%
copy %folder%\*.env                       %folder2%
copy %folder%\Package\*.py                %folder2%\Package
copy %folder%\Package\templates\*.html    %folder2%\Package\templates
copy %folder%\instance\*.db               %folder2%\instance
copy %folder%\instance\*.txt              %folder2%\instance
copy %folder%\instance\*.png              %folder2%\instance
copy %folder%\Package\static\images\*.png %folder2%\Package\static\images
copy %folder%\Package\static\images\*.ico %folder2%\Package\static\images

set zipfile=C:\Data\Python\_Backups_\DiveScheduling_Export_%_yyyymmdd_%_%_hhmm_%%comment%.zip

c:\data\utils\7z.exe a -r %zipfile% %folder2%

copy %zipfile% C:\Users\mvwil\OneDrive\Backups\MWI20\DiveScheduling

dir %folder2%
