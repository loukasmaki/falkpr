from flask_wtf import FlaskForm
from wtforms import StringField, SelectField, BooleanField, DecimalField, IntegerField, TextAreaField, SubmitField
from wtforms.validators import DataRequired, Length, Regexp, EqualTo
from wtforms import ValidationError
from ..models import User, Role
#from wtforms.ex.sqlalchemy.fields import QuerySelectField
from .. import db

class RegistreraFalk(FlaskForm):
    vikt = IntegerField('Vikt i gram', validators=[DataRequired(),] )
    kön = SelectField('Kön', choices=[('M'), ('F')])
    hb = StringField('Höger ben', )
    vb = StringField('Vänster ben', )
    hp10 = DecimalField('hp10', )
    hp7 = DecimalField('hp7', )
    sp = DecimalField('sp',)
    ålder = DecimalField('Ålder', )
    kräva = SelectField('Kräva', choices=[('Tom'), ('Halvfull'), ('Full')])
    foto = StringField('Foto, angiven kamera med foton')
    märkare = StringField('Märkare', )
    övrigt = TextAreaField('Övrigt')
    plats = StringField('Plats')
    submit = SubmitField('Submit')