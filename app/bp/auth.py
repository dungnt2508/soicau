import requests
from flask import render_template, request, redirect, url_for, flash, g, session, abort
from flask_login import login_user, logout_user, login_required, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from . import bp
from ..db import save_user, get_user
from ..models import User

import os
import pathlib
from google.oauth2 import id_token
from google_auth_oauthlib.flow import Flow
from pip._vendor import cachecontrol
import google.auth.transport.requests

GOOGLE_CLIENT_ID = "857580301880-q74aeqijs3bg6vpgplti5qh4fq8a3hel.apps.googleusercontent.com"
client_secrets_file = os.path.join(pathlib.Path(__file__).parent, "client_secret.json")
flow = Flow.from_client_secrets_file(
    client_secrets_file=client_secrets_file,
    scopes=["https://www.googleapis.com/auth/userinfo.profile", "https://www.googleapis.com/auth/userinfo.email",
            "openid"],
    redirect_uri="http://127.0.0.1:5000/callback"
)

"""Authen & Author"""



@bp.route('/login')
def login():
    return render_template('login.html')


@bp.route('/login', methods=['POST'])
def login_post():
    email = request.form.get("email")
    password = request.form.get("password")
    remember = True if request.form.get("remember") else False
    # print(remember)

    if len(email) == 0:
        flash('Email không được để trống')
    if len(password) == 0:
        flash('Mật khẩu không được để trống')

    user = get_user(email)

    if not user:
        flash("Email không tồn tại !")
        return redirect(url_for('bp.login'))
    if not check_password_hash(user.password, password):
        flash("Sai mật khẩu !")
        return redirect(url_for('bp.login'))

    # print(user)

    login_user(user, remember)

    session["email"] = email

    return redirect(url_for('bp.go88_sicbomd5'))


@bp.route("/login_google")
def login_google():
    authorization_url, state = flow.authorization_url()
    session["state"] = state
    return redirect(authorization_url)


@bp.route("/callback")
def callback():
    flow.fetch_token(authorization_response=request.url)
    if not session["state"] == request.args["state"]:
        abort(500)  # State does not match!

    credentials = flow.credentials
    request_session = requests.session()
    cached_session = cachecontrol.CacheControl(request_session)
    token_request = google.auth.transport.requests.Request(session=cached_session)

    id_info = id_token.verify_oauth2_token(
        id_token=credentials._id_token,
        request=token_request,
        audience=GOOGLE_CLIENT_ID
    )

    session["email"] = id_info.get("email")
    session["google_id"] = id_info.get("sub")
    session["name"] = id_info.get("name")
    user = User(session["email"], session["name"], '')
    login_user(user, remember=False, force=True)

    return redirect(url_for('bp.go88_sicbomd5'))


@bp.route('/signup')
def signup():
    return render_template('signup.html')


@bp.route('/signup', methods=['POST'])
def signup_post():
    fullname = request.form.get('fullname')
    email = request.form.get('email')
    password = request.form.get('password')
    re_password = request.form.get('re_password')

    user = get_user(email)  # check user

    if user:
        flash('Email đã tồn tại !')
        return redirect(url_for('bp.signup'))

    new_user = {'email': email, 'fullname': fullname, 'password': generate_password_hash(password, method='pbkdf2:sha256')}

    save_user(new_user)

    return redirect(url_for('bp.login'))


@bp.route('/logout')
@login_required
def logout():
    session.clear()
    logout_user()
    return render_template('login.html')

