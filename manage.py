#!venv/bin/python
import os
from app import create_app, db
from app.models import User, Follow, Role, Permission, Post
from flask_script import Manager, Shell, prompt_bool
from flask_migrate import Migrate, MigrateCommand
from flask_debugtoolbar import DebugToolbarExtension

app = create_app(os.getenv('FLASK_CONFIG') or 'default')
app.debug = True
manager = Manager(app)
migrate = Migrate(app, db)

toolbar = DebugToolbarExtension(app)

def make_shell_context():
    return dict(app=app, db=db, User=User, Role=Role)
manager.add_command("shell", Shell(make_context=make_shell_context))
manager.add_command('db', MigrateCommand)


@manager.command
def test():
    """Run the unit tests."""
    import unittest
    tests = unittest.TestLoader().discover('tests')
    unittest.TextTestRunner(verbosity=2).run(tests)

@manager.command
def deploy():
    """Run deployment tasks."""
    # migrate database to latest revision
    upgrade()

    # create or update user roles
    Role.insert_roles()

    # ensure all users are following themselves
    User.add_self_follows()

@manager.command
def dropdb():
    if prompt_bool('Are you sure you eant to lose all your data'):
        db.drop_all()
        
if __name__ == '__main__':
    manager.run()
