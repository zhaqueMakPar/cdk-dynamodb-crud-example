from aws_cdk import (
    Stack,
)
from constructs import Construct

from cdk_dynamodb_crud_example.constructs.gateway_construct import APIGatewayConstruct
from cdk_dynamodb_crud_example.constructs.dynamodb_construct import DynamoDBConstruct
from cdk_dynamodb_crud_example.constructs.lambda_construct import LambdaConstruct


class CdkDynamodbCrudExampleStack(Stack):
    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        __gateway = APIGatewayConstruct(self, "APIGateway")  # init gateway construct
        __dynamodb = DynamoDBConstruct(self, "DynamoDB")  # init dynamodb construct
        __lambdas = LambdaConstruct(
            self, "Lambdas", __dynamodb, __gateway
        )  # init lambda construct, pass dynamodb table and gateway construct as args
