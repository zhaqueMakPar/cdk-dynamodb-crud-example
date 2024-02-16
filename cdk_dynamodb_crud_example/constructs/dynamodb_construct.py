import aws_cdk as _cdk
from aws_cdk import aws_dynamodb as _dynamodb
from constructs import Construct


class DynamoDBConstruct(Construct):
    def __init__(self, scope: Construct, id_: str, **kwargs):
        super().__init__(scope, id_, **kwargs)

        self.dynamodb_table = _dynamodb.TableV2(
            self,
            "DynamoDBTable",
            table_name="my-table",
            removal_policy=_cdk.RemovalPolicy.DESTROY,
            partition_key=_dynamodb.Attribute(
                name="id", type=_dynamodb.AttributeType.STRING
            ),
        )
