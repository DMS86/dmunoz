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

def update_files():
    local('git checkout gh-pages')
    local('rm *.html')
    local('rm -r escala-de-notas')
    local('rm -r site_media')
    local('git pull origin master -- _output')
    local('mv _output/* .')
    local('rm -r _output')
    local('git pull origin master -- website/site_media')
    local('mv website/site_media .')
    local('rm -r website')
    local('git commit -m 'website update'')
    local('git push origin gh-pages')
    local('git checkout master')

def deploy():
    gen()
    update_files()