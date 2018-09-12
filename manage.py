#!venv/bin/python
import os
from app import create_app, db
from app.models import User, Follow, Role, Permission, Post, Comment
from flask_script import Manager, Shell, prompt_bool
from flask_migrate import Migrate, MigrateCommand
from flask_debugtoolbar import DebugToolbarExtension

from flask import url_for, redirect
from flask_admin import Admin, expose, AdminIndexView
from flask_admin.contrib.sqla import ModelView
from flask_admin import helpers, expose
from flask_admin.base import MenuLink
from flask_admin.contrib.fileadmin import FileAdmin
from flask_login import current_user

app = create_app(os.getenv('FLASK_CONFIG') or 'default')
app.debug = True
manager = Manager(app)
migrate = Migrate(app, db)

#toolbar = DebugToolbarExtension(app)

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

# Create customized model view class
class MyModelView(ModelView):

    def is_accessible(self):
        return current_user.is_authenticated


# Create customized index view class that handles login & registration
class MyAdminIndexView(AdminIndexView):

    @expose('/')
    def index(self):
        if not current_user.is_authenticated:
            return redirect(url_for('auth.login'))
        if not current_user.username=='chendamowang':
            return redirect(url_for('main.index'))
        return super(MyAdminIndexView, self).index()

# Create admin
admin = Admin(app, 'admin', template_mode='bootstrap3', index_view=MyAdminIndexView())

# Add view
admin.add_view(MyModelView(User, db.session))
admin.add_view(MyModelView(Post, db.session))
admin.add_view(MyModelView(Comment, db.session))
admin.add_view(MyModelView(Role, db.session))
admin.add_view(MyModelView(Follow, db.session))
path = os.path.join(os.path.dirname(__file__), 'app/static')
admin.add_view(FileAdmin(path, '/static/', name='Static Files'))

admin.add_link(MenuLink(name='Back Home', url='/'))
        
if __name__ == '__main__':
    manager.run()
