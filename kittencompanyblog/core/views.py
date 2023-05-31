from flask import render_template, request, Blueprint
from kittencompanyblog.users.views import users

core = Blueprint('core',__name__)

@core.route('/')
def index():
    return render_template('index.html', core=core, users=users)

@core.route('/info')
def info():
    return render_template('info.html', core=core, users=users)


