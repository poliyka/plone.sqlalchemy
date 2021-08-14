m ?= $(m)

upgrade:
	alembic upgrade head

migration:
	alembic revision --autogenerate -m "$(m)"