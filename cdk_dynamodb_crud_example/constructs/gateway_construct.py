from constructs import Construct
from aws_cdk import aws_apigateway as _apigateway


class APIGatewayConstruct(Construct):
    def __init__(self, scope: Construct, id_: str, **kwargs):
        super().__init__(scope, id_, **kwargs)

        self.gateway_instance = _apigateway.RestApi(self, "ApiGateway")
