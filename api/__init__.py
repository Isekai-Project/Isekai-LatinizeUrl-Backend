from flask import Blueprint
import importlib
import config

api_blue = Blueprint('api', __name__)

for module in config.API_MODULES:
    importlib.import_module(".controller." + module, __package__)