from apps import db
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime, timezone

class User(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), unique=True, nullable=False)
    full_name = db.Column(db.String(120), nullable=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    ddd = db.Column(db.String(2), nullable=True)
    contact = db.Column(db.String(9), nullable=True)
    password_hash = db.Column(db.String(256), nullable=False)
    role = db.Column(db.String(32), nullable=False, default='usuario')
    category = db.Column(db.String(32), nullable=False, default='Orange')
    active = db.Column(db.Boolean, nullable=False, default=True)
    must_change_password = db.Column(db.Boolean, nullable=False, default=False)
    avatar_filename = db.Column(db.String(160), nullable=True)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    @property
    def is_admin_or_manager(self):
        return self.role.lower() in {'admin', 'gerente'}

    def __repr__(self):
        return f'<User {self.email}>'


class CarouselImage(db.Model):
    __tablename__ = 'carousel_images'

    id = db.Column(db.Integer, primary_key=True)
    filename = db.Column(db.String(200), unique=True, nullable=False)
    title = db.Column(db.String(120), nullable=False)
    set_type = db.Column(db.String(32), nullable=False, default='outros')
    active = db.Column(db.Boolean, nullable=False, default=False)
    sort_order = db.Column(db.Integer, nullable=False, default=0)
    created_at = db.Column(db.DateTime, nullable=False, default=lambda: datetime.now(timezone.utc))

    def __repr__(self):
        return f'<CarouselImage {self.filename}>'
