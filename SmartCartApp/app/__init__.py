from flask import Flask

server = Flask(__name__)

from app.routes import product_routes
from app.routes import cart_routes3
from app.routes import purchase_routes
from app.routes import scraping_routes
from app.routes import analysis_routes
from app.routes import ai_routes
