FROM python:3.8.1
ENV PYTHONUNBUFFERED 1
RUN mkdir /config
ADD /config/requirements.pip /config/
RUN pip install -r /config/requirements.pip
RUN mkdir /static
RUN mkdir /src
WORKDIR /src
CMD ["sh", "-c", "python manage.py collectstatic --no-input; python manage.py migrate; gunicorn THtrpo.wsgi -b 0.0.0.0:8000 "]