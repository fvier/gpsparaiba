from apps import db
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime, timezone, date, timedelta

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


class CommercialPlan(db.Model):
    __tablename__ = 'commercial_plans'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), nullable=False)
    vehicle_type = db.Column(db.String(80), nullable=False)
    coverage = db.Column(db.String(160), nullable=False)
    monthly_price = db.Column(db.Numeric(10, 2), nullable=False, default=0)
    installation_price = db.Column(db.Numeric(10, 2), nullable=False, default=0)
    description = db.Column(db.String(240), nullable=False, default='')
    benefits = db.Column(db.Text, nullable=False, default='')
    badge = db.Column(db.String(60), nullable=False, default='')
    whatsapp_url = db.Column(db.Text, nullable=False, default='')
    active = db.Column(db.Boolean, nullable=False, default=True)
    featured = db.Column(db.Boolean, nullable=False, default=False)
    sort_order = db.Column(db.Integer, nullable=False, default=0)
    last_version_code = db.Column(db.String(32), nullable=True)
    updated_at = db.Column(db.DateTime, nullable=False, default=lambda: datetime.now(timezone.utc),
                           onupdate=lambda: datetime.now(timezone.utc))


class PlanVersion(db.Model):
    __tablename__ = 'plan_versions'

    id = db.Column(db.Integer, primary_key=True)
    version_code = db.Column(db.String(32), unique=True, nullable=False)
    snapshot = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime, nullable=False, default=lambda: datetime.now(timezone.utc))


class LandingCard(db.Model):
    __tablename__ = 'landing_cards'

    id = db.Column(db.Integer, primary_key=True)
    slot = db.Column(db.Integer, unique=True, nullable=False)
    plan_id = db.Column(db.Integer, db.ForeignKey('commercial_plans.id'), nullable=False)
    benefits = db.Column(db.Text, nullable=False, default='')
    updated_at = db.Column(db.DateTime, nullable=False, default=lambda: datetime.now(timezone.utc),
                           onupdate=lambda: datetime.now(timezone.utc))
    plan = db.relationship('CommercialPlan')


class LinktreeLink(db.Model):
    __tablename__ = 'linktree_links'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    subtitle = db.Column(db.String(180), nullable=False, default='')
    url = db.Column(db.Text, nullable=False)
    icon = db.Column(db.String(60), nullable=False, default='ri-links-line')
    color = db.Column(db.String(7), nullable=False, default='#2563eb')
    active = db.Column(db.Boolean, nullable=False, default=True)
    sort_order = db.Column(db.Integer, nullable=False, default=0)
    updated_at = db.Column(db.DateTime, nullable=False, default=lambda: datetime.now(timezone.utc),
                           onupdate=lambda: datetime.now(timezone.utc))


class FinancialCategory(db.Model):
    __tablename__ = 'financial_categories'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    entry_type = db.Column(db.String(16), nullable=False)
    parent_id = db.Column(db.Integer, db.ForeignKey('financial_categories.id'), nullable=True)
    active = db.Column(db.Boolean, nullable=False, default=True)
    created_at = db.Column(db.DateTime, nullable=False, default=lambda: datetime.now(timezone.utc))
    parent = db.relationship('FinancialCategory', remote_side=[id], backref='subcategories')


class FinancialEntry(db.Model):
    __tablename__ = 'financial_entries'

    id = db.Column(db.Integer, primary_key=True)
    entry_type = db.Column(db.String(16), nullable=False)
    description = db.Column(db.String(180), nullable=False)
    category_id = db.Column(db.Integer, db.ForeignKey('financial_categories.id'), nullable=False)
    amount = db.Column(db.Numeric(12, 2), nullable=False)
    due_date = db.Column(db.Date, nullable=False)
    status = db.Column(db.String(16), nullable=False, default='pendente')
    notes = db.Column(db.Text, nullable=False, default='')
    created_at = db.Column(db.DateTime, nullable=False, default=lambda: datetime.now(timezone.utc))
    category = db.relationship('FinancialCategory')

    @property
    def effective_status(self):
        if self.status != 'pendente':
            return self.status
        today = date.today()
        if self.due_date < today:
            return 'vencido'
        if self.due_date < today + timedelta(days=5):
            return 'perto_vencer'
        return 'pendente'


class AuditLog(db.Model):
    __tablename__ = 'audit_logs'

    id = db.Column(db.Integer, primary_key=True)
    user_email = db.Column(db.String(120), nullable=False, default='Sistema')
    user_name = db.Column(db.String(100), nullable=False, default='Sistema')
    action = db.Column(db.String(120), nullable=False)
    details = db.Column(db.Text, nullable=False, default='')
    ip_address = db.Column(db.String(45), nullable=False, default='')
    timestamp = db.Column(db.DateTime, nullable=False, default=lambda: datetime.now(timezone.utc))

