set -o erreit

#to install dependencies
pip install -r requirement.txt

#collect staticfiles
python manage.py collectstatic --no-input

#to make migrations and migrate
python manage.py makemigrations && pytho manage.py migrate