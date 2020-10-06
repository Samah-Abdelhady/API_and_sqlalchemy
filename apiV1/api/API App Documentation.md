# API App Documentation:

## Age of Empire||
### Age of Empire|| app is about how to get required data from online api and save every new data into postgres database. It is a webpage to manages:
1. (Search for Unit Data) display all specific unit data depending on its name.
   * Hint: I have made unit_id into db equal to new coming unit_id from api (to keep its original primary key). Because we don't read units in order, but we read them depending on their name randomly.
   * after running the program: enter unit name in the cmd or terminal.
2. Save unit data from the api into database
3. If the given unit name is already in database, then manages get fom database



## Getting Started
### Pre-requisites and Local Development:
To use this project on your local machine, you should alredy have
  * Python3
  * pip
  * postgres database (https://www.postgresql.org/download/)

### install required packages and libraries (it is an app which run on cli)
from requirements file run: pip install requirements.txt . As all required packagesare included in it 

To run the application use the following commands (on Windows):
1. python api.py

To run the application use the following commands (on Linux):
1. python3 api.py

to create the database database (I used migration):
* make sure you have ceatr your database first.
1. flask db init
  * write that command only once when start to create tables in db(it will initialize the database migration)
2. flask db migrate
  * write that command every time you have a change in tables shcema and want to update them
3. flask db upgrade
  * it will excute the founded changes to database shcema
4. flask db downgrade
  * use it only when you want to undo your last changes in db shcema (it will keep db and data save from being lost during updating on database tables shema) 


#### Virtual Enviornment

It is recommended to work within a virtual environment whenever using Python for projects. This keeps your dependencies for each project separate and organaized. Instructions for setting up a virual enviornment for your platform can be found in the [python docs](https://packaging.python.org/guides/installing-using-pip-and-virtual-environments/)

The application is run on: http://127.0.0.1:5000/  by default,and to get data copy and paste http://127.0.0.1:5000/unit  on your browser.


## API Reference

### Getting Started
* Base URL: At present this app can only be run locally and is not hosted as a base URL.

### Error Handling
Errors are returned as JSON objects in the following format:

{
  "success": False,
  "error": 404,
  "message": "not found"
}

The API will return three error types when requests fail:

* 400: Bad Request
* 404: Resource Not Found
* 500: Internal Server Error

### Endpoints

### GET '/unit'
* General:
   * Take from cmd/terminal unit_name 
   * Return an object of, which contains all data related to that unit
* Sample: after run the first 3 commands paste that `http://localhost:5000/unit` on your browser and write the name in the cmd/terminal

{
  "id": 28,
  "name": "Fire Ship",
  "description": "Spews fire at other ships. Good at sinking galleys. Attack shows pierce attack",
  "expansion": "Age of Kings",
  "age": "Castle",
  "created_in": "https://age-of-empires-2-api.herokuapp.com/api/v1/structure/dock",
  "cost": {
    "Wood": 75,
    "Gold": 45
  },
  "build_time": 36,
  "reload_time": 0.25,
  "movement_rate": 1.35,
  "line_of_sight": 5,
  "hit_points": 100,
  "range": "2.49",
  "attack": 2,
  "armor": "0/6",
  "attack_bonus": [
    "+2 buildings",
    "+3 ships/camels",
    "+2 turtle ships",
    "+1 melee"
  ],
  "armor_bonus": [
    "+5 ships/camel"
  ]
}

### Hint:
In some units like unit 35, it violates database constrains, as it is required to be (reload_time and attack) which shoul be nullable but that unit has no values for these fields. So to solve that case, I have give the fields values of (1.2 , 1) by coding just in case any unit has the same error and don't have value for them,
buid_time also in unit 43.


## Authors
Samah Abd El-hady