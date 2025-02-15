from flask import render_template, session
from flask_login import login_required, current_user
from . import bp
from ..db import get_predict_sicbomd5, get_lastid

"""content"""


@bp.route('/')
def home():
    return render_template('home.html')


@bp.route('/chatbot')
@login_required
def chatbot():
    return render_template('chatbot.html')

@bp.route('/go88_sicbomd5')
@login_required
def go88_sicbomd5():
    return render_template('go88_sicbomd5.html')


@bp.route('/sicbomd5/lastid_get')
# @login_required
def lastid_get():
    return get_lastid()

@bp.route('/sicbomd5/predict')
# @login_required
def predict_sicbomd5_get():
    print('zo')
    return get_predict_sicbomd5(1)

@bp.route('/sicbomd5/predict_v2')
# @login_required
def predict_sicbomd5_get_v2():
    return get_predict_sicbomd5(2)