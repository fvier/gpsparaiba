from apps.pages import blueprint
from apps.pages.models import User, CarouselImage
from apps import db
from flask import render_template, request, redirect, url_for, session, flash, current_app
from werkzeug.utils import secure_filename
from uuid import uuid4
import os
from jinja2 import TemplateNotFound

# Public pages that do not require authentication
PUBLIC_PAGES = [
    'landing', 'landing.html',
    'index', 'index.html',
    'links', 'links.html',
    'auth-signin', 'auth-signin.html',
    'auth-signup', 'auth-signup.html',
    'auth-password', 'auth-password.html'
]

MAX_PRIVILEGE_EMAILS = {'jarmessonn.cz@gmail.com'}
INITIAL_USER_PASSWORD = 'bemvindo'
VALID_ROLES = {'admin', 'gerente', 'usuario'}
VALID_CATEGORIES = {'Orange', 'Blue', 'Green', 'Gold', 'Platinum', 'Diamond', 'Black'}

CAROUSEL_IMAGE_TITLES = {
    'hero-set-hatches-v2.png': 'Conjunto 1 — Carros hatch populares',
    'hero-conjunto-2-v2.png': 'Conjunto 2 — Motos populares',
    'hero-conjunto-3-v2.png': 'Conjunto 3 — Pick-ups leves e utilitários',
    'hero-conjunto-4-v2.png': 'Conjunto 4 — Camionetes e SUVs grandes',
    'hero-conjunto-5-v2.png': 'Conjunto 5 — Motos premium e aventureiras',
    'rastrek_hero_vehicle.png': 'Range Rover — imagem original',
}
DEFAULT_ACTIVE_CAROUSEL = list(CAROUSEL_IMAGE_TITLES)[:5]
CAROUSEL_SET_TYPES = {
    'conjunto_1': 'Conjunto 1 — Carros Hatch',
    'conjunto_2': 'Conjunto 2 — Motos Populares',
    'conjunto_3': 'Conjunto 3 — Pick-ups e Utilitários',
    'conjunto_4': 'Conjunto 4 — Camionetes e SUVs',
    'conjunto_5': 'Conjunto 5 — Motos Premium',
    'outros': 'Outros / Testes',
}

PERMISSION_MODULES = [
    {'name': 'Landing page', 'route': '/', 'icon': 'ri-global-line', 'color': 'primary', 'login': False, 'usuario': 'total', 'gerente': 'total', 'admin': 'total'},
    {'name': 'Painel público da TV', 'route': '/index', 'icon': 'ri-tv-2-line', 'color': 'info', 'login': False, 'usuario': 'total', 'gerente': 'total', 'admin': 'total'},
    {'name': 'Dashboard de vendas', 'route': '/dashboard-sales', 'icon': 'ri-line-chart-line', 'color': 'success', 'login': True, 'usuario': 'total', 'gerente': 'total', 'admin': 'total'},
    {'name': 'Comissionamento', 'route': '/comissionamento', 'icon': 'ri-table-line', 'color': 'info', 'login': True, 'usuario': 'limited', 'gerente': 'total', 'admin': 'total'},
    {'name': 'Vendas', 'route': '/vendas', 'icon': 'ri-shopping-cart-2-line', 'color': 'primary', 'login': True, 'usuario': 'limited', 'gerente': 'total', 'admin': 'total'},
    {'name': 'Validação de vendas', 'route': '/validacao-vendas', 'icon': 'ri-checkbox-circle-line', 'color': 'warning', 'login': True, 'usuario': 'none', 'gerente': 'total', 'admin': 'total'},
    {'name': 'Planos', 'route': '/planos', 'icon': 'ri-price-tag-3-line', 'color': 'success', 'login': True, 'usuario': 'limited', 'gerente': 'total', 'admin': 'total'},
    {'name': 'Ranking', 'route': '/ranking', 'icon': 'ri-trophy-line', 'color': 'warning', 'login': True, 'usuario': 'total', 'gerente': 'total', 'admin': 'total'},
    {'name': 'Usuários e colaboradores', 'route': '/admin-cadastrar', 'icon': 'ri-team-line', 'color': 'danger', 'login': True, 'usuario': 'none', 'gerente': 'none', 'admin': 'total'},
    {'name': 'Privilégios', 'route': '/admin-privilegios', 'icon': 'ri-shield-keyhole-line', 'color': 'danger', 'login': True, 'usuario': 'none', 'gerente': 'none', 'admin': 'total'},
    {'name': 'Gerenciar carrossel', 'route': '/admin-carrossel', 'icon': 'ri-gallery-line', 'color': 'primary', 'login': True, 'usuario': 'none', 'gerente': 'none', 'admin': 'total'},
]


def carousel_set_type_from_filename(filename):
    lowered = filename.lower()
    if 'conjunto-2' in lowered or ('motos' in lowered and 'premium' not in lowered):
        return 'conjunto_2'
    if 'conjunto-3' in lowered or 'utilitarios' in lowered:
        return 'conjunto_3'
    if 'conjunto-4' in lowered or 'set-premium' in lowered or 'suv' in lowered:
        return 'conjunto_4'
    if 'conjunto-5' in lowered or 'motos-premium' in lowered:
        return 'conjunto_5'
    if 'hatches' in lowered:
        return 'conjunto_1'
    return 'outros'


def carousel_title_from_filename(filename):
    if filename in CAROUSEL_IMAGE_TITLES:
        return CAROUSEL_IMAGE_TITLES[filename]
    clean_name = os.path.splitext(filename)[0].replace('hero-', '').replace('rastrek-', '')
    return clean_name.replace('-', ' ').replace('_', ' ').title()


def ensure_carousel_images():
    """Register project carousel artwork without changing saved selections."""
    image_dir = os.path.join(current_app.static_folder, 'images')
    if not os.path.isdir(image_dir):
        return
    filenames = sorted(
        filename for filename in os.listdir(image_dir)
        if filename.lower().endswith(('.png', '.jpg', '.jpeg', '.webp'))
        and (filename.startswith('hero-') or filename == 'rastrek_hero_vehicle.png')
    )
    existing = {image.filename for image in CarouselImage.query.all()}
    database_was_empty = not existing
    next_order = (db.session.query(db.func.max(CarouselImage.sort_order)).scalar() or 0) + 10
    changed = False
    for filename in filenames:
        if filename in existing:
            continue
        is_default = database_was_empty and filename in DEFAULT_ACTIVE_CAROUSEL
        default_index = DEFAULT_ACTIVE_CAROUSEL.index(filename) if is_default else None
        db.session.add(CarouselImage(
            filename=filename,
            title=carousel_title_from_filename(filename),
            set_type=carousel_set_type_from_filename(filename),
            active=is_default,
            sort_order=(default_index + 1) * 10 if is_default else next_order,
        ))
        if not is_default:
            next_order += 10
        changed = True
    for image in CarouselImage.query.all():
        inferred_type = carousel_set_type_from_filename(image.filename)
        if (not image.set_type or image.set_type == 'outros') and inferred_type != 'outros':
            image.set_type = inferred_type
            changed = True
    if changed:
        db.session.commit()


def carousel_image_view(image):
    path = os.path.join(current_app.static_folder, 'images', os.path.basename(image.filename))
    version = int(os.path.getmtime(path)) if os.path.isfile(path) else 1
    return {
        'id': image.id,
        'filename': image.filename,
        'title': image.title,
        'set_type': image.set_type if image.set_type in CAROUSEL_SET_TYPES else 'outros',
        'set_type_label': CAROUSEL_SET_TYPES.get(image.set_type, CAROUSEL_SET_TYPES['outros']),
        'active': image.active,
        'sort_order': image.sort_order,
        'version': version,
    }


def active_carousel_images():
    ensure_carousel_images()
    images = CarouselImage.query.filter_by(active=True).all()
    image_views = [carousel_image_view(image) for image in images]
    return sorted(image_views, key=lambda image: (-image['version'], -image['id']))


def normalize_user_role(email='', username='', forced_role=None):
    if forced_role:
        return forced_role.lower()
    if email.strip().lower() in MAX_PRIVILEGE_EMAILS:
        return 'admin'
    identity = f"{email} {username}".lower()
    if 'admin' in identity:
        return 'admin'
    if 'gerente' in identity:
        return 'gerente'
    return 'usuario'


def ensure_default_user():
    """Create an initial admin user for system access."""
    try:
        if User.query.count() == 0 or not User.query.filter_by(email='admin@gpsparaiba.com.br').first():
            admin_email = os.getenv('INITIAL_ADMIN_EMAIL', 'admin@gpsparaiba.com.br').strip().lower()
            admin_password = os.getenv('INITIAL_ADMIN_PASSWORD', 'admin123')
            default_user = User.query.filter_by(email=admin_email).first()
            if not default_user:
                default_user = User(
                    username='admin',
                    full_name='Administrador GPS Paraíba',
                    email=admin_email,
                    role='admin',
                    category='Black',
                    active=True,
                    must_change_password=False
                )
                default_user.set_password(admin_password)
                db.session.add(default_user)
                db.session.commit()
                current_app.logger.info('Initial administrator created for %s', admin_email)
    except Exception as e:
        db.session.rollback()
        print("> Error ensuring default user: " + str(e))


@blueprint.route('/')
def home():
    """Render the public landing page for GPS Paraíba."""
    ensure_default_user()
    return render_template('pages/landing.html', segment='landing', carousel_images=active_carousel_images())


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
                if not user.active:
                    return redirect(url_for('pages_blueprint.route_template', template='auth-signin.html', msg='inactive_user'))
                role = ('admin' if user.email.strip().lower() in MAX_PRIVILEGE_EMAILS
                        else (user.role if getattr(user, 'role', None) else normalize_user_role(user.email, user.username)))
                if role not in {'admin', 'gerente', 'usuario'}:
                    role = normalize_user_role(user.email, user.username)
                user.role = role
                db.session.commit()

                session['logged_in'] = True
                session['user_email'] = user.email
                session['user_id'] = user.id
                session['user_role'] = role
                session['must_change_password'] = bool(user.must_change_password)
                if user.must_change_password:
                    return redirect(url_for('pages_blueprint.change_password'))
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


@blueprint.route('/alterar-senha', methods=['GET', 'POST'])
def change_password():
    if not session.get('logged_in'):
        return redirect(url_for('pages_blueprint.route_template', template='auth-signin.html', msg='login_required'))
    user = db.session.get(User, session.get('user_id'))
    if not user or not user.active:
        session.clear()
        return redirect(url_for('pages_blueprint.route_template', template='auth-signin.html', msg='inactive_user'))
    if request.method == 'POST':
        password = request.form.get('password', '')
        confirmation = request.form.get('password_confirmation', '')
        if len(password) < 8:
            flash('A nova senha deve possuir pelo menos 8 caracteres.', 'danger')
        elif password == INITIAL_USER_PASSWORD:
            flash('Escolha uma senha diferente da senha inicial.', 'danger')
        elif password != confirmation:
            flash('A confirmação da senha não confere.', 'danger')
        else:
            user.set_password(password)
            user.must_change_password = False
            db.session.commit()
            session['must_change_password'] = False
            flash('Senha alterada com sucesso.', 'success')
            return redirect('/index')
    return render_template('pages/alterar-senha.html', user_email=user.email, user_role=user.role,
                           user_display_name=user.full_name or user.username)


def admin_required():
    return session.get('logged_in') and session.get('user_role') == 'admin'


@blueprint.route('/perfil/foto', methods=['POST'])
def upload_profile_photo():
    if not session.get('logged_in'):
        return redirect(url_for('pages_blueprint.route_template', template='auth-signin.html', msg='login_required'))
    user = db.session.get(User, session.get('user_id'))
    photo = request.files.get('profile_photo')
    allowed_extensions = {'jpg', 'jpeg', 'png', 'webp'}
    original_name = secure_filename(photo.filename or '') if photo else ''
    extension = original_name.rsplit('.', 1)[-1].lower() if '.' in original_name else ''
    if not user or not photo or extension not in allowed_extensions:
        flash('Selecione uma imagem JPG, PNG ou WEBP válida.', 'danger')
        return redirect(request.referrer or '/index')
    photo.stream.seek(0, os.SEEK_END)
    file_size = photo.stream.tell()
    photo.stream.seek(0)
    if file_size > 3 * 1024 * 1024:
        flash('A foto deve possuir no máximo 3 MB.', 'danger')
        return redirect(request.referrer or '/index')
    signature = photo.stream.read(12)
    photo.stream.seek(0)
    valid_signature = (
        (extension in {'jpg', 'jpeg'} and signature.startswith(b'\xff\xd8\xff')) or
        (extension == 'png' and signature.startswith(b'\x89PNG\r\n\x1a\n')) or
        (extension == 'webp' and signature.startswith(b'RIFF') and signature[8:12] == b'WEBP')
    )
    if not valid_signature:
        flash('O arquivo enviado não é uma imagem válida.', 'danger')
        return redirect(request.referrer or '/index')
    upload_dir = os.path.join(current_app.static_folder, 'images', 'uploads', 'avatars')
    os.makedirs(upload_dir, exist_ok=True)
    new_filename = f'user-{user.id}-{uuid4().hex}.{extension}'
    photo.save(os.path.join(upload_dir, new_filename))
    old_filename = user.avatar_filename
    user.avatar_filename = new_filename
    db.session.commit()
    if old_filename:
        old_path = os.path.join(upload_dir, os.path.basename(old_filename))
        if os.path.isfile(old_path):
            os.remove(old_path)
    flash('Foto de perfil atualizada.', 'success')
    return redirect(request.referrer or '/index')


@blueprint.route('/admin/usuarios', methods=['POST'])
def create_user():
    if not admin_required():
        return redirect('/index')
    full_name = request.form.get('full_name', '').strip()
    email = request.form.get('email', '').strip().lower()
    ddd = request.form.get('ddd', '').strip()
    contact = request.form.get('contact', '').strip()
    role = request.form.get('role', 'usuario').lower()
    if not full_name or not email or len(ddd) != 2 or len(contact) not in {8, 9} or role not in VALID_ROLES:
        flash('Preencha corretamente todos os campos obrigatórios.', 'danger')
        return redirect('/admin-cadastrar')
    if User.query.filter_by(email=email).first():
        flash('Já existe um usuário com este e-mail.', 'danger')
        return redirect('/admin-cadastrar')
    username_base = email.split('@')[0]
    username = username_base
    sequence = 2
    while User.query.filter_by(username=username).first():
        username = f'{username_base}{sequence}'
        sequence += 1
    user = User(username=username, full_name=full_name, email=email, ddd=ddd, contact=contact,
                role=role, active=True, must_change_password=True)
    user.set_password(INITIAL_USER_PASSWORD)
    db.session.add(user)
    db.session.commit()
    flash(f'Usuário {full_name} cadastrado. Senha inicial: {INITIAL_USER_PASSWORD}.', 'success')
    return redirect('/admin-cadastrar')


@blueprint.route('/admin/usuarios/<int:user_id>/<action>', methods=['POST'])
def manage_user(user_id, action):
    if not admin_required():
        return redirect('/index')
    user = db.session.get(User, user_id)
    if not user:
        flash('Usuário não encontrado.', 'danger')
        return redirect('/admin-cadastrar')
    protected = user.email.lower() in MAX_PRIVILEGE_EMAILS
    if action == 'reset-password':
        user.set_password(INITIAL_USER_PASSWORD)
        user.must_change_password = True
        flash(f'Senha de {user.full_name or user.email} redefinida para {INITIAL_USER_PASSWORD}.', 'success')
    elif action == 'toggle-active' and not protected and user.id != session.get('user_id'):
        user.active = not user.active
        flash('Status do usuário atualizado.', 'success')
    elif action == 'change-role':
        role = request.form.get('role', '').lower()
        if role in VALID_ROLES and not protected and user.id != session.get('user_id'):
            user.role = role
            flash('Privilégio atualizado.', 'success')
    elif action == 'update-profile':
        full_name = request.form.get('full_name', '').strip()
        email = request.form.get('email', '').strip().lower()
        ddd = request.form.get('ddd', '').strip()
        contact = request.form.get('contact', '').strip()
        email_owner = User.query.filter(User.email == email, User.id != user.id).first()
        if not full_name or not email or len(ddd) != 2 or len(contact) not in {8, 9}:
            flash('Preencha corretamente os dados do colaborador.', 'danger')
            return redirect('/admin-cadastrar')
        if email_owner:
            flash('O e-mail informado já pertence a outro usuário.', 'danger')
            return redirect('/admin-cadastrar')
        user.full_name = full_name
        if not protected:
            user.email = email
        user.ddd = ddd
        user.contact = contact
        flash('Dados do colaborador atualizados.', 'success')
    elif action == 'change-category':
        category = request.form.get('category', '')
        if category in VALID_CATEGORIES:
            user.category = category
            flash(f'Categoria de {user.full_name or user.email} alterada para {category}.', 'success')
    db.session.commit()
    next_page = request.form.get('next', '')
    return redirect(next_page if next_page in {'/admin-cadastrar', '/admin-privilegios'} else '/admin-cadastrar')


@blueprint.route('/admin-carrossel')
def manage_carousel_page():
    if not admin_required():
        return redirect('/index')
    ensure_carousel_images()
    images = CarouselImage.query.all()
    image_views = [carousel_image_view(image) for image in images]
    image_views.sort(key=lambda image: (not image['active'], -image['version'], -image['id']))
    for automatic_number, image_view in enumerate(image_views, start=1):
        image_view['display_number'] = automatic_number
    current_user_id = session.get('user_id')
    current_user = db.session.get(User, current_user_id) if current_user_id is not None else None
    avatar_url = (url_for('static', filename=f'images/uploads/avatars/{current_user.avatar_filename}')
                  if current_user and current_user.avatar_filename
                  else url_for('static', filename='images/users/dummy-avatar.jpg'))
    return render_template(
        'pages/admin-carrossel.html',
        segment='admin-carrossel',
        carousel_images=image_views,
        user_email=session.get('user_email', ''),
        user_display_name=(current_user.full_name or current_user.username) if current_user else session.get('user_email', 'Administrador'),
        user_category=current_user.category if current_user else 'Orange',
        user_role=session.get('user_role', 'admin'),
        can_edit_commission=True,
        can_manage_plans=True,
        can_validate_sales=True,
        carousel_set_types=CAROUSEL_SET_TYPES,
        user_avatar_url=avatar_url,
    )


@blueprint.route('/admin/carrossel/save', methods=['POST'])
def save_carousel():
    if not admin_required():
        return redirect('/index')
    ensure_carousel_images()
    images = CarouselImage.query.all()
    selected_ids = {int(value) for value in request.form.getlist('active_ids') if value.isdigit()}
    valid_ids = {image.id for image in images}
    selected_ids &= valid_ids
    if not selected_ids:
        flash('Selecione pelo menos uma imagem para o carrossel.', 'warning')
        return redirect('/admin-carrossel')
    for image in images:
        image.active = image.id in selected_ids
        title = request.form.get(f'title_{image.id}', '').strip()
        if title:
            image.title = title[:120]
        set_type = request.form.get(f'set_type_{image.id}', '')
        if set_type in CAROUSEL_SET_TYPES:
            image.set_type = set_type
    ordered_images = sorted(
        images,
        key=lambda image: (
            not image.active,
            -int(os.path.getmtime(os.path.join(current_app.static_folder, 'images', image.filename)))
            if os.path.isfile(os.path.join(current_app.static_folder, 'images', image.filename)) else 0,
            -image.id,
        ),
    )
    for position, image in enumerate(ordered_images, start=1):
        image.sort_order = position * 10
    db.session.commit()
    flash(f'Carrossel atualizado com {len(selected_ids)} imagem(ns) ativa(s).', 'success')
    return redirect('/admin-carrossel')


@blueprint.route('/admin/carrossel/upload', methods=['POST'])
def upload_carousel_image():
    if not admin_required():
        return redirect('/index')
    photo = request.files.get('carousel_image')
    title = request.form.get('title', '').strip()
    set_type = request.form.get('set_type', '').strip()
    original_name = secure_filename(photo.filename or '') if photo else ''
    extension = original_name.rsplit('.', 1)[-1].lower() if '.' in original_name else ''
    if set_type not in CAROUSEL_SET_TYPES:
        flash('Selecione obrigatoriamente o tipo de conjunto.', 'danger')
        return redirect('/admin-carrossel')
    if not photo or extension not in {'jpg', 'jpeg', 'png', 'webp'}:
        flash('Selecione uma imagem JPG, PNG ou WEBP válida.', 'danger')
        return redirect('/admin-carrossel')
    photo.stream.seek(0, os.SEEK_END)
    file_size = photo.stream.tell()
    photo.stream.seek(0)
    if file_size > 8 * 1024 * 1024:
        flash('A imagem deve possuir no máximo 8 MB.', 'danger')
        return redirect('/admin-carrossel')
    signature = photo.stream.read(12)
    photo.stream.seek(0)
    valid_signature = (
        (extension in {'jpg', 'jpeg'} and signature.startswith(b'\xff\xd8\xff')) or
        (extension == 'png' and signature.startswith(b'\x89PNG\r\n\x1a\n')) or
        (extension == 'webp' and signature.startswith(b'RIFF') and signature[8:12] == b'WEBP')
    )
    if not valid_signature:
        flash('O arquivo enviado não possui um formato de imagem válido.', 'danger')
        return redirect('/admin-carrossel')
    filename = f'hero-upload-{uuid4().hex}.{extension}'
    upload_dir = os.path.join(current_app.static_folder, 'images')
    photo.save(os.path.join(upload_dir, filename))
    next_order = (db.session.query(db.func.max(CarouselImage.sort_order)).scalar() or 0) + 10
    db.session.add(CarouselImage(
        filename=filename,
        title=(title or carousel_title_from_filename(original_name))[:120],
        set_type=set_type,
        active=False,
        sort_order=next_order,
    ))
    db.session.commit()
    flash('Imagem adicionada à galeria. Ative-a quando desejar exibi-la.', 'success')
    return redirect('/admin-carrossel')


@blueprint.route('/admin/carrossel/<int:image_id>/delete', methods=['POST'])
def delete_carousel_image(image_id):
    if not admin_required():
        return redirect('/index')
    image = db.session.get(CarouselImage, image_id)
    if not image:
        flash('A imagem selecionada não foi encontrada.', 'danger')
        return redirect('/admin-carrossel')
    if image.active and CarouselImage.query.filter_by(active=True).count() <= 1:
        flash('Não é possível excluir a última imagem ativa do carrossel.', 'warning')
        return redirect('/admin-carrossel')
    filename = os.path.basename(image.filename)
    image_path = os.path.join(current_app.static_folder, 'images', filename)
    title = image.title
    db.session.delete(image)
    db.session.commit()
    if os.path.isfile(image_path):
        os.remove(image_path)
    flash(f'Imagem “{title}” excluída permanentemente da galeria.', 'success')
    return redirect('/admin-carrossel')


@blueprint.route('/<template>')
def route_template(template):
    """Serve templates with authentication protection for internal areas."""
    try:
        clean_template = template.replace('.html', '')

        # Check authentication for internal pages
        if clean_template not in PUBLIC_PAGES and not session.get('logged_in'):
            return redirect(url_for('pages_blueprint.route_template', template='auth-signin.html', next='/' + clean_template, msg='login_required'))

        if session.get('must_change_password') and clean_template != 'alterar-senha':
            return redirect(url_for('pages_blueprint.change_password'))

        if not template.endswith('.html'):
            template += '.html'

        segment = get_segment(request)
        user_role = session.get('user_role', 'usuario')
        current_user_id = session.get('user_id')
        current_user = db.session.get(User, current_user_id) if current_user_id is not None else None
        user_display_name = (current_user.full_name or current_user.username) if current_user else session.get('user_email', 'Colaborador')
        user_category = current_user.category if current_user and current_user.category in VALID_CATEGORIES else 'Orange'
        user_avatar_url = (url_for('static', filename=f'images/uploads/avatars/{current_user.avatar_filename}')
                           if current_user and current_user.avatar_filename
                           else url_for('static', filename='images/users/dummy-avatar.jpg'))
        can_edit_commission = user_role in {'admin', 'gerente'}
        can_manage_plans = user_role in {'admin', 'gerente'}
        can_validate_sales = user_role in {'admin', 'gerente'}
        if clean_template in {'admin-cadastrar', 'admin-privilegios'} and user_role != 'admin':
            return redirect('/index')
        if clean_template == 'validacao-vendas' and not can_validate_sales:
            flash('A validação de vendas é restrita a gerentes e administradores.', 'warning')
            return redirect(url_for('pages_blueprint.route_template', template='vendas'))
        sales_users = [
            {'email': user.email, 'username': user.username, 'full_name': user.full_name, 'category': user.category}
            for user in User.query.order_by(User.username.asc()).all()
        ] if clean_template in {'index', 'vendas', 'ranking'} else []
        managed_users = User.query.order_by(User.full_name.asc(), User.username.asc()).all() if clean_template in {'admin-cadastrar', 'admin-privilegios'} else []
        landing_carousel_images = active_carousel_images() if clean_template == 'landing' else []

        return render_template(
            "pages/" + template,
            segment=segment,
            user_email=session.get('user_email', ''),
            user_display_name=user_display_name,
            user_category=user_category,
            user_avatar_url=user_avatar_url,
            user_role=user_role,
            can_edit_commission=can_edit_commission,
            can_manage_plans=can_manage_plans,
            can_validate_sales=can_validate_sales,
            sales_users=sales_users,
            managed_users=managed_users,
            carousel_images=landing_carousel_images,
            permission_modules=PERMISSION_MODULES if clean_template == 'admin-privilegios' else [],
            max_privilege_emails=MAX_PRIVILEGE_EMAILS
        )

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
