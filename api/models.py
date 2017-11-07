# api/models.py
import datetime
import jwt

from api import app, db, bcrypt


class User(db.Model):
    '''Class to represent the users table'''

    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    public_id = db.Column(db.String(100), unique=True, nullable=False)
    first_name = db.Column(db.String(120), nullable=False)
    last_name = db.Column(db.String(120), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(250), nullable=False)
    registered_on = db.Column(db.DateTime, nullable=False)
    category = db.relationship('RecipeCategory', backref='users', 
                               lazy=True)

    def __init__(self, public_id, email, password, first_name, 
                  last_name):
        '''initialize with email'''
        self.public_id = public_id
        self.email = email
        self.password = bcrypt.generate_password_hash(
            password, app.config.get('BCRYPT_LOG_ROUNDS')
            ).decode('UTF-8')
        self.first_name = first_name 
        self.last_name = last_name
        self.registered_on = datetime.datetime.now()
    
    def save(self):
        db.session.add(self)
        db.session.commit()
    
    @staticmethod
    def get_all():
        return User.query.all()

    def delete(self):
        db.session.delete(self)
        db.session.commit()
    
    def encode_auth_token(self, user_id, public_id):
        """
        Generates the Auth Token
        :return: string
        """
        try:
            payload = {
                'exp': datetime.datetime.utcnow() + \
                       datetime.timedelta(days=0, minutes=30),
                'iat': datetime.datetime.utcnow(),
                'user_id': user_id,
                'public_id': public_id
            }
            return jwt.encode(
                payload,
                app.config.get('SECRET_KEY'),
                algorithm='HS256'
            )
        except Exception as e:
            return e
    
    @staticmethod
    def decode_auth_token(auth_token):
        """
        Validates the auth token
        :param auth_token:
        :return: integer|string
        """
        try:
            payload = jwt.decode(auth_token, app.config['SECRET_KEY'])
            is_blacklisted_token = BlacklistToken.\
            check_blacklist(auth_token)
            if is_blacklisted_token:
                return 'Token blacklisted. Please log in again.'
            else:
                return payload['user_id']
        except jwt.ExpiredSignatureError:
            return 'Signature expired. Please log in again.'
        except jwt.InvalidTokenError:
            return 'Invalid token. Please log in again.'
    def __repr__(self):
        return "<User: {}>". format(self.email)


class RecipeCategory(db.Model):
    '''class to represent recipe category table'''

    __tablename__ = 'recipe_category'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), unique=True, nullable=False)
    description = db.Column(db.Text)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), 
                        nullable=False)
    
    def __init__(self, name, description, user_id):
        self.name = name
        self.description = description
        self.user_id = user_id
    
    def save(self):
        db.session.add(self)
        db.session.commit()
    
    @staticmethod
    def get_all():
        return RecipeCategory.query.all()

    @staticmethod
    def get_all_limit_offset(userid, lim):
        return RecipeCategory.query.filter_by(user_id=\
                                              userid).limit(lim).all()

    def delete(self):
        db.session.delete(self)
        db.session.commit()
    
    def __repr__(self):
        return "<Category: {}>". format(self.name)


class Recipe(db.Model):
    '''Class to represent recipe table'''

    __tablename__ = 'recipe'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), unique=True, nullable=False)
    ingredients = db.Column(db.String(250))
    description = db.Column(db.Text)
    cat_id = db.Column(db.Integer, db.ForeignKey('recipe_category.id'), 
                        nullable=False)
    user_id = db.Column(db.Integer, nullable=False)

    def __init__(self, name, cat_id, user_id,  ingredients=None, 
                 description=None):
        self.name = name
        self.ingredients = ingredients
        self.description = description
        self.cat_id = cat_id
        self.user_id = user_id
    
    def save(self):
        db.session.add(self)
        db.session.commit()
    
    @staticmethod
    def update():
        db.session.commit()
    
    @staticmethod
    def get_all():
        return Recipe.query.all()

    @staticmethod
    def get_all_limit_offset(catid, userid, lim):
        return Recipe.query.filter_by(cat_id=catid, user_id=\
                                      userid).limit(lim).all()

    def delete(self):
        db.session.delete(self)
        db.session.commit()
    
    def __repr__(self):
        return "<Recipe: {}>". format(self.name)


class BlacklistToken(db.Model):
    """
    Token Model for storing JWT tokens
    """
    __tablename__ = 'blacklist_tokens'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    token = db.Column(db.String(500), unique=True, nullable=False)
    blacklisted_on = db.Column(db.DateTime, nullable=False)

    def __init__(self, token):
        self.token = token
        self.blacklisted_on = datetime.datetime.now()
    
    @staticmethod
    def check_blacklist(auth_token):
        # check whether auth token has been blacklisted
        res = BlacklistToken.query.filter_by(token=str(auth_token)).first()
        if res:
            return True
        else:
            return False

    def __repr__(self):
        return '<id: token: {}'.format(self.token)

