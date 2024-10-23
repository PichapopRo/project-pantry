echo Installing vertual environment
sudo apt-get update
sudo apt-get install python3.11
sudo apt install python3.11-venv
sudo apt install python3-virtualenv
virtualenv --python python3.11 venv
source venv/bin/activate
echo Installing python requirements
python -m pip install -r requirements.txt
echo Initializing Django
python manage.py migrate
echo "Initializing environment"
python -c "from django.core.management.utils import get_random_secret_key; f = open('.env', 'w'); f.write('SECRET_KEY=django-insecure-'+get_random_secret_key()+'\n'); f.close()"
echo "DEBUG=False" >> .env
echo "ALLOWED_HOSTS=*" >> .env
echo "TIME_ZONE=Asia/Bangkok" >> .env
echo API_KEY=fake-api-key >> .env
echo SPOONACULAR_PASSWORD=set-your_password >> .env