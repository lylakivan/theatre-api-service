# Theatre Service API

### Project that allows theater visitors to make reservations online and choose needed seats, without going physically to the theatre written on DRF

## DB Structure
![DB Structure](demo_readme/DB_Structure.png)

## Features
- **CRUD Operations**
- **JWT Authentication**
- **Email-Based Authentication**
- **Admin Panel**
- **Play's Filtering**
- **Throttling Mechanism**
- **Managing orders and tickets**
- **API Documentation**


## Installing using GitHub
Install PostgreSQL and create db.

Open Terminal to run following commands:
Clone the repository:
    ```
    git clone https://github.com/lylakivan/theatre-api-service.git
    ```
Create and activate virtual environment:
   * **On Windows**
      ```
      python -m venv venv
      ```

      ```
      venv\Scripts\activate
      ```

   *   **On MacOS**
      ```
      python3 -m venv venv
      ```

      ```
      source venv/bin/activate
      ```
Install needed requirements:
    ```
    pip install -r requirements.txt
    ```

Run database migrations:
    ```
    python manage.py migrate
    ```

Create .env file using ```env.sample``` file

Run server:

   ```
   python manage.py runserver
   ```

Go to [http://127.0.0.1:8000/](http://127.0.0.1:8000/)

## Run with Docker
Docker should be installed.

- pull docker container
    ``` 
    docker pull lylakivan/docker-theatre-api
    ```
- run container
    ```
    docker-compose build
    docker-compose up
    ```

## You can use following superuser (or create another one by yourself using createsuperuser)
* email: admin@admin.com
* password: admin

## Go to site: http://127.0.0.1:8000/api/theatre/


## DEMO

![Swagger](photo_readme/Swagger.png)


![API_page](photo_readme/API.png)