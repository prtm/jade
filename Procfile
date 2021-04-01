release: cd jade-frontend && npm install && npm run build && cd .. && python manage.py migrate 

web: gunicorn jade.wsgi:application
worker: celery worker --app=jade.celery_app --loglevel=info
beat: celery beat --app=jade.celery_app --loglevel=info
