# Core Digital Aragão R05.1

Base arquitetural modular do Core Digital Aragão.

## O que esta versão entrega
- Core público premium
- páginas públicas principais
- admin separado
- área do cliente separada
- engine de módulos
- módulo Financeiro já integrado
- manual de integração de módulos
- estrutura preparada para SaaS

## Logins demo
### Admin
- admin@digitalaragao.com
- 123456

### Cliente
- cliente@digitalaragao.com
- 123456

## Rodar localmente
```bash
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
python app.py
```

## Deploy no Render
- Build Command: `pip install -r requirements.txt`
- Start Command: `gunicorn wsgi:app`
