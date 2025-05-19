python3 ../server/wingbook/manage.py makemigrations
docker-compose down --force
docker-compose up -d --build