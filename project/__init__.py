import json
import datetime

from flask import Flask
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

with open("config.json") as config:
    config = json.load(config)

app = Flask(__name__)

app.secret_key = config["web"]["secret-key"]
app.config['PERMANENT_SESSION_LIFETIME'] = datetime.timedelta(days=7)

db_host, db_user, db_password, schema, db_port = config["database"]["hostname"], config["database"]["user"], \
    config["database"]["password"], config["database"]["schema"], config["database"]["port"]

engine = create_engine(f"mysql+pymysql://{db_user}:{db_password}@{db_host}:{db_port}/{schema}")
Session = sessionmaker(bind=engine)

db = Session()
Base = declarative_base()

from project import routes
from project import models
