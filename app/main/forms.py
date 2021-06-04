from flask_wtf import FlaskForm
from wtforms import StringField, SelectField, BooleanField, DecimalField, IntegerField, TextAreaField, SubmitField, DateTimeField
from wtforms.validators import DataRequired, Length, Regexp, EqualTo
from wtforms import ValidationError
from wtforms.fields.html5 import DateField
from ..models import User, Role, Lokal
from wtforms.ext.sqlalchemy.fields import QuerySelectField
from .. import db

class RegistreraFalk(FlaskForm):

    def hitta_lokaler():
        return db.session.query(Lokal).all()



    vikt = IntegerField('Vikt i gram', validators=[DataRequired(),] )
    kön = SelectField('Kön', choices=[('M'), ('F')])
    hb = StringField('Höger ben', validators=[DataRequired()] )
    vb = StringField('Vänster ben', validators=[DataRequired()])
    hp10 = DecimalField('hp10', validators=[DataRequired()])
    hp7 = DecimalField('hp7', validators=[DataRequired()])
    sp = DecimalField('sp', validators=[DataRequired()])
    dagar_17 = DecimalField('17 dagar', validators=[DataRequired()])
    kräva = SelectField('Kräva', choices=[('Tom'), ('Halvfull'), ('Full')])
    foto = StringField('Foto, angiven kamera med foton', validators=[DataRequired()])
    märkare = StringField('Märkare', validators=[DataRequired()])
    övrigt = TextAreaField('Övrigt')
    plats = QuerySelectField('Plats', validators=[DataRequired()], query_factory=hitta_lokaler)
    #plats = StringField('Plats', validators=[DataRequired()])
    datum = DateField('Datum', format='%Y-%m-%d', validators=[DataRequired()])
    #påse = StringField('Påse')
    #närvarande = StringField('Närvarande')
    #duvringar = BooleanField('Duvringar')
    submit = SubmitField('Submit')