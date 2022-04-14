<div id="top"></div>

  <h1 align="center">Python Django Integration with KeyCloak</h1>

## About The Project

just a simple web application with login page and two other pages one for admin and one for normal
user but to control user privilege using keycloak identity service so admin login can
view both 2 pages and normal user login can view only the normal user page.


Use the `README.md` to get started.




### Built With


* [Python3](https://www.python.org/)
* [Django Framework](https://www.djangoproject.com/)
* [Django Rest Framework](https://www.django-rest-framework.org/)
* [KeyCloak](https://www.keycloak.org/)
* [Docker](https://www.docker.com/)
* [PostgreSQL](https://www.postgresql.org/)




## Getting Started



### Prerequisites

You should have docker installed on your local machine

* check this [docs](https://docs.docker.com/get-docker/) to install docker 

### Installation

To RUN and TEST this project on your local machine, Please follow below instructions
1. Clone the repo
   ```sh
   git clone https://github.com:AbdelrahmanRabiee/key-cloak-django.git
   ```
2. Build the project with docker-compose
   ```sh
   docker-compose up --build
   ```


<h4>Open your browser</h4>

* Go to KeyCloak Administration console [http://0.0.0.0:28080/admin/](http://0.0.0.0:28080/admin/)
* Credentials --> username: admin    --> password: admin
* Create New Realm 'MontyMobile'
* Create new client 'monty_mobile_client'
* Generate Secret key for 'monty_mobile_client'
* Create new roles 'Admin User Role', 'Normal User Role'
* Create two users and add roles to each of them

After generating the secret key for 'monty_mobile_client' update the .env KEYCLOAK_CLIENT_SECRET_KEY with the new key and then build the images again
   ```sh
   docker-compose up --build
   ```


### Open [Postman](https://www.postman.com/) To TEST APIs </h4>
1. http://0.0.0.0:9090/api/v1/login/ to get new access token
2. POST Request: `{'email': 'normal_user@keycloak.org', 'password': 'passord'}`
3. Response: `{
    "access_token": "eyJhbGciOiJSUUZzZkNGYmlsZV9jbGllbnQiL0V_NnVe-xYyXyJbZP8bm8JtImimZu3",
    "expires_in": 300,
    "refresh_expires_in": 1800,
    "refresh_token": "eyJhbGciOiJIUzI1NiIsInR",
    "token_type": "Bearer",
    "not-before-policy": 0,
    "session_state": "67d00534-bfdc-4ac7-8112-4fb706f02775",
    "scope": "profile email"
}`
4. try to get token for admin user and normal user
5. GET http://0.0.0.0:9090/api/v1/user/ with user token or admin token
6. Response: ` {
        "keycloak_id": "098f3742-96e5-4040-88e8-459cd0478561",
        "password": "",
        "last_login": "2022-04-13T19:45:18.015986Z",
        "is_superuser": false,
        "email": "admin@keycloak.com",
        "first_name": "admin",
        "last_name": "keycloak",
        "role": "admin",
        "is_active": true,
        "is_staff": false,
        "is_email_verified": true,
        "groups": [],
        "user_permissions": []
    }`
7. GET http://0.0.0.0:9090/api/v1/admin/ with user token
8. Response: `{'error': 'you do not have permission to perform this action'}`

