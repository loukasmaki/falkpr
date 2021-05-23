from flask import render_template, session, redirect, url_for, flash
from flask_login import login_required, current_user
from . import main
from .forms import RegistreraFalk
from .. import db
from ..models import Permission, User, Role, Falk
from app.decorators import admin_required
from datetime import datetime

@main.route('/', methods=['GET', 'POST'])
#@login_required
def index():
    form = RegistreraFalk()
    if form.validate_on_submit():
        falk = Falk(
            vikt = form.vikt.data,
            kön = form.kön.data,
            hb = form.hb.data,
            vb = form.vb.data,
            hp10 = form.hp10.data,
            hp7 = form.hp7.data,
            sp = form.sp.data,
            ålder = form.ålder.data,
            kräva = form.kräva.data,
            foto = form.foto.data,
            märkare = form.märkare.data,
            övrigt = form.övrigt.data,
            lokal_id = form.plats.data,
        )
        db.session.add(falk)
        db.session.commit()
        return redirect(url_for('auth.login'))

        flash('Falk Registrerad')
    return render_template('index.html', current_time=datetime.utcnow(), form=form)