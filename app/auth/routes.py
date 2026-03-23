from flask import Blueprint, flash, redirect, render_template, request, session, url_for
from app.extensions import db
from app.models import User


auth_bp = Blueprint('auth', __name__)


@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    if session.get('user_id'):
        return redirect(url_for('client.app_home'))

    if request.method == 'POST':
        email = request.form.get('email', '').strip().lower()
        password = request.form.get('password', '')
        user = User.query.filter_by(email=email, is_active=True).first()

        if not user or not user.check_password(password):
            flash('E-mail ou senha inválidos.', 'danger')
            return render_template('auth/login.html', login_mode='client')

        session['user_id'] = user.id
        session['user_name'] = user.name
        session['role'] = user.role
        flash('Login realizado com sucesso.', 'success')
        return redirect(url_for('client.app_home'))

    return render_template('auth/login.html', login_mode='client')


@auth_bp.route('/cadastro', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        name = request.form.get('name', '').strip()
        email = request.form.get('email', '').strip().lower()
        password = request.form.get('password', '')

        if not name or not email or not password:
            flash('Preencha todos os campos.', 'danger')
            return render_template('auth/register.html')

        if User.query.filter_by(email=email).first():
            flash('Já existe uma conta com esse e-mail.', 'warning')
            return render_template('auth/register.html')

        user = User(name=name, email=email, role='client')
        user.set_password(password)
        db.session.add(user)
        db.session.commit()

        flash('Conta criada com sucesso. Agora faça login.', 'success')
        return redirect(url_for('auth.login'))

    return render_template('auth/register.html')


@auth_bp.route('/sair')
def logout():
    session.clear()
    flash('Sessão encerrada.', 'info')
    return redirect(url_for('public.home'))
