
from botocore.exceptions import ClientError
import boto3
import ast


def get_secret():

    secret_name = "database_credentials"
    region_name = "eu-west-2"

    # Create a Secrets Manager client
    session = boto3.session.Session()
    client = session.client(
        service_name='secretsmanager',
        region_name=region_name
    )

    try:
        get_secret_value_response = client.get_secret_value(
            SecretId=secret_name
        )
    except ClientError as e:
        raise e

    return ast.literal_eval(get_secret_value_response['SecretString'])


# secret_dict = get_secret()

# hostname = secret_dict['hostname']
# database_name = secret_dict['database_name']
# username = secret_dict['username']
# password = secret_dict['password']
# port = secret_dict['port']
