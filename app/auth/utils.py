from functools import wraps
from flask import session, redirect, url_for, flash


def login_required(view_func):
    @wraps(view_func)
    def wrapper(*args, **kwargs):
        if not session.get('user_id'):
            flash('Faça login para acessar esta área.', 'warning')
            return redirect(url_for('auth.login'))
        return view_func(*args, **kwargs)
    return wrapper


def admin_required(view_func):
    @wraps(view_func)
    def wrapper(*args, **kwargs):
        if not session.get('user_id'):
            flash('Faça login como administrador.', 'warning')
            return redirect(url_for('admin.login'))
        if session.get('role') != 'admin':
            flash('Acesso restrito à administração.', 'danger')
            return redirect(url_for('client.app_home'))
        return view_func(*args, **kwargs)
    return wrapper
