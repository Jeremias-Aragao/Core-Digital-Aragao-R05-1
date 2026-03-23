from flask import Flask, session
from config import Config
from .extensions import db
from .models import Module, Plan, Subscription, User
from .public.routes import public_bp
from .auth.routes import auth_bp
from .admin.routes import admin_bp
from .client.routes import client_bp


def create_app():
    app = Flask(__name__, template_folder='../templates', static_folder='../static')
    app.config.from_object(Config)

    db.init_app(app)

    app.register_blueprint(public_bp)
    app.register_blueprint(auth_bp)
    app.register_blueprint(admin_bp)
    app.register_blueprint(client_bp)

    register_modules(app)

    with app.app_context():
        db.create_all()
        seed_data()

    @app.context_processor
    def inject_global_data():
        return {
            'current_user_name': session.get('user_name'),
            'current_user_role': session.get('role'),
        }

    return app


def register_modules(app):
    loaded_modules = []

    try:
        from .modules.financeiro.routes import financeiro_bp
        app.register_blueprint(financeiro_bp)
        loaded_modules.append('financeiro')
    except Exception as exc:
        app.logger.error('Erro ao registrar módulo financeiro: %s', exc)

    app.config['LOADED_MODULES'] = loaded_modules



def seed_data():
    if not User.query.filter_by(email='admin@digitalaragao.com').first():
        admin = User(name='Jeremias Aragão', email='admin@digitalaragao.com', role='admin')
        admin.set_password('123456')
        db.session.add(admin)

    if not User.query.filter_by(email='cliente@digitalaragao.com').first():
        client = User(name='Cliente Demo', email='cliente@digitalaragao.com', role='client')
        client.set_password('123456')
        db.session.add(client)

    if Plan.query.count() == 0:
        db.session.add_all([
            Plan(name='Start', price_monthly=29.90, description='Acesso inicial para organizar sua operação.'),
            Plan(name='Pro', price_monthly=59.90, description='Mais controle, mais módulos e mais produtividade.'),
            Plan(name='Business', price_monthly=99.90, description='Estrutura mais forte para negócios em crescimento.'),
        ])

    if Module.query.count() == 0:
        db.session.add_all([
            Module(name='Controle Financeiro', slug='financeiro', short_description='Organize entradas, saídas, caixa e visão financeira.', full_description='Módulo SaaS para controle financeiro com foco em clareza, rotina e produtividade.', category='Financeiro', module_type='saas', route_base='/modulos/financeiro', icon='💰', display_order=1, is_installed=True, is_active=True, is_public=True, show_on_home=True, status_label='Ativo'),
            Module(name='CRM (Clientes)', slug='crm', short_description='Gerencie clientes e relacionamento comercial.', full_description='Estrutura preparada para evoluir para CRM vendável no ecossistema.', category='Relacionamento', module_type='saas', route_base='/modulos/crm', icon='👥', display_order=2, is_installed=False, is_active=False, is_public=True, show_on_home=True, status_label='Em breve'),
            Module(name='Agenda Inteligente', slug='agenda-inteligente', short_description='Organize compromissos, horários e rotinas.', full_description='Módulo futuro para agenda, lembretes e produtividade.', category='Produtividade', module_type='saas', route_base='/modulos/agenda', icon='📅', display_order=3, is_installed=False, is_active=False, is_public=True, show_on_home=True, status_label='Em breve'),
            Module(name='Gerador de Documentos Inteligente', slug='gerador-documentos', short_description='Crie documentos padronizados com mais velocidade.', full_description='Módulo futuro para geração inteligente e reaproveitamento de dados.', category='Automação', module_type='saas', route_base='/modulos/documentos', icon='📄', display_order=4, is_installed=False, is_active=False, is_public=True, show_on_home=True, status_label='Em breve'),
        ])

    db.session.commit()

    client = User.query.filter_by(email='cliente@digitalaragao.com').first()
    plan = Plan.query.filter_by(name='Start').first()
    if client and plan and Subscription.query.filter_by(user_id=client.id, plan_id=plan.id).count() == 0:
        db.session.add(Subscription(user_id=client.id, plan_id=plan.id, status='active'))
        db.session.commit()
