from apps.pages import blueprint
from apps.pages.models import User
from apps import db
from flask import render_template, request, redirect, url_for, session, flash
from jinja2 import TemplateNotFound

# Public pages that do not require authentication
PUBLIC_PAGES = [
    'landing', 'landing.html',
    'auth-signin', 'auth-signin.html',
    'auth-signup', 'auth-signup.html',
    'auth-password', 'auth-password.html'
]

def ensure_default_user():
    """Create initial admin user if database has no users."""
    try:
        if User.query.count() == 0:
            default_user = User(
                username='admin',
                email='admin@gpsparaiba.com.br'
            )
            default_user.set_password('admin123')
            db.session.add(default_user)
            db.session.commit()
            print("> Initial user created: admin@gpsparaiba.com.br / admin123")
    except Exception as e:
        db.session.rollback()
        print("> Error ensuring default user: " + str(e))

@blueprint.route('/')
def home():
    """Render the public landing page for GPS Paraíba."""
    ensure_default_user()
    return render_template('pages/landing.html', segment='landing')


@blueprint.route('/login', methods=['GET', 'POST'])
def login():
    """Handle user authentication against database."""
    ensure_default_user()

    if request.method == 'POST':
        email = request.form.get('email', '').strip()
        password = request.form.get('password', '').strip()

        if email and password:
            user = User.query.filter((User.email == email) | (User.username == email)).first()
            if user and user.check_password(password):
                session['logged_in'] = True
                session['user_email'] = user.email
                session['user_id'] = user.id
                next_page = request.args.get('next', '/index')
                return redirect(next_page)

        # Fallback / demo mode if invalid credentials or user not found
        return redirect(url_for('pages_blueprint.route_template', template='auth-signin.html', msg='invalid_credentials'))

    return redirect(url_for('pages_blueprint.route_template', template='auth-signin.html'))


@blueprint.route('/logout')
def logout():
    """Handle user logout."""
    session.clear()
    return redirect(url_for('pages_blueprint.home'))


@blueprint.route('/<template>')
def route_template(template):
    """Serve templates with authentication protection for internal areas."""
    try:
        clean_template = template.replace('.html', '')

        # Check authentication for internal pages
        if clean_template not in PUBLIC_PAGES and not session.get('logged_in'):
            return redirect(url_for('pages_blueprint.route_template', template='auth-signin.html', next='/' + clean_template, msg='login_required'))

        if not template.endswith('.html'):
            template += '.html'

        segment = get_segment(request)
        return render_template("pages/" + template, segment=segment, user_email=session.get('user_email', 'Frotista'))

    except TemplateNotFound:
        return render_template('pages/error-404.html'), 404

    except Exception:
        return render_template('pages/error-500.html'), 500


def get_segment(request):
    try:
        segment = request.path.split('/')[-1]
        if segment == '':
            segment = 'index'
        return segment
    except:
        return None
