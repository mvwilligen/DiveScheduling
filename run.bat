@echo off

rem linux: source env/bin/activate
call C:\Data\Python\DiveScheduling\env\Scripts\activate.bat

for /f %%a in (.env) do set %%a

flask --app Package run --host=0.0.0.0 --debug --port=8080
