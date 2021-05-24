from flask_wtf import FlaskForm
from wtforms import StringField, SelectField, BooleanField, DecimalField, IntegerField, TextAreaField, SubmitField
from wtforms.validators import DataRequired, Length, Regexp, EqualTo
from wtforms import ValidationError
from ..models import User, Role
from wtforms.ex.sqlalchemy.fields import QuerySelectField
from .. import db

class RegistreraFalk(FlaskForm):
    vikt = IntegerField('Vikt i gram', validators=[DataRequired(),] )
    kön = SelectField('Kön', choices=[('M'), ('F')])
    hb = StringField('Höger ben', validators=[DataRequired()] )
    vb = StringField('Vänster ben', validators=[DataRequired()])
    hp10 = DecimalField('hp10', validators=[DataRequired()])
    hp7 = DecimalField('hp7', validators=[DataRequired()])
    sp = DecimalField('sp', validators=[DataRequired()])
    ålder = DecimalField('Ålder', validators=[DataRequired()])
    kräva = SelectField('Kräva', choices=[('Tom'), ('Halvfull'), ('Full')])
    foto = StringField('Foto, angiven kamera med foton', validators=[DataRequired()])
    märkare = StringField('Märkare', validators=[DataRequired()])
    övrigt = TextAreaField('Övrigt')
    plats = QuerySelectorField('Plats', validators=[DataRequired()])
    submit = SubmitField('Submit')