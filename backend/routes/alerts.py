from flask import Blueprint, request, jsonify
from datetime import datetime
from bson import json_util, ObjectId
import json
from extensions import mongo
from flask_jwt_extended import jwt_required

alerts = Blueprint('alerts', __name__)

@alerts.route('/alerts', methods=['POST'])
def create_alert():
    data = request.json
    alert_data = {
        'title': data['title'],
        'message': data['message'],
        'severity': data['severity'],
        'source': data['source'],
        'timestamp': datetime.utcnow(),
        'acknowledged': False
    }
    result = mongo.db.alerts.insert_one(alert_data)
    return jsonify({'message': 'Alert created', 'id': str(result.inserted_id)}), 201

@alerts.route('/alerts', methods=['GET'])
@jwt_required()
def get_alerts():
    # Query parameters for filtering
    severity = request.args.get('severity')
    acknowledged = request.args.getlist('acknowledged')
    
    query = {}
    if severity:
        query['severity'] = severity
    if acknowledged:
        query['acknowledged'] = acknowledged[0].lower() == 'true'
    
    alerts = mongo.db.alerts.find(query).sort('timestamp', -1)
    return json.loads(json_util.dumps(list(alerts)))

@alerts.route('/alerts/<alert_id>/acknowledge', methods=['PUT'])
@jwt_required()
def acknowledge_alert(alert_id):
    result = mongo.db.alerts.update_one(
        {'_id': ObjectId(alert_id)},
        {'$set': {'acknowledged': True}}
    )
    
    if result.modified_count:
        return jsonify({'message': 'Alert acknowledged successfully'})
    return jsonify({'message': 'Alert not found'}), 404