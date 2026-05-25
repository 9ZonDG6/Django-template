.PHONY: check createsuperuser server

define run_check
	@printf '\n\033[1;34m%s\033[0m\n' "$(1)"
	@$(2); status=$$?; \
	if [ $$status -eq 0 ]; then \
		printf '   \033[0;32m✔ Passed\033[0m\n'; \
	else \
		printf '   \033[0;31m✘ Failed\033[0m\n'; \
		$(if $(3),$(3) || true;) \
		exit $$status; \
	fi
endef

check:
	$(call run_check,Ruff format,uv run ruff format)
	$(call run_check,Ruff lint,uv run ruff check --fix)
	$(call run_check,Ty,uv run ty check)
	$(call run_check,Django check,uv run python manage.py check)
	$(call run_check,Django makemigrations,uv run python manage.py makemigrations --check --dry-run)
	$(call run_check,Django migrate,uv run python manage.py migrate --check,uv run python manage.py showmigrations --plan | grep "\[ \]")

createsuperuser:
	@printf "\033[1;34mCreating Django superuser...\033[0m\n"
	@uv run python manage.py createsuperuser --noinput

server:
	@printf "\033[1;34mStarting local server...\033[0m\n"
	@uv run python manage.py runserver
