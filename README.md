# townhallbackend
Backend Django server using DRF


Following the set up of
https://medium.com/swlh/build-your-first-rest-api-with-django-rest-framework-e394e39a482c
If you can't access the article, just follow the instructions below

Install Dependencies

Step1
First you need to install python and pip:
https://www.python.org/downloads/
https://pip.pypa.io/en/stable/installation/

Step2
Then once you have it installed, run the following command in your Terminal (in vscode click "New Terminal" on the top tabs)
`pip install django` then `pip install djangorestframework`

Step2.5: run migrations
To run migrations:
`python manage.py migrate`
![alt text](image.png)

Step2.6: setup pre-commit (linter checks before commiting to git)
Run `pip install pre-commit`, then `pre-commit install`.
Afterwards, `flake8` and `black` will be run every time before commiting.

Step3
Run the following command to make superuser, ensure you have `cd townhall` and gone in the townhall subdirectory
`python manage.py createsuperuser`
username: townhall
pw: townhall 
if it asks for email, just type your persona email 
if you dont see the password youre writing being typed out, THAT IS OK, the text you are writing when setting your password is purposefully invisible, just don't make any typos! 



Step4: run the server
To run the server: 
`python manage.py runserver`
![alt text](image-1.png)

Step5: checking if server is running
To check if your server is running, navigate to http://localhost:8000/admin/ or http://localhost:8000/

Read the linked medium article or ping Ansel if there are any questions. 

To run tests from the `tests.py` file, run the command `python manage.py tests` 
This will run all tests in the file and show how many succeeded or failed

If at any point you have migrations that need to be applied, run the following
`python manage.py migrate`
