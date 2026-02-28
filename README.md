# TSES API

Simple Dockerised Django application
---

### Set up
1. Clone directory and cd into the project directory
2. Create a file called local.env inside the core directory and populate it with the content of the `sample.env` file in the project root directory. Update the file accordingly
3. Run command: `docker compose up -—build`, to the docker images and containers
5. Open your browser and navigate to `0.0.0.0:8000/docs/` to view and test the API
6. You can create a Django super user by starting the containers in detarched mode and running the django command.  
   `docker compose up -d —build`  
    `docker compose exec web python manage.py createsuperuser`

