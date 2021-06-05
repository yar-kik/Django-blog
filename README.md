# Django Blog
 
[![Build Status](https://travis-ci.com/yar-kik/Django-blog.svg?branch=master)](https://travis-ci.com/yar-kik/Django-blog)
[![Coverage Status](https://coveralls.io/repos/github/yar-kik/Django-blog/badge.svg)](https://coveralls.io/github/yar-kik/Django-blog)
![GitHub](https://img.shields.io/github/license/yar-kik/Django-blog)
[![Python 3.8](https://img.shields.io/badge/python-3.8-blue.svg)](https://www.python.org/downloads/release/python-3810/)

This is simple blog on Django web-framework
## Requirements
To install and run this application you should have already installed Git and Docker.

## Installation 
To download project you should run in command line:
```
git clone https://github.com/yar-kik/Django-blog.git
```
To install and run project with development settings:
```
docker-compose -f docker-compose-dev.yml up -d
```
Or you can run production-ready environment configuration with Gunicorn and Nginx:
 ```
docker-compose -f docker-compose.yml up -d
```