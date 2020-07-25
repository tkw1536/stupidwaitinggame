FROM python:3.8-alpine

# Install binary python dependencies
RUN apk add --no-cache \
    build-base \
    mailcap \
    libxslt-dev \
    linux-headers \
    pcre-dev \
    python3-dev

ADD docker/uwsgi.ini /app/uwsgi.ini

# Add requirements and install dependencies
ADD requirements.txt /app/
ADD requirements-prod.txt /app/
WORKDIR /app/

# Add the entrypoint and add configuration
RUN mkdir -p /var/www/static/ \
    && pip install -r requirements.txt \
    && pip install -r requirements-prod.txt

# Install Django App and setup the setting module
ADD manage.py /app/
ADD stupidwaitinggame/ /app/stupidwaitinggame
ADD docker/ /app/docker

ENV DJANGO_SETTINGS_MODULE "stupidwaitinggame.docker_settings"

### ALL THE CONFIGURATION

ENV DJANGO_INCLUDE_TRACKING ""

# The secret key used for django
ENV DJANGO_SECRET_KEY ""

# A comma-seperated list of allowed hosts
ENV DJANGO_ALLOWED_HOSTS "localhost"

# Database settings
## Use SQLITE out of the box
ENV DJANGO_DB_ENGINE "django.db.backends.sqlite3"
ENV DJANGO_DB_NAME "/data/stupidwaitinggame.db"
ENV DJANGO_DB_USER ""
ENV DJANGO_DB_PASSWORD ""
ENV DJANG_DB_HOST ""
ENV DJANGO_DB_PORT ""

# Collect all the static files at build time
RUN DJANGO_SECRET_KEY=setup python manage.py collectstatic --noinput

# Volume and ports
VOLUME /data/
EXPOSE 80

ENTRYPOINT ["/app/docker/entrypoint.sh"]
CMD ["uwsgi", "--ini", "/app/docker/uwsgi.ini"]
