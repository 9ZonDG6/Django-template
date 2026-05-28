.PHONY: check fix createsuperuser server

SAFE_MIGRATIONS_EXCLUDE_APPS ?= axes silk

define run_check
	@output_file=$$(mktemp); \
	if $(2) > $$output_file 2>&1; then \
		printf '\n\033[1;34m%s\033[0m   \033[0;32m✔ Passed\033[0m\n' "$(1)"; \
		if [ -s $$output_file ]; then \
			awk 'BEGIN { blank = "" } /^[[:space:]]*$$/ { blank = blank $$0 ORS; next } { printf "%s", blank; blank = ""; print }' $$output_file; \
		fi; \
		rm -f $$output_file; \
	else \
		status=$$?; \
		printf '\n\033[1;34m%s\033[0m   \033[0;31m✘ Failed\033[0m\n' "$(1)"; \
		if [ -s $$output_file ]; then \
			awk 'BEGIN { blank = "" } /^[[:space:]]*$$/ { blank = blank $$0 ORS; next } { printf "%s", blank; blank = ""; print }' $$output_file; \
		fi; \
		rm -f $$output_file; \
		$(if $(3),$(3) || true;) \
		exit $$status; \
	fi
endef

check:
	$(call run_check,Ruff format,uv run ruff format --check)
	$(call run_check,Ruff lint,uv run ruff check)
	$(call run_check,Ty,uv run ty check)
	$(call run_check,Django check,uv run python manage.py check)
	$(call run_check,Django makemigrations,uv run python manage.py makemigrations --check --dry-run)
	$(call run_check,Django safe migrations,uv run python manage.py check_migrations --exclude-apps $(SAFE_MIGRATIONS_EXCLUDE_APPS))
	$(call run_check,Django migrate,uv run python manage.py migrate --check,uv run python manage.py showmigrations --plan | grep "\[ \]")
	$(call run_check,Import linter,uv run lint-imports)

fix:
	$(call run_check,Ruff lint,uv run ruff check --fix)
	$(call run_check,Ruff format,uv run ruff format)

createsuperuser:
	@printf "\033[1;34mCreating Django superuser...\033[0m\n"
	@DJANGO_SUPERUSER_USERNAME="admin" \
	DJANGO_SUPERUSER_EMAIL="admin@example.com" \
	DJANGO_SUPERUSER_PASSWORD="admin" \
	uv run python manage.py createsuperuser --noinput

server:
	@printf "\033[1;34mStarting local server...\033[0m\n"
	@uv run python manage.py runserver
