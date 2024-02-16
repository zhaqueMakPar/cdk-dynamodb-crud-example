import aws_cdk as cdk

from cdk_dynamodb_crud_example.cdk_dynamodb_crud_example_stack import (
    CdkDynamodbCrudExampleStack,
)


app = cdk.App()
CdkDynamodbCrudExampleStack(app, "CdkDynamodbCrudExampleStack")

app.synth()
