from flask import render_template, session, redirect, url_for, flash
from flask_login import login_required, current_user
from . import main
from .forms import RegisterFalcon
from .. import db
from ..models import Permission, User, Role
from app.decorators import admin_required


@main.route('/', methods=['GET', 'POST'])
def index():
    form = RegisterFalcon()
    return render_template('index.html', current_time=datetime.utcnow(), form=form)