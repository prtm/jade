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

1. [Python3](https://www.python.org/downloads/) required
2. Create isolated virtual python environment
```
    pip3 install pipenv
```
3. Install all dependencies for this project. 
```
# Specific requirement file found in requirements folder

pipenv install
```
4. add env file
``` 
cp docs/env_example .env
```

Checkout [Jade-frontend](https://github.com/prtm/jade-frontend)