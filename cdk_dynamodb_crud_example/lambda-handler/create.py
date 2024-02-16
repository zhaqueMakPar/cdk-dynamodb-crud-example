import json
import os
import uuid

import boto3

_client = boto3.client("dynamodb")


def handler(event, context):
    try:
        # get table name from enviroment variable, if not found return error
        table_name = os.environ.get("TABLE_NAME")
        if not table_name:
            return {
                "statusCode": 400,
                "body": json.dumps("TABLE_NAME env var is not set"),
            }

        # get the name from the body of the request, return an error if name not present
        body = json.loads(event["body"])
        name = body.get("name")
        if not name:
            return {"statusCode": 400, "body": json.dumps("name is required")}

        # generate uuid for new item
        generated_id = str(uuid.uuid4())

        # create dict for new item, include the generated uuid and name
        item = {
            "id": {"S": generated_id},
            "name": {"S": name},
        }

        # insert item into table
        response = _client.put_item(TableName=table_name, Item=item)

        return {
            "statusCode": 200,
            "body": json.dumps({"id": generated_id, "name": name, "message": response}),
        }

    # if something goes wrong return error
    except Exception as e:
        print(e)  # log to cloudwatch
        return {"statusCode": 500, "body": json.dumps(e)}
