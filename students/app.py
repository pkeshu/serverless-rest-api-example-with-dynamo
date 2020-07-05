import json
import boto3
import uuid
from flask.json import jsonify
from flask_lambda import FlaskLambda
from flask import request

app = FlaskLambda(__name__)
ddb = boto3.resource('dynamodb')
table = ddb.Table('students')

content_type = {'Content-Type': 'application/json'}


@app.route("/")
def index():
    data = {
        "message": "Hello there i'm keshar from here"
    }
    return (
        json.dumps(data),
        200,

    )


@app.route("/students", methods=['GET', 'POST'])
def put_or_list_students():
    if request.method == 'GET':
        students = table.scan()['Items']
        print("keshar>>>>>>>", type(students))
        return (
            json.dumps(students),
            200,
            content_type
        )
    else:
        print('keshar>>>>>', request.get_json())
        uid = uuid.uuid4()
        string = str(uid)
        print(string.upper())
        data = request.get_json()
        data['sid'] = string.upper()
        table.put_item(Item=data)
        response = {"message": "Students created"}
        return (
            json.dumps(response),
            201,
            content_type
        )


@app.route("/students/<id>", methods=['GET', 'PUT', 'DELETE'])
def get_update_delete_student(id):
    if request.method == 'GET':
        student = table.get_item(Key={"sid": id}).get('Item')
        return (
            json.dumps(student),
            200,
            content_type
        )
    elif request.method == 'PUT':
        attribute_updates = {key: {"Value": value, "Action": "PUT"} for key, value in request.get_json().items()}
        print(table.update_item(Key={'sid': id}, AttributeUpdates=attribute_updates))
        return (
            json.dumps({"message": "Student updated"}),
            200,
            content_type
        )
    elif request.method == 'DELETE':
        table.delete_item(Key={"sid": id})
        return (
            json.dumps({"message": "Student deleted"}),
            200,
            content_type
        )
    else:
        return (
            json.dumps({"message:": "Method not specified!"}),
            404,
            content_type
        )
