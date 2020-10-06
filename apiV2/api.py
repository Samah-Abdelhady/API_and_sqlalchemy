import os
from flask import Flask, render_template, abort, jsonify
import psycopg2
import json
import requests
import database
from models import AttackBouns, ArmorBouns, Unit


def create_app():
    app = Flask(__name__)
    app.config.from_object('config')
    database.setup_db(app)
    errorFlag = 0

    @app.after_request
    def after_request(response):
        response.headers.add('Access-Control-Allow-Methods', 'GET,POST')
        return response

    def get_unit_name():
        unitName = input("enter unit name...\t")
        return " ".join(unitName.split())  # move all extra spaces in the name
    #################################################
    #  check if the given unit name is empty as just press enter


    def check_empty_unit_name(unitName):
        if (len(unitName) == 0):  # could be if(unitName is '\r') too
            return True
        else:
            return False


    ##############################################
    #  ask database to search about given unit name data
    def ask_database(unitName):
        try:
            unitData = Unit.query.filter(Unit.name.ilike(unitName)).one_or_none()
            return unitData
        #  if can not retrive any data from db or enen None, then there is an error
        except (Exception, psycopg2.DatabaseError) as error:
        	global errorFlag
        	print(error)
        	errorFlag = 1
        	return error

            # abort(500)


    #########################################
    #  ask api to search about given unit name data
    def ask_api(unitName):
        apiUrl = "https://age-of-empires-2-api.herokuapp.com/api/v1/unit/"+unitName
        #   gey datas for a specific unit from api
        request = requests.get(apiUrl)
        if 'json' in request.headers.get('Content-Type'):
        	data = request.json()
        else:
        	return False
        # data = json.loads(request.content)
        return data


    ####################################
    #  is the given unit is in api or not founded
    def is_exist_in_api(data):
        #  mesage is a dictionary key,returned if the api doesn't have given unit
        if "message" in data:
            print('not in the api')
            # input not found
            abort(404)
        else:
            return True


    ###############################
    # is this unit had gained attack bouns
    def has_attack_bonus(new_unit_attack_bonuses):
        if (new_unit_attack_bonuses is None):
            return False
        else:
            return True


    ############################
    # is this unit had gained armor bouns
    def has_armor_bonus(new_unit_armor_bonuses):
        if (new_unit_armor_bonuses is None):
            return False
        else:
            return True


    #########################
    #  save new unit data into postgres database
    #  unit attributes which Could have None value are not mandatory to have value
    def set_new_unit_data_into_db(data):
        new_unit_id = data["id"]
        new_unit_name = data['name']
        new_nuit_description = data['description'] if "description" in data else None
        new_unit_expansion = data['expansion']
        new_unit_age = data['age']
        new_unit_created_in = data['created_in']
        new_unit_cost = data['cost']
        #  ubit 43 reload_time constrain(not null) so I but any number to pass
        new_unit_build_time = data['build_time'] if "build_time" in data else 1
        # ubit 53  reload_time constrain not null, so I but any number to pass
        new_unit_reload_time = data['reload_time'] if "reload_time" in data else 1.2
        new_unit_attack_delay = data['attack_delay'] if "attack_delay" in data else None
        new_unit_movement_rate = data['movement_rate']
        new_unit_line_of_sight = data['line_of_sight']
        new_unit_hit_points = data['hit_points']
        new_unit_range = data['range'] if "range" in data else None
        #  ubit 53 attack constrain not null, so I but any number here to pass test
        new_unit_armor = data['armor']
        new_unit_attack = data['attack'] if "attack" in data else 1
        new_unit_armor = data['armor']
        new_unit_search_radius = data['search_radius'] if "search_radius" in data else None
        new_unit_accuracy = data['accuracy'] if "accuracy" in data else None
        new_unit_blast_radius = data['blast_radius'] if "blast_radius" in data else None
        new_unit_attack_bonuses = data['attack_bonus'].copy() if "attack_bonus" in data else None
        new_unit_armor_bonuses = data['armor_bonus'].copy() if "armor_bonus" in data else None

        #  see if the unit has attack/armor bounses
        attack_bonus = has_attack_bonus(new_unit_attack_bonuses)
        armor_bonus = has_armor_bonus(new_unit_armor_bonuses)

        try:
            #  save unit data into unit table
            new_unit = Unit(id=new_unit_id, name=new_unit_name, description=new_nuit_description, expansion=new_unit_expansion, age=new_unit_age, created_in=new_unit_created_in, cost=new_unit_cost, build_time=new_unit_build_time, reload_time=new_unit_reload_time, attack_delay=new_unit_attack_delay, movement_rate=new_unit_movement_rate, line_of_sight=new_unit_line_of_sight, hit_points=new_unit_hit_points, unit_range=new_unit_range, attack=new_unit_attack, armor=new_unit_armor, search_radius=new_unit_search_radius, accuracy=new_unit_accuracy, blast_radius=new_unit_blast_radius)
            new_unit.insert()
            #  in case unit has poth attack and armor bouns
            if ((attack_bonus is True) and (armor_bonus is True)):
                new_attack_bouns = AttackBouns(attackBouns=new_unit_attack_bonuses)
                new_armor_bouns = ArmorBouns(armorBouns=new_unit_armor_bonuses)
                new_unit.attack_bonuses = [new_attack_bouns]
                new_unit.armor_bonuses = [new_armor_bouns]
                new_attack_bouns.insert()
                new_armor_bouns.insert()

            #  in case unit has only armor bouns
            elif((attack_bonus is False) and (armor_bonus is True)):
                new_armor_bouns = ArmorBouns(armorBouns=new_unit_armor_bonuses)
                new_unit.armor_bonuses = [new_armor_bouns]
                new_armor_bouns.insert()

            #  in case unit has only attack bouns
            elif((attack_bonus is True) and (armor_bonus is False)):
                new_attack_bouns = AttackBouns(attackBouns=new_unit_attack_bonuses)
                new_unit.attack_bonuses = [new_attack_bouns]
                new_attack_bouns.insert()

        except (Exception, psycopg2.DatabaseError) as error:
            print('error during saving into database')
            print(error)
            return error
        finally:
            db.session.close()

    #######################################


    def retrive_unit_data_from_db(unitData):
        #  dectionary to read data coming from db in it
        all_data = {}

        #  start setting data into dectionary
        all_data["id"] = unitData.id
        all_data["name"] = unitData.name

        #  (check it to print only data which have values)
        if (unitData.description is not None):
            all_data["description"] = unitData.description

        all_data["expansion"] = unitData.expansion
        all_data["age"] = unitData.age
        all_data["created_in"] = unitData.created_in
        all_data["cost"] = unitData.cost
        all_data["build_time"] = unitData.build_time
        #  convert decimal object data to float then to json object
        all_data["reload_time"] = json.dumps(float(unitData.reload_time))

        if (unitData.attack_delay is not None):
            all_data["attack_delay"] = json.dumps(float(unitData.attack_delay))

        all_data["movement_rate"] = json.dumps(float(unitData.movement_rate))
        all_data["line_of_sight"] = unitData.line_of_sight
        all_data["hit_points"] = unitData.hit_points

        if (unitData.unit_range is not None):
            all_data["range"] = unitData.unit_range

        all_data["attack"] = unitData.attack
        all_data["armor"] = unitData.armor

        if (len(unitData.attack_bonuses) > 0):
            all_data["attack_bouns"] = [attack.attackBouns for attack in unitData.attack_bonuses]

        if (len(unitData.armor_bonuses) > 0):
            all_data["armor_bouns"] = [armor.armorBouns for armor in unitData.armor_bonuses]

        if (unitData.search_radius is not None):
            all_data["search_radius"] = unitData.search_radius

        if (unitData.accuracy is not None):
            all_data["accuracy"] = unitData.accuracy

        if (unitData.blast_radius is not None):
            all_data["blast_radius"] = unitData.blast_radius

        return all_data
    ################
    # @app.route('/unit/<string:unit_name>', methods=['GET','POST'])


    @app.route('/', methods=['GET', 'POST'])
    def get_unit_data():
        #  read name from user on cmd or termnal
        unitName = get_unit_name()

        #  see if the user just leave name empty
        nameFlag = check_empty_unit_name(unitName)

        #  if name left empty
        if (nameFlag is True):
            print("error, empty input")
            #  unprocessable
            abort(422)

        else:
            #  search about data in db
            unitData = ask_database(unitName)

            if (errorFlag == 1):
            	print('can not get from database', unitData)
            	# return unitData

            elif unitData is not None:
                all_data = retrive_unit_data_from_db(unitData)

                print(json.dumps(all_data, indent=2))

            #  if unit data is not in database then search about it in the api
            elif unitData is None:
                #  ask api about given unit name data
                data = ask_api(unitName)

                #  if api not working
                if data is False:
                	print("api is not working, we can not get data...")

                #  if the api do really have given unit data or not
                apiFlag = is_exist_in_api(data)

                #  if the given name is currently existed in the api
                #  then return the nuit data from the api and save them into local database
                if apiFlag:
                    set_new_unit_data_into_db(data)
                    print(json.dumps(data, indent=2))
            return

    with app.app_context():
        get_unit_data()


    @app.errorhandler(400)
    def bad_request(error):
        return jsonify({
            "success": False,
            "error": 400,
            "message": "bad request"
            }), 400


    @app.errorhandler(404)
    def not_found(error):
        return jsonify({
            "success": False,
            "error": 404,
            "message": "resource not found"
            }), 404


    @app.errorhandler(500)
    def internal_server_error(error):
        return jsonify({
            "success": False,
            "error": 500,
            "message": "internal server error"
            }), 500


    return app

create_app()

