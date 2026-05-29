# Marketplace Artesanal API

API RESTful desenvolvida em Python, Django e Django REST Framework para um marketplace de produtos artesanais.

## Funcionalidades
- Cadastro de usuários
- Login com JWT
- Área pública para visualizar produtos ativos
- Área restrita para cadastrar, editar e excluir produtos
- CRUD de formas de venda
- Associação dos produtos ao usuário logado
- Relatório resumido por endpoint

## Como rodar
```bash
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
python manage.py makemigrations
python manage.py migrate
python manage.py runserver
```

## Endpoints
- POST `/api/usuarios/` - cadastro de usuário
- POST `/api/login/` - login JWT
- GET `/api/produtos/` - listar produtos
- POST `/api/produtos/` - cadastrar produto autenticado
- PUT `/api/produtos/{id}/` - editar produto
- DELETE `/api/produtos/{id}/` - excluir produto
- GET `/api/produtos/ativos/` - produtos ativos
- GET `/api/produtos/usuario/` - produtos do usuário logado
- POST `/api/formas-venda/` - cadastrar forma de venda
- GET `/api/relatorios/resumo/` - relatório resumido

## Token
Depois do login, use:
```text
Authorization: Bearer SEU_TOKEN_AQUI
```
