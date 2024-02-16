import os
import json

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

        # get queryStringParameters from the event
        query_params = event.get("queryStringParameters", {})
        # get item_id query parameter
        item_id = query_params.get("item_id", None)

        # if item_id is none return error
        if item_id is None:
            return {
                "statusCode": 500,
                "body": json.dumps("item_id not present in query params"),
            }

        response = _client.get_item(TableName=table_name, Key={"id": {"S": item_id}})
        return {
            "statusCode": 200,
            "body": json.dumps({"message": response}),
        }

    # if something goes wrong return error
    except Exception as e:
        print(e)  # log to cloudwatch
        return {"statusCode": 500, "body": json.dumps(e)}
