from flask import Blueprint, request, jsonify
from datetime import datetime, timedelta
from bson import json_util
import json
from extensions import mongo

metrics = Blueprint('metrics', __name__)

@metrics.route('/metrics', methods=['POST'])
def add_metrics():
    data = request.json
    metrics_data = {
        'host_name': data['host_name'],
        'cpu_usage': data['cpu_usage'],
        'memory_usage': data['memory_usage'],
        'disk_usage': data['disk_usage'],
        'timestamp': datetime.utcnow()
    }
    mongo.db.metrics.insert_one(metrics_data)
    return jsonify({'message': 'Metrics recorded successfully'}), 201

@metrics.route('/metrics/<host_name>', methods=['GET'])
def get_host_metrics(host_name):
    # Get time range from query parameters (default to last 24 hours)
    hours = int(request.args.get('hours', 24))
    since = datetime.utcnow() - timedelta(hours=hours)
    
    query = {
        'host_name': host_name,
        # 'timestamp': {'$gte': since}
    }
    print(f"Executing Query: {query}")
    
    metrics = mongo.db.metrics.find(query)
    metrics_list = list(metrics)
    print(f"Query Results: {metrics_list}")
    
    return json.loads(json_util.dumps(metrics_list))