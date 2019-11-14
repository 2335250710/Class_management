from utils.functions import create_app

from flask_script import Manager
from models.models import db
from flask_migrate import Migrate, MigrateCommand

app = create_app()
db.init_app(app=app)
migrate = Migrate(app, db)
manager = Manager(app)
manager.add_command('db', MigrateCommand)

if __name__ == '__main__':
    manager.run()
