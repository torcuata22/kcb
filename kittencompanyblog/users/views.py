from flask import render_template, url_for, flash, redirect, request, Blueprint
from flask_login import login_user, current_user, logout_user, login_required
from kittencompanyblog import db #grabs db from __init__.py
from kittencompanyblog.models import User, BlogPost
from kittencompanyblog.users.forms import RegistrationForm, LoginForm, UpdateUserForm
from kittencompanyblog.users.picture_handler import add_profile_pic


users = Blueprint('users', __name__)

#register view
@users.route('/register', methods = ['GET','POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(email = form.email.data,
                    username = form.username.data,
                    password = form.password.data)
        
        db.session.add(user)
        db.session.commit()
        flash("Thanks for registering!")
        return redirect(url_for('users.login'))
    return render_template('register.html', form=form)


#login view
@users.route('/login', methods = ['GET','POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email = form.email.data).first()
        if user.check_password(form.password.data) and user is not None:
            login_user(user)
            flash("Login successful")

            next = request.args.get('next')
            if next == None or not next[0] == '/':
                next = url_for('core.index')

            return redirect('next')
        return render_template('login.html', form = form)

#logout view
@users.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('core.index'))

#show account (update user?)
#show all of user's blogposts (list)