
from weatherapp.users.forms import RegistrationForm, LoginForm, UserUpdateForm
from weatherapp.models import User
from weatherapp import bcrypt, db
from flask_login import login_user, current_user, logout_user, login_required
from flask import render_template, flash, redirect, url_for, request, Blueprint


users = Blueprint('users', __name__)
@users.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember.data)
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for('main.home'))
        else:
            flash('Login unsuccessful!', 'danger')
    return render_template('login.html', form=form)


@users.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('main.home'))


@users.route('/account', methods=['GET', 'POST'])
@login_required
def account():
    country = current_user.country
    form = UserUpdateForm(country=country)
    if form.validate_on_submit():
        current_user.username = form.username.data
        current_user.email = form.email.data
        current_user.country = form.country.data
        db.session.commit()
        flash("Your account has been updated!", 'success')
        return redirect(url_for('users.account'))
    elif request.method == 'GET':
        form.username.data = current_user.username
        form.email.data = current_user.email
        form.country.data = current_user.country
    return render_template('account.html', form=form)


@users.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))
    form = RegistrationForm()
    if form.validate_on_submit():
        password_hash = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(username=form.username.data, email=form.email.data, country=form.country.data, password=password_hash)
        db.session.add(user)
        db.session.commit()
        print(form.country.data)
        flash(f'Your account has been created!', 'success')
        return redirect(url_for('users.login'))
    return render_template('register.html', form=form)