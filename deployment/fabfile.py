from fabric import task

site_dir = "/home/django/sites/rattletat.com/"
hosts = ["do"]


CONFIG_PRODUCTION = "config.settings.production"
ENV_VARS = [
    f"DJANGO_SETTINGS_MODULE={CONFIG_PRODUCTION}",
]
POETRY = " ".join(ENV_VARS) + " ~/.local/bin/poetry "


@task(hosts=hosts)
def deploy(c):
    c.run(f"mkdir -p {site_dir}")
    with c.cd(site_dir):
        c.run("git pull")
        c.run(POETRY + " install")
        c.run("set -a")
        c.run("source .env")
        c.run("set +a")
        c.run(POETRY + "run python3.8 manage.py collectstatic --noinput")
        c.run(POETRY + "run python3.8 manage.py compress")
        c.run(POETRY + "run python3.8 manage.py makemigrations")
        c.run(POETRY + "run python3.8 manage.py migrate --noinput")
    c.sudo("systemctl restart gunicorn.service")
    c.sudo("systemctl restart nginx.service")
