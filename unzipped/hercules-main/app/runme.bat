del hercules\db.sqlite3
del main\migrations\0*.py
python manage.py makemigrations
python manage.py migrate
python manage.py initialize
python manage.py runserver
