# Installation guide
## Table of contents
1. [For Windows](#windows)
2. [For MacOS](#mac-os)
3. [For Linux machine](#linux)
4. [Testing](#testing-the-application)
5. [Installation notes](#installation-notes)

## Windows
> Notice: Please make sure that you have ```git``` installed in your machine.
### Using a prewritten script
1. Make sure that you have Python 3.11 installed on your machine. You can download it from [Microsoft Store](https://www.microsoft.com/store/productId/9NRWMJP3717K?ocid=pdpshare).
2. Open ```Command Prompt``` (Powershell is not recommended)
3. Download the repository by running the following command.
```sh
git clone https://github.com/PichapopRo/project-pantry
```
4. Execute the script file ```project-pantry/installation/windows.bat```.
```sh
cd project-pantry
call installation/windows.bat
```
### Manually
1. Open ```Command Prompt``` (Powershell is not recommended)
2. Download the repository by running the following command.
```sh
git clone https://github.com/PichapopRo/project-pantry
```
3. Make sure that you have Python 3.11 installed in your machine. You can download it from [Microsoft Store](https://www.microsoft.com/store/productId/9NRWMJP3717K?ocid=pdpshare).
4. Install Python Virtual Environment.
```sh
cd project-pantry
py -3.11 -m venv venv
```
5. Install requirement packages.
```sh
call venv/Scripts/activate
python -m pip install -r requirements.txt
```
6. Initialize Django
```sh
python manage.py migrate
```
7. Initialize ```.env``` file. The following script will automatically create a .env file and generate a Django secret key for you.
```sh
python -c "from django.core.management.utils import get_random_secret_key; f = open('.env', 'w'); f.write('SECRET_KEY=django-insecure-'+get_random_secret_key()+'\n'); f.close()"
echo API_USERNAME= 'Spoonacular'
echo DEBUG=False
echo TIME_ZONE = Asia/Bangkok
echo ALTER_PROMT = 'You are a chef embedded inside a recipe-viewing program. You are here to give the alternative ingredient to the users. Answer the question in this JSON format strictly:[{"name":"The ingredient name","description":"The description of the ingredient","amount":number,"unit":"The unit of the amount"},{"name":"The ingredient name","description":"The description of the ingredient","amount":number,"unit":"The unit of the amount"},...]'
echo DIFF_PROMPT = 'You are a chef embedded inside a recipe-viewing program. You are here to give a difficulty for each recipe based on techniques used, steps, ingredient and preparation. Answer strictly only "Hard", "Normal" and "Easy".'
echo APPROVAL_PROMPT = 'You are a chef embedded inside a recipe-viewing program. You are here to review recipes that was uploaded by user based on possibility and eatable. Answer strictly only in boolean (True or False). True means the recipe is possible and eatable. False means it is impossible to make and not eatable.'
echo NUTRITION_PROMPT = 'You are a chef embedded inside a recipe-viewing program. You are here to give nutrition information based on ingredients. Answer strictly only in this JSON format: {"nutrients":[{"name":"Calories","amount":316.49,"unit":"kcal","percentOfDailyNeeds":15.82},{"name":"Fat","amount":12.09,"unit":"g","percentOfDailyNeeds":18.6},{"name":"Saturated Fat","amount":3.98,"unit":"g","percentOfDailyNeeds":24.88},{"name":"Carbohydrates","amount":49.25,"unit":"g","percentOfDailyNeeds":16.42},{"name":"Net Carbohydrates","amount":46.76,"unit":"g","percentOfDailyNeeds":17.0},{"name":"Sugar","amount":21.98,"unit":"g","percentOfDailyNeeds":24.42},{"name":"Cholesterol","amount":1.88,"unit":"mg","percentOfDailyNeeds":0.63},{"name":"Sodium","amount":279.1,"unit":"mg","percentOfDailyNeeds":12.13},{"name":"Protein","amount":3.79,"unit":"g","percentOfDailyNeeds":7.57}, ...]}'
echo CHEF_BADGE_APPROVED = 10
echo DJANGO_LOG_LEVEL = DEBUG
```
8. Open ```.env``` file to put your own API_KEY, SPOONACULAR_PASSWORD, SECRET_KEY, OPENAI_APIKEY, IMGUR_CLIENT_ID, DB_PASSWORD, DB_USERNAME, DB_NAME, ALLOWED_HOSTS, and LINK_URL. Look at ```sample.env``` file for an example.

## Mac OS
> Notice: Please make sure that you have ```git``` installed in your machine.
### Using a prewritten script
1. Open ```Terminal```
2. Download the repository by running the following command.
```sh
git clone https://github.com/PichapopRo/project-pantry
```
3. Execute the script file ```project-pantry/installation/mac-os.sh```.
```sh
cd project-pantry
source installation/mac-os.sh
```
### Manually
1. Open your terminal.
2. Download the repository by running the following command.
```sh
git clone https://github.com/PichapopRo/project-pantry
```
3. Make sure that you have Python 3.11 installed on your machine. You can download it from by:
```bash
brew install python@3.11
```
4. Install Python Virtual Environment.
```sh
python3.11 -m pip install --user virtualenv
python3.11 -m venv venv
source venv/bin/activate
```
5. Install requirement packages.
```sh
python -m pip install -r requirements.txt
```
6. Initialize Django
```sh
python manage.py migrate
```

7. Initialize ```.env``` file. The following script will automatically create a .env file and generate a Django secret key for you.
```sh
python -c "from django.core.management.utils import get_random_secret_key; f = open('.env', 'w'); f.write('SECRET_KEY=django-insecure-'+get_random_secret_key()+'\n'); f.close()"
echo API_USERNAME= 'Spoonacular'
echo DEBUG=False
echo TIME_ZONE = Asia/Bangkok
echo ALTER_PROMT = 'You are a chef embedded inside a recipe-viewing program. You are here to give the alternative ingredient to the users. Answer the question in this JSON format strictly:[{"name":"The ingredient name","description":"The description of the ingredient","amount":number,"unit":"The unit of the amount"},{"name":"The ingredient name","description":"The description of the ingredient","amount":number,"unit":"The unit of the amount"},...]'
echo DIFF_PROMPT = 'You are a chef embedded inside a recipe-viewing program. You are here to give a difficulty for each recipe based on techniques used, steps, ingredient and preparation. Answer strictly only "Hard", "Normal" and "Easy".'
echo APPROVAL_PROMPT = 'You are a chef embedded inside a recipe-viewing program. You are here to review recipes that was uploaded by user based on possibility and eatable. Answer strictly only in boolean (True or False). True means the recipe is possible and eatable. False means it is impossible to make and not eatable.'
echo NUTRITION_PROMPT = 'You are a chef embedded inside a recipe-viewing program. You are here to give nutrition information based on ingredients. Answer strictly only in this JSON format: {"nutrients":[{"name":"Calories","amount":316.49,"unit":"kcal","percentOfDailyNeeds":15.82},{"name":"Fat","amount":12.09,"unit":"g","percentOfDailyNeeds":18.6},{"name":"Saturated Fat","amount":3.98,"unit":"g","percentOfDailyNeeds":24.88},{"name":"Carbohydrates","amount":49.25,"unit":"g","percentOfDailyNeeds":16.42},{"name":"Net Carbohydrates","amount":46.76,"unit":"g","percentOfDailyNeeds":17.0},{"name":"Sugar","amount":21.98,"unit":"g","percentOfDailyNeeds":24.42},{"name":"Cholesterol","amount":1.88,"unit":"mg","percentOfDailyNeeds":0.63},{"name":"Sodium","amount":279.1,"unit":"mg","percentOfDailyNeeds":12.13},{"name":"Protein","amount":3.79,"unit":"g","percentOfDailyNeeds":7.57}, ...]}'
echo CHEF_BADGE_APPROVED = 10
echo DJANGO_LOG_LEVEL = DEBUG
```
8. Open ```.env``` file to put your own API_KEY, SPOONACULAR_PASSWORD, SECRET_KEY, OPENAI_APIKEY, IMGUR_CLIENT_ID, DB_PASSWORD, DB_USERNAME, DB_NAME, ALLOWED_HOSTS, and LINK_URL. Look at ```sample.env``` file for an example.

## Linux
> Notice: Please make sure that you have ```git``` installed in your machine.
### Using a prewritten script
1. Open ```Terminal```
2. Download the repository by running the following command.
```sh
git clone https://github.com/PichapopRo/project-pantry
```
3. Execute the script file ```project-pantry/installation/linux-deb-ubun.sh```.
```sh
cd project-pantry
source installation/linux-deb-ubun.sh
```
### Manually
1. Open Terminal.
2. Download the repository by running the following command.
```sh
git clone https://github.com/PichapopRo/project-pantry
```
3. Make sure that you have Python 3.11 installed in your machine. You can download it from by:
```bash
sudo apt-get update
sudo apt-get install python3.11
```
4. Install Python Virtual Environment.
```sh
sudo apt install python3.11-venv
sudo apt install python3-virtualenv
virtualenv --python python3.11 venv
```
5. Install requirement packages.
```sh
source venv/bin/activate
python -m pip install -r requirements.txt
```
6. Initialize Django
```sh
python manage.py migrate
```

7. Initialize ```.env``` file. The following script will automatically create a .env file and generate a Django secret key for you.
```sh
python -c "from django.core.management.utils import get_random_secret_key; f = open('.env', 'w'); f.write('SECRET_KEY=django-insecure-'+get_random_secret_key()+'\n'); f.close()"
echo API_USERNAME= 'Spoonacular'
echo DEBUG=False
echo TIME_ZONE = Asia/Bangkok
echo ALTER_PROMT = 'You are a chef embedded inside a recipe-viewing program. You are here to give the alternative ingredient to the users. Answer the question in this JSON format strictly:[{"name":"The ingredient name","description":"The description of the ingredient","amount":number,"unit":"The unit of the amount"},{"name":"The ingredient name","description":"The description of the ingredient","amount":number,"unit":"The unit of the amount"},...]'
echo DIFF_PROMPT = 'You are a chef embedded inside a recipe-viewing program. You are here to give a difficulty for each recipe based on techniques used, steps, ingredient and preparation. Answer strictly only "Hard", "Normal" and "Easy".'
echo APPROVAL_PROMPT = 'You are a chef embedded inside a recipe-viewing program. You are here to review recipes that was uploaded by user based on possibility and eatable. Answer strictly only in boolean (True or False). True means the recipe is possible and eatable. False means it is impossible to make and not eatable.'
echo NUTRITION_PROMPT = 'You are a chef embedded inside a recipe-viewing program. You are here to give nutrition information based on ingredients. Answer strictly only in this JSON format: {"nutrients":[{"name":"Calories","amount":316.49,"unit":"kcal","percentOfDailyNeeds":15.82},{"name":"Fat","amount":12.09,"unit":"g","percentOfDailyNeeds":18.6},{"name":"Saturated Fat","amount":3.98,"unit":"g","percentOfDailyNeeds":24.88},{"name":"Carbohydrates","amount":49.25,"unit":"g","percentOfDailyNeeds":16.42},{"name":"Net Carbohydrates","amount":46.76,"unit":"g","percentOfDailyNeeds":17.0},{"name":"Sugar","amount":21.98,"unit":"g","percentOfDailyNeeds":24.42},{"name":"Cholesterol","amount":1.88,"unit":"mg","percentOfDailyNeeds":0.63},{"name":"Sodium","amount":279.1,"unit":"mg","percentOfDailyNeeds":12.13},{"name":"Protein","amount":3.79,"unit":"g","percentOfDailyNeeds":7.57}, ...]}'
echo CHEF_BADGE_APPROVED = 10
echo DJANGO_LOG_LEVEL = DEBUG
```
8. Open ```.env``` file to put your own API_KEY, SPOONACULAR_PASSWORD, SECRET_KEY, OPENAI_APIKEY, IMGUR_CLIENT_ID, DB_PASSWORD, DB_USERNAME, DB_NAME, ALLOWED_HOSTS, and LINK_URL. Look at ```sample.env``` file for an example.

## Testing the application
In ```.env``` file, change ```DEBUG=True```, then run the following command.
```sh
python manage.py test
```

## Installation notes
You can specify the following 
settings in the ```.env``` file.
1. ```TIME_ZONE``` - You can change this to your local timezone. It must be written in TZ format ([you can find the TZ list here](https://en.wikipedia.org/wiki/List_of_tz_database_time_zones)).
2. ```DEBUG``` - You can set this to ```True``` if you want Django to provide you with further information when something crashes or to test the application.
3. ```DEBUG=True``` - the application will use SQLite database.
4. ```DEBUG=False``` - the application will use PostgreSQL database.