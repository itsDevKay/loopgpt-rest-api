from app import db
from random import choice
from urllib.parse import quote
from werkzeug.security import check_password_hash
from werkzeug.security import generate_password_hash
from sqlalchemy.orm.attributes import QueryableAttribute
import datetime, os, string, secrets, json
from random import shuffle

class BaseModel(db.Model):
    __abstract__ = True

    def update(self, **kwargs):
        for key, value in kwargs.items():
            print(key)
            if hasattr(self, key):
                setattr(self, key, value)

    def to_dict(self, show=None, _hide=[], _path=None):
        """Return a dictionary representation of this model."""

        show = show or []

        hidden = self._hidden_fields if hasattr(self, "_hidden_fields") else []
        default = self._default_fields if hasattr(self, "_default_fields") else []
        default.extend(['id', 'modified_at', 'created_at'])

        if not _path:
            _path = self.__tablename__.lower()

            def prepend_path(item):
                item = item.lower()
                if item.split(".", 1)[0] == _path:
                    return item
                if len(item) == 0:
                    return item
                if item[0] != ".":
                    item = ".%s" % item
                item = "%s%s" % (_path, item)
                return item

            _hide[:] = [prepend_path(x) for x in _hide]
            show[:] = [prepend_path(x) for x in show]

        columns = self.__table__.columns.keys()
        relationships = self.__mapper__.relationships.keys()
        properties = dir(self)

        ret_data = {}

        for key in columns:
            if key.startswith("_"):
                continue
            check = "%s.%s" % (_path, key)
            if check in _hide or key in hidden:
                continue
            if check in show or key in default:
                ret_data[key] = getattr(self, key)

        for key in relationships:
            if key.startswith("_"):
                continue
            check = "%s.%s" % (_path, key)
            if check in _hide or key in hidden:
                continue
            if check in show or key in default:
                _hide.append(check)
                is_list = self.__mapper__.relationships[key].uselist
                if is_list:
                    items = getattr(self, key)
                    if self.__mapper__.relationships[key].query_class is not None:
                        if hasattr(items, "all"):
                            items = items.all()
                    ret_data[key] = []
                    for item in items:
                        ret_data[key].append(
                            item.to_dict(
                                show=list(show),
                                _hide=list(_hide),
                                _path=("%s.%s" % (_path, key.lower())),
                            )
                        )
                else:
                    if (
                        self.__mapper__.relationships[key].query_class is not None
                        or self.__mapper__.relationships[key].instrument_class
                        is not None
                    ):
                        item = getattr(self, key)
                        if item is not None:
                            ret_data[key] = item.to_dict(
                                show=list(show),
                                _hide=list(_hide),
                                _path=("%s.%s" % (_path, key.lower())),
                            )
                        else:
                            ret_data[key] = None
                    else:
                        ret_data[key] = getattr(self, key)

        for key in list(set(properties) - set(columns) - set(relationships)):
            if key.startswith("_"):
                continue
            if not hasattr(self.__class__, key):
                continue
            attr = getattr(self.__class__, key)
            if not (isinstance(attr, property) or isinstance(attr, QueryableAttribute)):
                continue
            check = "%s.%s" % (_path, key)
            if check in _hide or key in hidden:
                continue
            if check in show or key in default:
                val = getattr(self, key)
                if hasattr(val, "to_dict"):
                    ret_data[key] = val.to_dict(
                        show=list(show),
                        _hide=list(_hide),
                        # _path=('%s.%s' % (path, key.lower())), # original
                        _path=('%s.%s' % (_path, key.lower())),
                    )
                else:
                    try:
                        ret_data[key] = json.loads(json.dumps(val))
                    except:
                        pass

        return ret_data
    
class Users(BaseModel):
    __tablename__ = 'users'
    id                  = db.Column(db.Integer, primary_key=True)
    uuid                = db.Column(db.CHAR(36), nullable=False, index=True, unique=True)
    email               = db.Column(db.String(120), nullable=False, index=True, unique=True)
    password_hash       = db.Column(db.String(128))
    status              = db.Column(db.String(20), default='driver')
    first_name          = db.Column(db.String(50), nullable=False)
    last_name           = db.Column(db.String(50), nullable=False)
    phone_number        = db.Column(db.String(12), default=None) # Only needed for drivers.
    creation_date       = db.Column(db.DateTime, default=datetime.datetime.utcnow())
    last_updated        = db.Column(db.DateTime, default=datetime.datetime.utcnow())

    _default_fields = [
        'email', 'first_name', 'last_name', 'phone_number',
        'id', 'uuid'
    ]
    _readonly_fields = [ 'creation_date' ]
    _hidden_fields = [ 'password_hash' ]

    def __repr__(self):
        return f'<Renters {self.email}>'

    def is_active(self):
        """True, as all users are active."""
        return True
    
    def get_id(self):
        """Return the email address to satisfy Flask-Login's requirements."""
        return self.id

    def is_authenticated(self):
        """Return True if the user is authenticated."""
        return self.authenticated

    def is_anonymous(self):
        """False, as anonymous users aren't supported."""
        return False

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)
    
class IPAddresses(BaseModel):
    __tablename__ = 'ip_addresses'
    id          = db.Column(db.Integer, primary_key=True)
    uuid        = db.Column(db.CHAR(36), nullable=False, index=True, unique=True)
    ip_address  = db.Column(db.String(50), nullable=False, index=True)
    user_uuid   = db.Column(db.CHAR(36), nullable=False, index=True)
    user_status = db.Column(db.String(20), nullable=False)
    login_date  = db.Column(db.DateTime, default=datetime.datetime.utcnow())

    _default_fields = [ 'ip_address', 'uuid' 'user_uuid', 'user_status', 'login_date' ]

    def __repr__(self):
        return f'<IPAddresses: {self.user_status} login from [ {self.ip_address} ] on [ {self.login_date} ].'
    
class Chatrooms(BaseModel):
    __tablename__ = 'chatrooms'
    id                  = db.Column(db.Integer, primary_key=True)
    uuid                = db.Column(db.String(40), nullable=False)
    host_uuid           = db.Column(db.CHAR(36), nullable=False, index=True) # uuid of host user
    name                = db.Column(db.String(100), default=None) # name of chatroom
    last_message        = db.Column(db.String(500), default='')
    last_message_from   = db.Column(db.String(120), default='')
    creation_date       = db.Column(db.DateTime, default=datetime.datetime.utcnow())
    last_updated        = db.Column(db.DateTime, default=datetime.datetime.utcnow())
    
    _default_fields = [
        'uuid', 'host', 'name', 'last_message', 'last_message_from'
    ]
    _readonly_fields = [ 'creation_date', 'last_updated' ] 

class ChatParticipants(BaseModel):
    __tablename__ = 'chat_participants'
    id              = db.Column(db.Integer, primary_key=True)
    uuid            = db.Column(db.CHAR(36), nullable=False, index=True)
    user_uuid       = db.Column(db.CHAR(36), nullable=False, index=True)
    chatroom        = db.Column(db.String(40), nullable=False)
    creation_date   = db.Column(db.DateTime, default=datetime.datetime.utcnow())
    
    _default_fields = [ 'user', 'chatroom', 'uuid' ]
    _readonly_fields = [ 'creation_date' ] 

class Chats(BaseModel):
    __tablename__ = 'chats'
    id              = db.Column(db.Integer, primary_key=True)
    uuid            = db.Column(db.CHAR(36), nullable=False, unique=True, index=True)
    chatroom        = db.Column(db.String(40), nullable=False)
    from_user_uuid  = db.Column(db.CHAR(36), nullable=False)
    message         = db.Column(db.String(500), nullable=False)
    timestamp       = db.Column(db.String(80), nullable=False)
    creation_date   = db.Column(db.DateTime, default=datetime.datetime.utcnow())

    _default_fields = [ 'chatroom', 'uuid', 'from_user', 'message', 'timestamp' ]
    _readonly_fields = [ 'creation_date' ]