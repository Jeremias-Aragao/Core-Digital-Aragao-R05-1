from flask import Blueprint, render_template
from app.models import Plan
from app.services.module_service import get_public_modules


public_bp = Blueprint('public', __name__)


@public_bp.route('/')
def home():
    modules = get_public_modules(limit=6)
    return render_template('public/home.html', modules=modules)


@public_bp.route('/sobre')
def about():
    return render_template('public/about.html')


@public_bp.route('/solucoes')
def solutions():
    modules = get_public_modules()
    return render_template('public/solutions.html', modules=modules)


@public_bp.route('/planos')
def plans():
    plans = Plan.query.filter_by(is_active=True).all()
    return render_template('public/plans.html', plans=plans)


@public_bp.route('/contato')
def contact():
    return render_template('public/contact.html')
