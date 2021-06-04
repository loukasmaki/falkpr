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
    
    return render_template('index.html')

@main.route('/registrera', methods=['GET', 'POST'])
@login_required
def registrera_falk():
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
            dagar_17 = form.dagar_17.data,
            kräva = form.kräva.data,
            foto = form.foto.data,
            märkare = form.märkare.data,
            lokal_id = form.plats.data.id,
            ringmärkt_datum = form.datum.data,
            #påse = form.påse.data,
            #närvarande = form.närvarande.data,
            #duvringar = form.duvringar.data,
            övrigt = form.övrigt.data,
        )
        db.session.add(falk)
        db.session.commit()
        return redirect(url_for('main.registrera_falk'))
        
        flash('Falk Registrerad')
    return render_template('registrera_falk.html', form=form)

@main.route('/falkar', methods=['GET'])
@login_required
def falkar():
    falkar = Falk.query.order_by(Falk.id).all()
    return render_template('falkar.html', falkar=falkar)