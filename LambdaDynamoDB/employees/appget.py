import json
import os
from botocore.exceptions import ClientError
from boto3.dynamodb.conditions import Key, Attr
import boto3


def get_employee(event, context):
    try:
        person_id = event['queryStringParameters']['id']
        person_name = event['queryStringParameters']['first_name']
        request_data_id = person_id
        response = None
        if request_data_id is not None:
            table_name = os.getenv('TABLE_NAME')
            dyn_resource = boto3.resource('dynamodb')
            employee_table = dyn_resource.Table(table_name)
            # Loop through all the items and load each
            employee = employee_table.query(
                KeyConditionExpression=Key('first_name').eq(person_name) & Key('id').eq(int(person_id)),
            )
            if employee['Count'] == 0:
                return {
                    "statusCode": 200,
                    "body": json.dumps({
                        "message": f"There is no Employee in the Data Base with id: {person_id} and name:{person_name}",
                    }),
                }
            else:
                return {
                    "statusCode": 200,
                    "body": json.dumps({
                        "message": f"Successfully retrieved Employee: {employee['Items'][0]}",
                    }),
                }
        else:
            return {
                "statusCode": 400,
                "body": json.dumps({
                    "message": f"Query string must have parameter{response}",
                }),
            }

    except ClientError as ex:
        print(ex.response)
        return {
            "statusCode": 200,
            "body": json.dumps({
                "message": f"{ex}",
            }),
        }

