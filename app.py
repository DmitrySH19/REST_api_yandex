from flask import Flask, jsonify
from flask import abort
from flask import make_response
from flask import request
from mysql.connector import MySQLConnection, Error
from python_mysql_dbconfig import read_db_config
from utils import type_by_num, num_by_type

app = Flask(__name__)


def insert_courier(json_list):
    query_couriers = "INSERT INTO couriers(id,courier_type) "\
                    "VALUES(%s,%s)"
    courier_region = "INSERT INTO region(courires_id,region) "\
                    "VALUES(%s,%s)"
    working_hours = "INSERT INTO working_hours(courires_id,start_time,end_time) "\
                    "VALUES(%s,%s,%s)"
    try:
        db_config = read_db_config()
        conn = MySQLConnection(**db_config)

        cursor = conn.cursor()
        for i in range(len(json_list)):
            args = (json_list[i]['courier_id'], json_list[i]['courier_type'])
            cursor.execute(query_couriers, args)
            for j in range(len(json_list[i]['regions'])):
                args = (json_list[i]['courier_id'], json_list[i]['regions'][j])
                cursor.execute(courier_region, args)
            for j in range(len(json_list[i]['working_hours'])):
                hours = json_list[i]['working_hours'][j].split('-')
                args = (json_list[i]['courier_id'], hours[0], hours[1])
                cursor.execute(working_hours, args)

        if cursor.lastrowid:
            print('last insert id', cursor.lastrowid)
        else:
            print('last insert id not found')

        conn.commit()
    except Error as error:
        print(error)

    finally:
        cursor.close()
        conn.close()

tasks = [
    {
        'id': 1,
        'title': u'Buy groceries',
        'description': u'Milk, Cheese, Pizza, Fruit, Tylenol', 
        'done': False
    },
    {
        'id': 2,
        'title': u'Learn Python',
        'description': u'Need to find a good Python tutorial on the web', 
        'done': False
    }
]

@app.route('/couriers', methods=['POST'])
def post_couriers():
    insert_courier(request.json['data'])
    return 'sucsess'


@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'error': 'Not found'}), 404)

@app.route('/tasks', methods=['GET'])
def get_tasks():
    return jsonify({'tasks': tasks})

from flask import abort

@app.route('/tasks/<int:task_id>', methods=['GET'])
def get_task(task_id):
    #task = filter(lambda t: t['id'] == task_id, tasks)
    # if len(task) == 0:
    #     abort(404)
    return jsonify({'task': tasks[0]})

@app.route('/tasks', methods=['POST'])
def create_task():
    if not request.json or not 'title' in request.json:
        abort(400)
    task = {
        'id': tasks[-1]['id'] + 1,
        'title': request.json['title'],
        'description': request.json.get('description', ""),
        'done': False
    }
    tasks.append(task)
    return jsonify({'task': task}), 201

if __name__ == '__main__':
    app.run(debug=True)
