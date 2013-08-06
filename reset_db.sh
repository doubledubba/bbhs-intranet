su root
rm /var/www/faculty.bishopblanchet.org/sqlite.db
python manage.py syncdb
chmod 777 /var/www/faculty.bishopblanchet.org/sqlite.db
