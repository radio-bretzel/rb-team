import os
from flask import Flask, jsonify

from app import config, docker
from app.database import init_db
from app.docker import init_docker
from app.channel import channel

def create_app():
   """ Main application entry point """
   app = Flask(__name__)

   load_config(app)
   register_modules(app)
   register_blueprints(app)
   # register_teardown(app)

   @app.route('/')
   def hello_world():
      return 'Welcome to Radio Bretzel'

   @app.route('/networks')
   def get_docker():
      networks = []
      for network in app.docker.networks.list(names=[docker.get_source_network_name(app)]):
         networks.append(network.name)
      return jsonify(networks)

   @app.route('/source_network')
   def network():
      if hasattr(app, 'source_network'):
         return jsonify(app.source_network.name)
      else:
         return jsonify("Not Found")
   return app

def load_config(app):
   """ Load app configuration """
   env = os.environ.get('RADIO_BRETZEL_ENV', 'development')
   if env == 'development':
      app.config.from_object(config.development)
   elif env == 'test':
      app.config.from_object(config.test)
   else:
      raise ValueError('environment variable not supported ('+ env + ')')
   try:
      app.config.from_pyfile('local.py')
   except Exception as e:
      pass

def register_modules(app):
   """Activate Flask extensions and initiate external connections"""
   init_db(app)
   init_docker(app)

def register_blueprints(app):
   """Register blueprints with the Flask application."""
   app.register_blueprint(channel, url_prefix='/channel')

# def register_teardown(app):
#    """Register teardowns """
#    @app.teardown_appcontext
#    def remove_source_network(error):
#       teardown_docker(app)
