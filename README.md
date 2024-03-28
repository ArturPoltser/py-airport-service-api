# Airport Service API
The Airport Service API project, built using Django Rest Framework, provides a comprehensive API for managing airport data.
## Installation using GitHub

Install PostgresSQL and create DB

```
git clone https://github.com/ArturPoltser/py-airport-service-api.git
cd py-airport-service-api
python -m venv venv
venv\Scripts\activate  #for MacOS/Linux use: source vevn/bin/activate
pip install -r requirements.txt
```
Don't forget to create and fill your ```.env``` file according to ```.env.sample```
```shell
python manage.py migrate
python manage.py loaddata airport_service_db_data.json
python manage.py runserver
```

### Run with Docker
Docker should be installed

```
docker-compose build
docker-compose up
```

### Features

>* JWT Authentication
>* Admin panel (```/admin/```)
>* Documentation (located at ```/api/schema/swagger-ui/```)
>* Managing Orders and Tickets
>* Creating Routs with Airports
>* Creating Flights, Crew, Airplanes, Airplane Types
>* Filtering routs and flights by various parameters 
>* Covered the project with tests

### Getting access
You can use the following Superuser:

* Email: `admin@admin.com`
* Password: `1qazcde3`

Or register a new user using the ```/api/user/register/``` endpoint.
Obtain an authentication(access) token by sending a POST request to the ```/api/user/token/``` endpoint with your email and password.
Use the obtained token in the authorization header for accessing protected endpoints(ex. ```Authorization: Bearer <Your Access Token>```).

Be free to explore various endpoints for different functionalities provided by the API.

