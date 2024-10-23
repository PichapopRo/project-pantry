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
echo DEBUG=False >> .env
echo ALLOWED_HOSTS=* >> .env
echo TIME_ZONE=Asia/Bangkok >> .env
```
8. Installation is completed.

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
echo DEBUG=False >> .env
echo ALLOWED_HOSTS=* >> .env
echo TIME_ZONE=Asia/Bangkok >> .env
```
8. Installation is completed.

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
echo DEBUG=False >> .env
echo ALLOWED_HOSTS=* >> .env
echo TIME_ZONE=Asia/Bangkok >> .env
```
8. Installation is completed.

## Testing the application
The test can be done with the following command.
```sh
python manage.py test
```

## Installation notes
You can specify the following 
settings in the ```.env``` file.
1. ```TIME_ZONE``` - You can change this to your local timezone. It must be written in TZ format ([you can find the TZ list here](https://en.wikipedia.org/wiki/List_of_tz_database_time_zones)).
2. ```DEBUG``` - You can set this to ```True``` if you want Django to provide you with further information when something crashes.
3. ```ALLOWED_HOSTS``` 