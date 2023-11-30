from aws_cdk import (
    Stack,
    aws_certificatemanager as acm,
    aws_route53 as route53,
    aws_cognito as cognito,
    aws_apigateway as apigateway,
    aws_lambda as _lambda,
    aws_route53_targets as targets,
    aws_secretsmanager as secretsmanager,
    RemovalPolicy as RemovalPolicy,
    SecretValue as SecretValue
)
    
from constructs import Construct
import string
import random

class AwsMongodbSampleStack(Stack):

    def __init__(self, scope: Construct, construct_id: str, atlas_uri : str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        # The code that defines your stack goes here

        env_name = "dev"
        secretname = "ATLAS_URI3"
        
        # Create a new secret in Secrets Manager and fetch the ARN
        mySecret = secretsmanager.Secret(self, "Secret", secret_name = secretname, secret_string_value = SecretValue.unsafe_plain_text(atlas_uri))

        secretarn = mySecret.secret_arn
        
        generated_name = mySecret.secret_name
        
        # Create a user pool
        user_pool = cognito.UserPool(self, "SampleUserPool",
                                    user_pool_name="mysample-userpool",
                                    sign_in_case_sensitive=False, 
                                    sign_in_aliases=cognito.SignInAliases(
                                                    username=True,
                                                    email=True),
                                    self_sign_up_enabled= True
                                    )
         
        # using random.choices()
        # generating random strings
        res = ''.join(random.choices(string.ascii_lowercase +
                             string.digits, k=7))
                             
        # Create domain prefix here                            
        user_pool.add_domain("CognitoDomain", 
        cognito_domain=cognito.CognitoDomainOptions(domain_prefix ="mysample-app" + str(res))
        )
        
        auth = apigateway.CognitoUserPoolsAuthorizer(self, "apiAuthorizer",
                                                     cognito_user_pools=[user_pool])
    
        # Create a lambda function
        lambdahandler = _lambda.Function(
            self,
            "ApiHandler",
             environment= {
                            "PYTHONPATH" : "dependencies",
                            "ENV": env_name ,
                            "ATLAS_URI": generated_name
                          },
            runtime=_lambda.Runtime.PYTHON_3_11,
            handler="lambda_function.lambda_handler",
            code=_lambda.Code.from_asset("aws_mongodb_sample"),
           
        )
        
        secret = secretsmanager.Secret.from_secret_attributes(self, secretname, 
        secret_complete_arn=secretarn)
        
        secret.grant_read(grantee=lambdahandler)
        

        # Create an API Gateway
        api = apigateway.LambdaRestApi(
            self,
            "ApiGateway",
            default_method_options={
                                     "authorizer": auth, 
                                     "authorization_type": apigateway.AuthorizationType.COGNITO},
            handler=lambdahandler,
            deploy_options = apigateway.StageOptions(stage_name = env_name),
            default_cors_preflight_options=apigateway.CorsOptions(
                allow_origins=apigateway.Cors.ALL_ORIGINS,
                allow_methods=apigateway.Cors.ALL_METHODS),
            proxy=False
            )
            
        api.root.add_method('GET')

        
        #add callback urls
        callbackUrls = [] 
        callbackUrls.append(api.url)

        read_only_scope = cognito.ResourceServerScope(scope_name="read", scope_description="Read-only access")
        # for full access 
        # full_access_scope = cognito.ResourceServerScope(scope_name="*", scope_description="Full access")

        user_server = user_pool.add_resource_server("ResourceServer",
        identifier="users",
        scopes=[read_only_scope])
        
        poolClient = user_pool.add_client(env_name + '_Test_AppClient', 
            auth_flows=cognito.AuthFlow(user_password=True,user_srp=True),
            o_auth=cognito.OAuthSettings(flows=cognito.OAuthFlows(authorization_code_grant=True),
            scopes=[cognito.OAuthScope.resource_server(user_server, read_only_scope)],
            callback_urls= callbackUrls)
        );
        
