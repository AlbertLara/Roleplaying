from .admin import blueprint as admin_blueprint
from .auth import blueprint as auth_blueprint
from .friends import blueprint as friend_blueprint
from .groups import blueprint as group_blueprint
from .home import blueprint as home_blueprint
from .. import app

app.register_blueprint(home_blueprint)
app.register_blueprint(auth_blueprint)
app.register_blueprint(admin_blueprint)
app.register_blueprint(group_blueprint)
app.register_blueprint(friend_blueprint)