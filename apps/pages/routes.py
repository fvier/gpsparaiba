from apps.pages import blueprint
from flask import render_template, request, redirect, url_for, session, flash
from jinja2 import TemplateNotFound

# Public pages that do not require authentication
PUBLIC_PAGES = [
    'landing', 'landing.html',
    'auth-signin', 'auth-signin.html',
    'auth-signup', 'auth-signup.html',
    'auth-password', 'auth-password.html'
]

@blueprint.route('/')
def home():
    """Render the public landing page for Rastrek Paraíba."""
    return render_template('pages/landing.html', segment='landing')


@blueprint.route('/login', methods=['GET', 'POST'])
def login():
    """Handle user authentication."""
    if request.method == 'POST':
        email = request.form.get('email', '').strip()
        password = request.form.get('password', '').strip()

        # For demonstration / initial setup: allow login with any valid input or admin
        if email and password:
            session['logged_in'] = True
            session['user_email'] = email
            next_page = request.args.get('next', '/index')
            return redirect(next_page)
        else:
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
