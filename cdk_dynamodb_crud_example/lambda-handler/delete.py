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
                "body": json.dumps("TABLE_NAME environment variable is not set"),
            }

        # get the item_id from the body of the request, return an error if name not present
        body = json.loads(event["body"])
        item_id = body.get("item_id")
        if not item_id:
            return {"statusCode": 400, "body": json.dumps("item_id is required")}

        response = _client.delete_item(TableName=table_name, Key={"id": {"S": item_id}})
        return {
            "statusCode": 200,
            "body": json.dumps(
                {"message": item_id + " deleted", "db_message": response}
            ),
        }

    # if something goes wrong return error
    except Exception as e:
        print(e)  # log to cloudwatch
        return {"statusCode": 500, "body": json.dumps(e)}
