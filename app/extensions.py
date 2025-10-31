from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_marshmallow import Marshmallow
ma = Marshmallow()
db = SQLAlchemy()
migrate = Migrate()