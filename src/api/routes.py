from flask import Blueprint, request, jsonify, current_app
from src.store.store import DistributedStore

api = Blueprint('api', __name__)
store = DistributedStore()

@api.route('/kv/<key>', methods=['PUT'])
def create(key):
    value = request.json.get('value')
    if value is None:
        return jsonify({'error': 'Value is required'}), 400
    
    success = store.create(key, value)
    if success:
        if current_app.cluster:
            current_app.cluster.broadcast_update(key, value, 'create')
        return jsonify({'status': 'created'}), 201
    return jsonify({'error': 'Key already exists'}), 409

@api.route('/kv/<key>', methods=['GET'])
def read(key):
    value = store.read(key)
    if value is None:
        return jsonify({'error': 'Key not found'}), 404
    return jsonify({'value': value}), 200

@api.route('/kv/<key>', methods=['DELETE'])
def delete(key):
    success = store.delete(key)
    if success:
        if current_app.cluster:
            current_app.cluster.broadcast_update(key, None, 'delete')
        return jsonify({'status': 'deleted'}), 200
    return jsonify({'error': 'Key not found'}), 404
