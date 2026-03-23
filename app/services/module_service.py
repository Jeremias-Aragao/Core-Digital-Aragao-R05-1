from app.models import Module


def get_public_modules(limit: int | None = None):
    query = Module.query.filter_by(is_installed=True, is_active=True, is_public=True).order_by(Module.display_order.asc(), Module.name.asc())
    return query.limit(limit).all() if limit else query.all()


def get_all_modules():
    return Module.query.order_by(Module.display_order.asc(), Module.name.asc()).all()
