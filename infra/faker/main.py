from flask import Flask
# from flask_cors import CORS
from routes.api import api
import logging
import os

def create_app():
    """Cria e configura a aplicação Flask"""
    app = Flask(__name__)
    
    # CORS(app)
    
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        handlers=[
            logging.StreamHandler(),
            logging.FileHandler('app.log')
        ]
    )
    
    app.register_blueprint(api)
    
    return app

if __name__ == '__main__':
    app = create_app()
    port = int(os.environ.get('PORT', 3001))
    debug = os.environ.get('FLASK_DEBUG', 'true').lower() == 'true'
    
    app.run(
        host='0.0.0.0',
        port=port,
        debug=debug
    )