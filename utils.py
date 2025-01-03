from elasticsearch import Elasticsearch
import boto3
import mysql.connector
from datetime import datetime
from config import *

# Conexão com Elasticsearch
es = Elasticsearch([ELASTICSEARCH_HOST])

# Conexão com DynamoDB
session = boto3.Session(
    aws_access_key_id=AWS_ACCESS_KEY_ID,
    aws_secret_access_key=AWS_SECRET_ACCESS_KEY,
    region_name=DYNAMODB_REGION
)
dynamodb = session.resource('dynamodb')
table_dynamodb = dynamodb.Table(DYNAMODB_TABLE_NAME)

# Conexão com MySQL
mysql_conn = mysql.connector.connect(
    host=MYSQL_HOST,
    user=MYSQL_USER,
    password=MYSQL_PASSWORD,
    database=MYSQL_DATABASE
)

#Function para consulta no ElasticSearch
def search_elasticsearch(index, start_date, end_date):
    # Verificar formato das datas
    try:
        start_date = datetime.strptime(start_date, "%Y-%m-%d")
        end_date = datetime.strptime(end_date, "%Y-%m-%d")
    except ValueError:
        raise ValueError("Date format should be YYYY-MM-DD")

    # Construir query Elasticsearch
    query = {
        "query": {
            "range": {
                "date": {  # Substitua "date" pelo nome do campo de data no seu índice
                    "gte": start_date.strftime("%Y-%m-%d"),
                    "lte": end_date.strftime("%Y-%m-%d")
                }
            }
        }
    }

    response = es.search(index=index, body=query)
    results = [hit['_source'] for hit in response['hits']['hits']]
    return results

# Função para criar item no DynamoDB
def create_item(table, body):
    dynamodb = boto3.resource('dynamodb')
    tbl = dynamodb.Table(table)
    tbl.put_item(Item=body)

#Function para consulta no DynamoDB
def get_item_from_dynamodb(key, value):
    try:
        response = table_dynamodb.get_item(Key={key: value})
        item = response.get('Item', {})
        if not item:
            raise ValueError("Item not found")
        return item
    except Exception as e:
        raise e

#Function para consulta no MySQL
def get_item_from_mysql(column, value):
    cursor = mysql_conn.cursor(dictionary=True)
    try:
        query = f"SELECT * FROM {MYSQL_TABLE_NAME} WHERE {column} = %s"
        cursor.execute(query, (value,))
        result = cursor.fetchone()
        cursor.close()
        
        if not result:
            raise ValueError("Item not found")
        return result
    except Exception as e:
        cursor.close()
        raise e

#Function para insert no MySQL
def insert_record_mysql(config, table, data):
    try:
        # Conectar ao banco de dados
        connection = mysql.connector.connect(**config)
        cursor = connection.cursor()

        # Construir a query de inserção
        columns = ', '.join(data.keys())
        placeholders = ', '.join(['%s'] * len(data))
        query = f"INSERT INTO {table} ({columns}) VALUES ({placeholders})"

        # Executar a query
        cursor.execute(query, tuple(data.values()))
        connection.commit()

        # Retornar o ID do registro inserido
        return cursor.lastrowid
    except mysql.connector.Error as err:
        raise Exception(f"Erro ao inserir no MySQL: {err}")
    finally:
        # Fechar conexões
        if cursor:
            cursor.close()
        if connection:
            connection.close()

def update_record_mysql(config, table, record_id, update_data):
    try:
        # Conectar ao banco de dados
        connection = mysql.connector.connect(**config)
        cursor = connection.cursor()

        # Construir a query de atualização
        set_clause = ', '.join([f"{col} = %s" for col in update_data.keys()])
        query = f"UPDATE {table} SET {set_clause} WHERE id = %s"

        # Executar a query
        cursor.execute(query, tuple(update_data.values()) + (record_id,))
        connection.commit()

        # Retornar o número de linhas afetadas
        return cursor.rowcount
    except mysql.connector.Error as err:
        raise Exception(f"Erro ao atualizar no MySQL: {err}")
    finally:
        # Fechar conexões
        if cursor:
            cursor.close()
        if connection:
            connection.close()

def delete_record_mysql(config, table, record_id):
    try:
        # Conectar ao banco de dados
        connection = mysql.connector.connect(**config)
        cursor = connection.cursor()

        # Construir a query de deleção
        query = f"DELETE FROM {table} WHERE id = %s"

        # Executar a query
        cursor.execute(query, (record_id,))
        connection.commit()

        # Retornar o número de linhas afetadas
        return cursor.rowcount
    except mysql.connector.Error as err:
        raise Exception(f"Erro ao deletar no MySQL: {err}")
    finally:
        # Fechar conexões
        if cursor:
            cursor.close()
        if connection:
            connection.close()
