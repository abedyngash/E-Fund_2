# Elimu Fund

This is the an improved version of the Bursary Management system for county bursaries. This version will involve integrating ML techniques to allow automation of the awarding process.

Key modules/Features
1. User modules
 - User roles
	1. Applicant - (Can only apply for bursary)
	2. Staff User - (Can view and edit applications, and also view allocation details)
	3. School User - (A school entity can add disciplinary comments for their students)
	4. Admin User - (Has superuser privileges)

2. Application module
 - Application criteria
 	1. Anyone can apply for bursary
 	2. Applicant records will be used to award or disqualify them

3. Accounting module
 - Features
	1. Admins can add or edit allocation details for different financial years
	2. Money disbursed can be accounted
	3. Admins can access the disbursements generated
	4. The money allocated to every sublocation should not be exceeded during the award process

## Getting Started

Open your terminal in the project directory then run:

```bash
pip install -r requirements.txt
```
You might want to be in a new [virtual environment](https://packaging.python.org/guides/installing-using-pip-and-virtual-environments/) when doing this.

The next step is to start your Database server - (Note that the database used here is POSTGRESQL)

- In linux this is a bit easy:
```bash
service postgresql start
```
- In windows you might want to install PgAdmin

The next step is to create a `.env` file which will contain the variables as follows in the base of your project directory (Same directory as the `manage.py` file).

The email uses SMPT service and the credentials can be found on the service that you choose. Ideally [SendGrid](https://sendgrid.com/)/ Gmail can be used for production, while [Mailtrap](https://mailtrap.io/) is a good candidate for testing emails.
```BASH
DEBUG=True
DB_USER="YOUR_USER_NAME_HERE"
DB_PASSWORD="PASSWORD_HERE"
DB_NAME="DB_NAME_HERE"

EMAIL_HOST="LOOK FOR DOCS ON SERVICE (EG. GMAIL, SENDGRID OR MAILTRAP)"
EMAIL_PORT="DOCUMENTED ON SERVICE"
EMAIL_USER="USER FOR SERVICE ACCOUNT"
EMAIL_PASSWORD="PASSWORD FOR SERVICE ACCOUNT"
```

with that you can now start your server:

```bash
python manage.py runserver
```

## Adding First Super User
Almost a mandatory step if you want to access the [admin](http://127.0.0.1:8000/admin) site.
This is easily done by:

1. Running your migrations to create your database tables:

	```bash
	python manage.py migrate
	```
	Then

2. Creating your superuser through the python shell

	```bash
	python manage.py createsuperuser
	```
	And BOOM! You can access the admin site and/or access your superuser privileges

	On a successful setup you should get something like this when logged in as a super user:

	![dashboard](https://user-images.githubusercontent.com/30406704/61175579-c5a5fa80-a5ba-11e9-8652-6c0455b129d7.png)

	And this when not logged in:
	![guest](https://user-images.githubusercontent.com/30406704/61175712-aa3bef00-a5bc-11e9-8ae8-702be2991aec.png)

3. Populate the database with default values/fixtures located in `fixtures` directory.
	Refer to this [video](https://www.youtube.com/watch?v=3ryK7e7mFJE) for demo example.
	```BASH
	python manage.py loaddata fixtures/{name of fixture.ext}
	```