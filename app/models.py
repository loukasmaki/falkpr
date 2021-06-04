from werkzeug.security import generate_password_hash, check_password_hash
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from flask import current_app
from flask_login import UserMixin, AnonymousUserMixin
from . import db, login_manager
from datetime import datetime

falk_återfynd = db.Table(
    'falk_återfynd',
    db.Column('falk_id', db.Integer, db.ForeignKey('falkar.id'), primary_key=True),
    db.Column('återfynd_id', db.Integer, db.ForeignKey('återfynd.id'), primary_key=True)
)

class Permission:
    SCHEDULE = 1
    WRITE = 2
    REGISTRATION = 4
    TOURNAMENT = 8
    ADMIN = 16

class Role(db.Model):
    __tablename__ = 'roles'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), unique=True)
    default = db.Column(db.Boolean, default=False, index=True)
    permissions = db.Column(db.Integer)
    user = db.relationship('User', backref='role', lazy='dynamic')

    def __init__(self, **kwargs):
        super(Role, self).__init__(**kwargs)
        if self.permissions is None:
            self.permissions = 0


    @staticmethod
    def insert_roles():
        roles = {
            'User' : [Permission.SCHEDULE, Permission.COMMENT],
            'Staff' : [Permission.SCHEDULE, Permission.COMMENT, Permission.REGISTRATION],
            'TournamentManager' : [Permission.SCHEDULE, Permission.COMMENT, Permission.TOURNAMENT],
            'Administrator' : [Permission.SCHEDULE, Permission.COMMENT, Permission.TOURNAMENT, Permission.REGISTRATION, Permission.ADMIN],
        }
        default_role = 'User'
        for r in roles:
            role = Role.query.filter_by(name=r).first()
            if role is None:
                role = Role(name=r)
            role.reset_permissions()
            for perm in roles[r]:
                role.add_permission(perm)
            role.default = (role.name == default_role)
            db.session.add(role)
        db.session.commit()

    def add_permission(self, perm):
        if not self.has_permission(perm):
            self.permissions += perm

    def remove_permission(self, perm):
        if self.has_permission(perm):
            self.permissions -= perm

    def reset_permissions(self):
        self.permissions = 0

    def has_permission(self, perm):
        return self.permissions & perm == perm

    def __repr__(self):
        return '<Role %r>' % self.name


class User(UserMixin, db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(64), unique=True, index=True)
    name = db.Column(db.String(64), index=True)
    role_id = db.Column(db.Integer, db.ForeignKey('roles.id'))
    password_hash = db.Column(db.String(128))
    country = db.Column(db.String(64))
    club = db.Column(db.String(64), nullable=True)
    #dateofbirth = db.Column(db.Date)
    #nextofkin = db.Column(db.String(64), nullable=True)
    #nextofkinphoneemail = db.Column(db.String(64), nullable=True)

    confirmed = db.Column(db.Boolean, default=False)
    #posts = db.relationship('Post', backref='author', lazy='dynamic')
    #order = db.relationship('Order', backref='user')

    def __init__(self, **kwargs):
        super(User, self).__init__(**kwargs)
        if self.role is None:
            if self.email == current_app.config['EVENT_ADMIN']:
                self.role = Role.query.filter_by(name='Administrator').first()
            if self.role is None:
                self.role = Role.query.filter_by(default=True).first()
    
    @property
    def password(self):
        raise AttributeError('password is not a readable attribute')

    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password)

    def verify_password(self, password):
        return check_password_hash(self.password_hash, password)

    def generate_confirmation_token(self, expiration=3600):
        s = Serializer(current_app.config['SECRET_KEY'], expiration)
        return s.dumps({'confirm': self.id}).decode('utf-8')

    def confirm(self, token):
        s = Serializer(current_app.config['SECRET_KEY'])
        try:
            data = s.loads(token.encode('utf-8'))
        except:
            return False
        if data.get('confirm') != self.id:
            return False
        self.confirmed = True
        db.session.add(self)
        return True

    def generate_reset_token(self, expiration=3600):
        s = Serializer(current_app.config['SECRET_KEY'], expiration)
        return s.dumps({'reset': self.id}).decode('utf-8')

    @staticmethod
    def reset_password(token, new_password):
        s = Serializer(current_app.config['SECRET_KEY'])
        try:
            data = s.loads(token.encode('utf-8'))
        except:
            return False
        user = User.query.get(data.get('reset'))
        if user is None:
            return False
        user.password = new_password
        db.session.add(user)
        return True

    def generate_email_change_token(self, new_email, expiration=3600):
        s = Serializer(current_app.config['SECRET_KEY'], expiration)
        return s.dumps(
            {'change_email': self.id, 'new_email': new_email}).decode('utf-8')

    def change_email(self, token):
        s = Serializer(current_app.config['SECRET_KEY'])
        try:
            data = s.loads(token.encode('utf-8'))
        except:
            return False
        if data.get('change_email') != self.id:
            return False
        new_email = data.get('new_email')
        if new_email is None:
            return False
        if self.query.filter_by(email=new_email).first() is not None:
            return False
        self.email = new_email
        db.session.add(self)
        return True

    def can(self, perm):
        return self.role is not None and self.role.has_permission(perm)

    def is_administrator(self):
        print(self.role, self.role_id)
        return self.can(Permission.ADMIN)
    
    def __repr__(self):
        return '<User %r>' % self.name

class AnonymousUser(AnonymousUserMixin):
    def can(self, permissions):
        return False
    
    def is_administrator(self):
        return False

login_manager.anonymous_user = AnonymousUser


class Falk(db.Model):
    __tablename__ = 'falkar'
    id = db.Column(db.Integer, primary_key=True)
    vikt = db.Column(db.Integer)
    kön = db.Column(db.String(1))
    hb = db.Column(db.String(20))
    vb = db.Column(db.String(20))
    hp10 = db.Column(db.Integer)
    hp7 = db.Column(db.Integer)
    sp = db.Column(db.Integer)
    dagar_17 = db.Column(db.Integer)
    kräva = db.Column(db.String(10))
    foto = db.Column(db.String(64))
    märkare = db.Column(db.String(64))
    övrigt = db.Column(db.String(128)) #Textareafield?
    ringmärkt_datum = db.Column(db.DateTime(), default=datetime.utcnow)
    lokal_id = db.Column(db.Integer, db.ForeignKey('lokaler.id'))
    återfynd = db.relationship('Återfynd', secondary=falk_återfynd, lazy='subquery', backref=db.backref('falkar', lazy=True))
    påse = db.Column(db.String(64))
    närvarande = db.Column(db.String(128))
    duvringar = db.Column(db.Boolean)

class Lokal(db.Model):
    __tablename__ = 'lokaler'
    id = db.Column(db.Integer, primary_key=True)
    namn = db.Column(db.String(64))
    koordinatref = db.Column(db.String(64))
    kommun = db.Column(db.String(128))
    län = db.Column(db.String(128)) 
    förälder_id = db.Column(db.Integer) # Vissa lokaler har en förälder
    år_hittad = db.Column(db.DateTime) #Behöver specificera det här bättre
    observationer = db.relationship('Observation', backref='lokaler', lazy=True)

    def __str__(self):
        return self.namn

class Återfynd(db.Model):
    __tablename__ = 'återfynd'
    id = db.Column(db.Integer, primary_key=True)
    hb = db.Column(db.String(20))
    vb = db.Column(db.String(20))
    levande = db.Column(db.Boolean)

class Hylla(db.Model):
    __tablename__ = 'hyllor'
    id = db.Column(db.Integer, primary_key=True)
    beskrivning = db.Column(db.String(128))
    lokal_id = db.Column(db.Integer)
    

class Observation(db.Model):
    __tablename__ = 'observationer'
    id = db.Column(db.Integer, primary_key=True)
    datum = db.Column(db.DateTime)
    person = db.Column(db.String(64))
    såg_falk = db.Column(db.Boolean)
    bekräftad_häckning = db.Column(db.Boolean)
    lokal_id = db.Column(db.Integer, db.ForeignKey('lokaler.id'))
    datum = db.Column(db.DateTime)

class Foto(db.Model):
    __tablename__ = 'foton'
    id = db.Column(db.Integer, primary_key=True)
    namn = db.Column(db.String(128))
    fotograf = db.Column(db.String(128))
    hyll_id = db.Column(db.Integer)
    kategori = db.Column(db.String(64))
    datum = db.Column(db.DateTime)
    

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))
