run_migrations:
	python scripts/wait-for-db.py \
		&& python manage.py migrate