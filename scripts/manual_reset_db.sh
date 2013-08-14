sudo rm /var/www/faculty.bishopblanchet.org/sqlite.db
cd ~/bbhs_intranet
python manage.py syncdb
sudo chmod 777 /var/www/faculty.bishopblanchet.org/sqlite.db
