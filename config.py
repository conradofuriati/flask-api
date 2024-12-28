import os

# Configurações para DynamoDB
DYNAMODB_REGION = os.getenv('DYNAMODB_REGION', 'us-west-2')
DYNAMODB_TABLE_NAME = os.getenv('DYNAMODB_TABLE_NAME', 'YourDynamoDBTableName')

# Credenciais AWS
AWS_ACCESS_KEY_ID = os.getenv('AWS_ACCESS_KEY_ID')
AWS_SECRET_ACCESS_KEY = os.getenv('AWS_SECRET_ACCESS_KEY')

# Configurações para Elasticsearch
ELASTICSEARCH_HOST = os.getenv('ELASTICSEARCH_HOST', 'http://localhost:9200')

# Configurações para MySQL
MYSQL_HOST = os.getenv('MYSQL_HOST', 'localhost')
MYSQL_DATABASE = os.getenv('MYSQL_DATABASE', 'my_database')
MYSQL_USER = os.getenv('MYSQL_USER', 'my_user')
MYSQL_PASSWORD = os.getenv('MYSQL_PASSWORD', 'my_password')
MYSQL_TABLE_NAME = os.getenv('MYSQL_TABLE_NAME', 'dados') #your_mysql_table_name
