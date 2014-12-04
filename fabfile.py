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