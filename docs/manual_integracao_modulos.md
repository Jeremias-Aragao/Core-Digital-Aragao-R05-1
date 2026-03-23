# Manual de Integração de Módulos

## Padrão oficial
Os módulos usam rota base no formato:

```text
/modulos/nome-do-modulo
```

## Checklist de integração
1. Criar a pasta do módulo dentro de `app/modules/`.
2. Criar `routes.py` com um Blueprint próprio.
3. Registrar o blueprint em `app/__init__.py` dentro de `register_modules()`.
4. Cadastrar o módulo na tabela `modules`.
5. Ativar o módulo no painel admin.

## Exemplo mínimo de rota
```python
from flask import Blueprint, render_template
from app.auth.utils import login_required

meu_modulo_bp = Blueprint('meu_modulo', __name__, url_prefix='/modulos/meu-modulo')

@meu_modulo_bp.route('/')
@login_required
def index():
    return render_template('modules/meu_modulo/index.html')
```

## Regra importante
O Core continua funcionando mesmo se um módulo não for registrado ou falhar no carregamento. O registro é protegido em `try/except`.
