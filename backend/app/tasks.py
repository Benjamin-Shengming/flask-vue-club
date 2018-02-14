from invoke import task, run
from datetime import datetime
@task
def translate(ctx):
    run("pybabel extract -F babel.cfg -k lazy_gettext -o messages.pot .")
    run("pybabel update -i messages.pot -d translations")
    run("pybabel compile -d translations")

@task
def git(ctx):
    now = str(datetime.now())
    run("git add .")
    run('git commit -m "{}"'.format(now))
    run("git push")
