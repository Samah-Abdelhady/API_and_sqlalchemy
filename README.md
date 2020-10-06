# Api APP Documentation:

## Age of Empire||
### Age of Empire|| app is about how to get required data from online api and save every new data into postgres database. It is a webpage to manages:
1. (Search for Unit Data) display all specific unit data depending on its name.
   * Hint: I have made unit_id into db equal to new coming unit_id from api (to keep its original primary key). Because we don't read units in order, but we read them depending on their name randomly.
   * after running the program: enter unit name in the cmd or terminal.
2. Save unit data from the api into database
3. If the given unit name is already in database, then manages get fom database



## It is an application which run only on cli by the command (python api.py)

## Read documention to know every thing to know how to install requirements, run program and know program target.