# superstore-sales-api with FASTApi

A Boilerplate FastApi project

![MIT license](https://img.shields.io/badge/License-MIT-blue.svg) [![Build Status](https://api.travis-ci.com/ari-hacks/fastapi-boilerplate.svg?branch=master)](https://travis-ci.com/ari-hacks/fastapi-skeleton)


## Features 
- [x] Boilerplate project structure  
- [x] Asynchronous API 
- [x] Travis CI configuration before deploy 
- [x] API testing with `pytest` 
- [x] Pipenv dependency management 
- [x] Docker containerization and deploy to Heroku   

## Set up

### Requirements

- [Python](https://www.python.org/) >= 3.8.1
- Pipenv
        → pip install pipenv

  ```` Setup in Windown

    → py -3 -m venv venv
    → venv\Scripts\activate
    → pip install pipenv
    → pipenv install

  ````

## Running Locally 

1. Clone this repository and `cd` into it

    ```bash
        → cd superstore-ales-api
    ```


2. Pipenv dependency management 
    ```bash
        #run pipenv 
        → pipenv shell
    ```
    ```bash
        #install dependencies  
        → pipenv install
        #run locally
        → uvicorn app.main:app --reload 
    ```

3. [Install & Run in docker](https://hub.docker.com/) 
4. Build Docker Image 
    ```bash
        ➜ docker build -t app .
    ```
5. Start Docker container 
    ```bash
        ➜ docker run -d --name superstore-sales-api -p 5000:5000 app
    ```
6. Run the application
   ```bash 
    Uvicorn running on http://0.0.0.0:5000/users/health-check 
    #or 
    http://localhost:5000/users/health-check
   ```
7. Check the logs 
   ```bash 
   ➜ docker container logs -f superstore-sales-api
   ```
## Dev
uvicorn app.main:app --host localhost --port 8000 --reload

-> Enjoy: http://localhost:8000/docs
## Deploy pre-configured (Docker Deploy)

### Có thể sử dụng heroku để host
Please [Sign up](https://www.heroku.com/)  before Deploying.  [![Deploy](https://www.herokucdn.com/deploy/button.svg)](https://heroku.com/deploy)                                               
