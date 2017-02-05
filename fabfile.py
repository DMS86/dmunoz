from fabric.api import local

# restart local db and server
def restart(branch=None):
    try:
        local('rm dev.db')
    except:
        pass
    local('python manage.py syncdb --noinput')
    local('python manage.py loaddata sites')
    if branch is not None:
        local('python manage.py loaddata ' + branch)
    local('python manage.py runserver')

def gen():
    local('python manage.py staticsitegen')
    local('python manage.py collectstatic --noinput')
    try:
        local('git add .')
        local("git commit -m 'update html'")
    except:
        pass
    local('git push origin master')

def update_files():
    local('git checkout gh-pages')
    try:
        local('rm *.html')
    except:
        pass
    try:
        local('rm -r escala-de-notas')
    except:
        pass
    try:
        local('rm -r postparental-transition')
    except:
        pass
    try:
        local('rm -r site_media')
    except:
        pass
    local('git checkout master -- _output')
    local('mv _output/* .')
    local('rm -r _output')
    local('git checkout master -- website/site_media')
    local('mv website/site_media .')
    local('rm -r website')
    local('git add --all')
    try:
        local("git commit -m 'website update'")
        local('git push origin gh-pages')
    except:
        pass
    local('git checkout master')

def deploy():
    gen()
    update_files()