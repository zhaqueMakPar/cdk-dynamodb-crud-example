import aws_cdk as core
import aws_cdk.assertions as assertions

from cdk_dynamodb_crud_example.cdk_dynamodb_crud_example_stack import CdkDynamodbCrudExampleStack

# example tests. To run these tests, uncomment this file along with the example
# resource in cdk_dynamodb_crud_example/cdk_dynamodb_crud_example_stack.py
def test_sqs_queue_created():
    app = core.App()
    stack = CdkDynamodbCrudExampleStack(app, "cdk-dynamodb-crud-example")
    template = assertions.Template.from_stack(stack)

#     template.has_resource_properties("AWS::SQS::Queue", {
#         "VisibilityTimeout": 300
#     })
