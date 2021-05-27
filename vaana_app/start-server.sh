#!/usr/bin/env bash
# start-server.sh
if [ -n "$DJANGO_SUPERUSER_USERNAME" ] && [ -n "$DJANGO_SUPERUSER_PASSWORD" ] ; then
    (cd vaana_app; python manage.py createsuperuser --no-input)
fi
cd vaana_app
python manage.py collectstatic --noinput
python manage.py makemigrations --noinput
python manage.py migrate --noinput
(gunicorn vaana_app.wsgi --user www-data --bind 0.0.0.0:8010 --workers 3) &
nginx -g "daemon off;"