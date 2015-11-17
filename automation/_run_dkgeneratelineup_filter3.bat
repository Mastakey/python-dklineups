set mydate=%DATE:~10,4%-%DATE:~4,2%-%DATE:~7,2%
cd C:\local\python\27\dklineups\
C:\local\python\27\venv\Scripts\python.exe dkgeneratelineup_filter3.py %mydate% > C:\local\python\27\dklineups\out\%mydate%filter3.csv
%SystemRoot%\explorer.exe C:\local\python\27\dklineups\out\
PAUSE