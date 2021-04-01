# Jade

<img src="docs/images/favicon-32x32.png" alt="Jade"/>

A BSE bhav browser for the recent activity that has taken place in the market.

## Features

* Powered by Django, Redis
* Bhav data is stored in Redis
* Get the sorted bhav data
* Search with suggestions
* Download search results as csv

## Installation

Vue JS
```shell
cd jade-frontend

# Install dependencies
npm install

# Copy env file
cp docs/env_example .env

# Production build
npm run build
```

[Python3](https://www.python.org/downloads/)
```
# Create isolated virtual python environment
pip3 install pipenv


# Install all dependencies for this project. 

# Specific requirement file found in requirements folder

pipenv install

# Add env file
cp docs/env_example .env 
```

### For Celery task
```
# Run celery worker
celery worker --app=jade.celery_app --loglevel=info

# Run celery beat
celery beat --app=jade.celery_app --loglevel=info
```

Checkout Jade-frontend [here](https://github.com/prtm/jade-frontend).