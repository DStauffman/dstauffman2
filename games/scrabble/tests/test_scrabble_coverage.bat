cd C:\Users\%username%\Documents\GitHub\dstauffman2\games\scrabble\tests

coverage run  --rcfile=C:\Users\%username%\Documents\GitHub\dstauffman2\tests\.coveragerc run_all_tests.py
coverage html --rcfile=C:\Users\%username%\Documents\GitHub\dstauffman2\tests\.coveragerc
start C:\Users\%username%\Documents\GitHub\dstauffman2\games\scrabble\tests\coverage_html_report\index.html

echo 'Press any key to continue'
pause
