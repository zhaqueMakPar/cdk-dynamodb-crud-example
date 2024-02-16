import aws_cdk as _cdk
from aws_cdk import aws_apigateway as _gateway
from aws_cdk import aws_lambda as _lambda
from constructs import Construct

from cdk_dynamodb_crud_example.constructs.dynamodb_construct import DynamoDBConstruct
from cdk_dynamodb_crud_example.constructs.gateway_construct import APIGatewayConstruct


class LambdaConstruct(Construct):
    def __init__(
        self,
        scope: Construct,
        id_: str,
        __table: DynamoDBConstruct,
        __gateway: APIGatewayConstruct,
        **kwargs,
    ):
        super().__init__(scope, id_, **kwargs)

        LAMBDA_PATH = "cdk_dynamodb_crud_example/lambda-handler"

        __table_name = __table.dynamodb_table.table_name

        # lambda definitions
        self.dynamodb_create_lambda = _lambda.Function(
            self,
            "DynamoDBCreate",
            runtime=_lambda.Runtime.PYTHON_3_10,
            handler="create.handler",
            code=_lambda.Code.from_asset(LAMBDA_PATH),
            timeout=_cdk.Duration.seconds(180),
            environment={
                "TABLE_NAME": __table_name,  # set table name as an enviroment variable to access in lambda code
            },
        )

        self.dynamodb_read_lambda = _lambda.Function(
            self,
            "DynamoDBRead",
            runtime=_lambda.Runtime.PYTHON_3_10,
            handler="read.handler",
            code=_lambda.Code.from_asset(LAMBDA_PATH),
            timeout=_cdk.Duration.seconds(180),
            environment={
                "TABLE_NAME": __table_name,
            },
        )

        self.dynamodb_update_lambda = _lambda.Function(
            self,
            "DynamoDBUpdate",
            runtime=_lambda.Runtime.PYTHON_3_10,
            handler="update.handler",
            code=_lambda.Code.from_asset(LAMBDA_PATH),
            timeout=_cdk.Duration.seconds(180),
            environment={
                "TABLE_NAME": __table_name,
            },
        )

        self.dynamodb_delete_lambda = _lambda.Function(
            self,
            "DynamoDBDelete",
            runtime=_lambda.Runtime.PYTHON_3_10,
            handler="delete.handler",
            code=_lambda.Code.from_asset(LAMBDA_PATH),
            timeout=_cdk.Duration.seconds(180),
            environment={
                "TABLE_NAME": __table_name,
            },
        )

        # grant permissions to lambda to read/write to dynamodb table
        __table.dynamodb_table.grant_write_data(self.dynamodb_create_lambda)
        __table.dynamodb_table.grant_write_data(self.dynamodb_update_lambda)
        __table.dynamodb_table.grant_write_data(self.dynamodb_delete_lambda)
        __table.dynamodb_table.grant_read_data(self.dynamodb_read_lambda)

        # endpoint definitions + lambda integration with gateway
        create_endpoint = __gateway.gateway_instance.root.add_resource("create")
        create_endpoint.add_method(
            "POST",
            _gateway.LambdaIntegration(
                handler=self.dynamodb_create_lambda,
                proxy=True,
            ),
        )

        read_endpoint = __gateway.gateway_instance.root.add_resource("read")
        read_endpoint.add_method(
            "GET",
            _gateway.LambdaIntegration(
                handler=self.dynamodb_read_lambda,
                proxy=True,
            ),
        )

        update_endpoint = __gateway.gateway_instance.root.add_resource("update")
        update_endpoint.add_method(
            "PUT",
            _gateway.LambdaIntegration(
                handler=self.dynamodb_update_lambda,
                proxy=True,
            ),
        )

        delete_endpoint = __gateway.gateway_instance.root.add_resource("delete")
        delete_endpoint.add_method(
            "DELETE",
            _gateway.LambdaIntegration(
                handler=self.dynamodb_delete_lambda,
                proxy=True,
            ),
        )
