from flask import Blueprint, render_template, session
from app.auth.utils import login_required
from app.models import Subscription
from app.services.module_service import get_public_modules


client_bp = Blueprint('client', __name__, url_prefix='/app')


@client_bp.route('/')
@login_required
def app_home():
    modules = get_public_modules()
    subscriptions = Subscription.query.filter_by(user_id=session['user_id']).all()
    return render_template('client/home.html', modules=modules, subscriptions=subscriptions)
