from fabric.contrib.files import append, exists
from fabric.api import cd, env, local, run, sudo, settings, hide

env.use_ssh_config = True
CONFIG_PRODUCTION = "config.settings.production"

ENV_VARS = [
    f"DJANGO_SETTINGS_MODULE={CONFIG_PRODUCTION}",
]
POETRY = " ".join(ENV_VARS) + " poetry "


def deploy(domain):
    site_folder = f"/home/{env.user}/sites/{domain}"
    run(f"mkdir -p {site_folder}")
    with cd(site_folder):
        _get_latest_source()
        _update_virtualenv()
        _create_or_update_dotenv()
        _update_static_files()
        _update_database()
        _restart_gunicorn()
        _restart_nginx()


def _get_latest_source():
    run("git fetch --all")
    run(f"git reset --hard HEAD")


def _update_virtualenv():
    run(POETRY + "install")


def _create_or_update_dotenv():
    run("set -a")
    run("cat .env")
    run("source .env")
    run("set +a")


def _update_static_files():
    run(POETRY + "run python3.8 manage.py collectstatic --noinput")


def _update_database():
    run(POETRY + "run python3.8 manage.py makemigrations")
    run(POETRY + "run python3.8 manage.py migrate --noinput")


def _restart_gunicorn():
    sudo("systemctl restart gunicorn.service")


def _restart_nginx():
    sudo("systemctl restart nginx.service")
