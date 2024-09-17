@echo off

for /f %%a in (.env) do set %%a

flask --app Package run --host=0.0.0.0 --debug 
