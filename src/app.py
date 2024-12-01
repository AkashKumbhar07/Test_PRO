from flask import Flask
from src.api.routes import api
from src.network.cluster import ClusterManager
import os

def create_app():
    app = Flask(__name__)
    
    # Initialize cluster manager
    node_address = os.getenv('NODE_ADDRESS')
    seed_nodes = os.getenv('SEED_NODES', '').split(',') if os.getenv('SEED_NODES') else []
    app.cluster = ClusterManager(node_address, seed_nodes) if node_address else None
    
    # Register blueprint
    app.register_blueprint(api)
    
    return app

def main():
    app = create_app()
    port = int(os.getenv('PORT', '8000'))
    app.run(host='0.0.0.0', port=port, debug=True)

if __name__ == '__main__':
    main()
