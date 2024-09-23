# [CHALLENGE] NORKTOWN

```
This is a RESTful API for managing car owners and their vehicles.
The system adheres to specific rules,
such as limiting the number of vehicles per person and vehicle color/model options.

```

The project was built using Python, Flask, SQLAlchemy, and JWT for authentication, and containerized with Docker. 
It supports CRUD operations (Create, Read, Update, Delete) for car owners and their vehicles.

### Challenge Requirements:

- One person can own up to 3 cars.
- A car must be one of three colors: Yellow, Blue, or Gray.
- Cars have one of three models: Hatch, Sedan, or Convertible.
- Cars must have an owner, and no car can exist without one.
- Unowned individuals are marked as "sale opportunities" (potential future car owners).

## Getting Started

1. Clone this repository

```
git clone https://github.com/404six/norktown.git
```

2. Create a virtual environment

```
py -m venv venv
```

3. Activate the virtual environment
```
./venv/Scripts/activate
```

4. Build the docker image

```
docker-compose build
```

5. Start the Docker container

```
docker-compose up
```

Once running, the API will be available at http://localhost:5000.



# API Endpoints

## Authentication
All routes require authentication via a JWT token.

### Register a User
- Endpoint: /api/auth/register
- Method: POST
- Description: ``Registers a new user``
## Login & Get Token
- Endpoint: /api/auth/login
- Method: POST
- Description: ``Authenticates the user and returns a JWT token`` 

  
## Sample Login Request:

```
{
  "username": "yourusername",
  "password": "yourpassword"
}

```
### Include this token in the Authorization header of your requests:
```
Authorization: Bearer yourjwttoken
```

To obtain a token, send a POST request to /api/auth/login with a JSON body containing your username and password. For example:

```
{
  "username": "yourusername",
  "password": "yourpassword"
}
```

Include this token in the Authorization header of your requests:
```
{
  "access_token": "yourjwttoken"
}
```

## API Endpoints


### Cars

| Endpoint                            | HTTP Method | Result                                     |
| ----------------------------------- | -----------| ------------------------------------------ |
| /api/cars                           | GET        | Retrieve all cars                                |
| /api/cars/<int:car_id>              | GET        | Retrieve a specific car                     |
| /api/cars                           | POST       | Add a car to an existing owner    |
| /api/cars/<int:car_id>              | PUT        | Update an existing car                |
| /api/cars/<int:car_id>              | DELETE     | Delete an existing car                |


### Car Owners

| Endpoint                            | HTTP Method | Result                                     |
| ----------------------------------- | -----------| ------------------------------------------ |
| /api/owners                         | GET        | Retrieve all owners                             |
| /api/owners/<int:owner_id>          | GET        | Retrieve a specific owner                  |
| /api/owners                         | POST       | Create a new owner                         |
| /api/owners/<int:owner_id>          | PUT        | Update an existing owner             |
| /api/owners/<int:owner_id>          | DELETE     | Delete an existing owner             |


## License

This project is licensed under the MIT License 
