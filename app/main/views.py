from datetime import datetime
from flask import render_template, session, redirect, url_for, abort, flash
from . import main
from .forms import NameForm
from .. import db
from ..models import User
from flask_login import login_required


@main.route('/')
def home():
    return render_template('index.html')

@main.route('/form', methods=['GET', 'POST'])
def form():
    form = NameForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.name.data).first()
        if user is None:
            user = User(username=form.name.data)
            db.session.add(user)
            session['known'] = False
        else:
            session['known'] = True

        old_name = session.get('name')
        if old_name is not None and old_name != form.name.data:
            flash('Looks like you have changed your name!')

        session['name'] = form.name.data
        form.name.data = ''
        return redirect(url_for('main.home'))
    return render_template('form.html', form=form, name=session.get('name'), known=session.get('known', False))


@main.route('/time')
@login_required
def current_time():
    return render_template('current_time.html', current_time=datetime.utcnow())
#
#
# @main.route('/aboute')
# def about():
#     return 'About.'
#
#
# @main.route('/user/<name>')
# def user(name):
#     return json.dumps({'name': name})
#
#
# @main.route('/hello_user/<name>')
# def hello_user(name):
#     return render_template('user.html', name=name)
#
#
@main.route('/error')
def error():
    abort(500)
#
#
# @main.route('/cookie')
# def cookie():
#     response = make_response('<h3>This is document carries a cookie!</h3>') # функция сохранит этот текст в куки
#     response.set_cookie('answer', '42')
#     return response
#
#
# @main.route('/redirect')
# def redirect_link():
#     return redirect('https://lenta.ru')
#
#
# @main.route('/get_user/<id>')
# def get_user(id):
#     user = load_user(id)
#     if not user:
#         abort(404)
#     return '<h3>Hello, {}</h3>'.format(user.name)
