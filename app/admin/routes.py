from flask import Blueprint, flash, redirect, render_template, request, session, url_for
from sqlalchemy import func
from app.auth.utils import admin_required
from app.extensions import db
from app.models import Module, Subscription, User
from app.services.module_service import get_all_modules


admin_bp = Blueprint('admin', __name__, url_prefix='/admin')


@admin_bp.route('/login', methods=['GET', 'POST'])
def login():
    if session.get('role') == 'admin':
        return redirect(url_for('admin.dashboard'))

    if request.method == 'POST':
        email = request.form.get('email', '').strip().lower()
        password = request.form.get('password', '')
        user = User.query.filter_by(email=email, role='admin', is_active=True).first()

        if not user or not user.check_password(password):
            flash('Credenciais de administrador inválidas.', 'danger')
            return render_template('auth/login.html', login_mode='admin')

        session['user_id'] = user.id
        session['user_name'] = user.name
        session['role'] = user.role
        flash('Acesso administrativo liberado.', 'success')
        return redirect(url_for('admin.dashboard'))

    return render_template('auth/login.html', login_mode='admin')


@admin_bp.route('/')
@admin_required
def dashboard():
    stats = {
        'modules_total': Module.query.count(),
        'modules_active': Module.query.filter_by(is_active=True, is_installed=True).count(),
        'clients_total': User.query.filter_by(role='client').count(),
        'subscriptions_total': Subscription.query.count(),
    }
    modules = get_all_modules()
    return render_template('admin/dashboard.html', stats=stats, modules=modules)


@admin_bp.route('/modulos', methods=['GET', 'POST'])
@admin_required
def modules():
    if request.method == 'POST':
        module = Module(
            name=request.form.get('name', '').strip(),
            slug=request.form.get('slug', '').strip(),
            short_description=request.form.get('short_description', '').strip(),
            full_description=request.form.get('full_description', '').strip(),
            category=request.form.get('category', '').strip() or 'Geral',
            module_type=request.form.get('module_type', '').strip() or 'saas',
            route_base=request.form.get('route_base', '').strip(),
            icon=request.form.get('icon', '').strip() or '🧩',
            status_label=request.form.get('status_label', '').strip() or 'Ativo',
            display_order=int(request.form.get('display_order', '0') or 0),
            is_installed=request.form.get('is_installed') == 'on',
            is_active=request.form.get('is_active') == 'on',
            is_public=request.form.get('is_public') == 'on',
            show_on_home=request.form.get('show_on_home') == 'on',
        )
        db.session.add(module)
        db.session.commit()
        flash('Módulo cadastrado com sucesso.', 'success')
        return redirect(url_for('admin.modules'))

    modules = get_all_modules()
    return render_template('admin/modules.html', modules=modules)


@admin_bp.route('/modulos/<int:module_id>/toggle', methods=['POST'])
@admin_required
def toggle_module(module_id: int):
    module = Module.query.get_or_404(module_id)
    module.is_active = not module.is_active
    module.status_label = 'Ativo' if module.is_active else 'Pausado'
    db.session.commit()
    flash('Status do módulo atualizado.', 'info')
    return redirect(url_for('admin.modules'))
