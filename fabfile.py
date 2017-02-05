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
    local('git add .')
    try:
        local("git commit -m 'update html'")
    except:
        pass
    local('git push origin master')

def update_files():
    local('git checkout gh-pages')
    local('rm *.html')
    local('rm -rf escala-de-notas')
    local('rm -rf postparental-transition')
    local('rm -rf site_media')
    local('rm -rf blog')
    local('git checkout master -- _output')
    local('mv _output/* .')
    local('rm -r _output')
    local('git checkout master -- website/site_media')
    local('mv website/site_media .')
    local('rm -r website')
    local('git add --all')
    local("git commit -m 'website update'")
    local('git push origin gh-pages')
    local('git checkout master')

def deploy():
    gen()
    update_files()