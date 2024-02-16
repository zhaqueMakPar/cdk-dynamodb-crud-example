import os
import json
import boto3

cognito_idp_client = boto3.client("cognito-idp")
dynamo_db_client = boto3.resource("dynamodb")

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

        body = json.loads(event["body"])

        # get the item_id from the body of the request, return an error if name not present
        item_id = body.get("item_id")
        if not item_id:
            return {"statusCode": 400, "body": json.dumps("item_id is required")}

        # get the new_name from the body of the request, return an error if name not present
        new_name = body.get("new_name")
        if not new_name:
            return {"statusCode": 400, "body": json.dumps("new_name is required")}

        response = _client.update_item(
            TableName=table_name,
            Key={"id": {"S": item_id}},
            UpdateExpression="SET #n = :val",
            ExpressionAttributeNames={"#n": "name"},
            ExpressionAttributeValues={":val": {"S": new_name}},
            ReturnValues="ALL_NEW",
        )
        return {"statusCode": 200, "body": json.dumps({"message": response})}

    # if something goes wrong return error
    except Exception as e:
        print(e)  # log to cloudwatch
        return {"statusCode": 500, "body": json.dumps(e)}
