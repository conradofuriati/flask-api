from flask import Flask, jsonify, request
from utils import create_item, search_elasticsearch, get_item_from_dynamodb, get_item_from_mysql

app = Flask(__name__)

# Rota para inserir dados no DynamoDB
@app.route('/insert_dynamodb', methods=['POST'])
def insert_data():
    try:
        # Obter os dados do corpo da requisição
        data = request.get_json()
        if not data:
            return jsonify({'error': 'Invalid or missing JSON payload'}), 400

        # Nome da tabela DynamoDB
        table = 'table_name'

        # Inserir os dados no DynamoDB
        create_item(table, data)

        return jsonify({'message': 'Item inserted successfully'}), 201
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/get_dynamodb', methods=['GET'])
def get_from_dynamodb():
    key = request.args.get('key')
    value = request.args.get('value')
    
    if not key or not value:
        return jsonify({"error": "Missing 'key' or 'value' parameter"}), 400
    
    try:
        item = get_item_from_dynamodb(key, value)
        return jsonify(item)
    except ValueError as e:
        return jsonify({"error": str(e)}), 404
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/get_elasticsearch', methods=['GET'])
def get_from_elasticsearch():
    index = request.args.get('index')
    start_date = request.args.get('start_date')
    end_date = request.args.get('end_date')
    
    if not index or not start_date or not end_date:
        return jsonify({"error": "Missing 'index', 'start_date' or 'end_date' parameter"}), 400

    try:
        results = search_elasticsearch(index, start_date, end_date)
        return jsonify(results)
    except ValueError as e:
        return jsonify({"error": str(e)}), 400
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/get_mysql', methods=['GET'])
def get_from_mysql():
    column = request.args.get('column')
    value = request.args.get('value')
    
    if not column or not value:
        return jsonify({"error": "Missing 'column' or 'value' parameter"}), 400
    
    try:
        result = get_item_from_mysql(column, value)
        return jsonify(result)
    except ValueError as e:
        return jsonify({"error": str(e)}), 404
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
