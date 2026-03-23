from datetime import datetime, date
from flask import Blueprint, flash, redirect, render_template, request, session, url_for
from sqlalchemy import func
from app.auth.utils import login_required
from app.extensions import db
from app.models import FinancialEntry


financeiro_bp = Blueprint('financeiro', __name__, url_prefix='/modulos/financeiro')


@financeiro_bp.route('/')
@login_required
def index():
    user_id = session['user_id']
    entries = FinancialEntry.query.filter_by(user_id=user_id).order_by(FinancialEntry.reference_date.desc(), FinancialEntry.id.desc()).all()
    total_entries = db.session.query(func.coalesce(func.sum(FinancialEntry.amount), 0.0)).filter_by(user_id=user_id, entry_type='entrada').scalar()
    total_exits = db.session.query(func.coalesce(func.sum(FinancialEntry.amount), 0.0)).filter_by(user_id=user_id, entry_type='saida').scalar()
    today = date.today()
    month_entries = db.session.query(func.coalesce(func.sum(FinancialEntry.amount), 0.0)).filter(
        FinancialEntry.user_id == user_id,
        FinancialEntry.entry_type == 'entrada',
        func.extract('month', FinancialEntry.reference_date) == today.month,
        func.extract('year', FinancialEntry.reference_date) == today.year,
    ).scalar()
    month_exits = db.session.query(func.coalesce(func.sum(FinancialEntry.amount), 0.0)).filter(
        FinancialEntry.user_id == user_id,
        FinancialEntry.entry_type == 'saida',
        func.extract('month', FinancialEntry.reference_date) == today.month,
        func.extract('year', FinancialEntry.reference_date) == today.year,
    ).scalar()

    stats = {
        'saldo_total': total_entries - total_exits,
        'entradas_mes': month_entries,
        'saidas_mes': month_exits,
    }
    return render_template('modules/financeiro/index.html', entries=entries, stats=stats)


@financeiro_bp.route('/novo', methods=['GET', 'POST'])
@login_required
def create():
    if request.method == 'POST':
        description = request.form.get('description', '').strip()
        category = request.form.get('category', '').strip()
        entry_type = request.form.get('entry_type', '').strip()
        amount_raw = request.form.get('amount', '').replace(',', '.').strip()
        reference_date_raw = request.form.get('reference_date', '').strip()
        notes = request.form.get('notes', '').strip()

        if not all([description, category, entry_type, amount_raw, reference_date_raw]):
            flash('Preencha os campos obrigatórios.', 'danger')
            return render_template('modules/financeiro/form.html')

        try:
            amount = float(amount_raw)
            reference_date = datetime.strptime(reference_date_raw, '%Y-%m-%d').date()
        except ValueError:
            flash('Valor ou data inválidos.', 'danger')
            return render_template('modules/financeiro/form.html')

        entry = FinancialEntry(
            user_id=session['user_id'],
            description=description,
            category=category,
            entry_type=entry_type,
            amount=amount,
            reference_date=reference_date,
            notes=notes,
        )
        db.session.add(entry)
        db.session.commit()
        flash('Lançamento salvo com sucesso.', 'success')
        return redirect(url_for('financeiro.index'))

    return render_template('modules/financeiro/form.html')


@financeiro_bp.route('/<int:entry_id>/excluir', methods=['POST'])
@login_required
def delete(entry_id):
    entry = FinancialEntry.query.filter_by(id=entry_id, user_id=session['user_id']).first_or_404()
    db.session.delete(entry)
    db.session.commit()
    flash('Lançamento excluído.', 'info')
    return redirect(url_for('financeiro.index'))
