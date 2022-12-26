import warnings
import pandas as pd
import boto3
import json
import redshift_connector

warnings.filterwarnings("ignore")

with open('/run/media/roberto/black-box/.syek/connections/secret_manager_b3.json', 'r') as file:
    cred = json.load(file)

client = boto3.client('secretsmanager', region_name='us-east-1',
aws_access_key_id= cred.get('id'),
aws_secret_access_key=cred.get('passwd'))

get_secret_value_response = client.get_secret_value(SecretId="projeto_athena_datascience")
secret = json.loads(get_secret_value_response['SecretString'])

conn = redshift_connector.connect(
    host= secret.get('host'),
    database=secret.get('database'),
    user=secret.get('user'),
    password=secret.get('password')
)

qry = input("QUERY: ")

df = pd.read_sql(qry, conn)
print(df)
