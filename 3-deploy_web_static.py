#!/usr/bin/python3
"""
Fabric script (based on the file 2-do_deploy_web_static.py)
that creates and distributes an archive to your web servers,
using the function deploy:
"""

from datetime import datetime
from fabric.api import local, put, run, env
import os.path

env.hosts = ['35.196.31.36', '35.237.103.48']


def do_pack():
    """
    generate tgz archive using fabric
    """
    date = datetime.now().strftime("%Y%m%d%H%M%S")
    fil_path = "versions/web_static_{}.tgz".format(date)
    if os.path.isdir("versions") is False:
        local(" mkdir versions")
    local('tar -cvzf ' + fil_path + ' web_static')
    if os.path.exists(fil_path):
        return fil_path
    return None


def do_deploy(archive_path):
    """
        deploy archive to web servers
    """
    if os.path.exists(archive_path) is False:
        return False
    arch_nm = archive_path.split('/')[1]
    arch_nm_nex = arch_nm.split(".")[0]
    re_pth = "/data/web_static/releases/" + arch_nm_nex
    up_pth = '/tmp/' + arch_nm
    put(archive_path, up_pth)
    run('mkdir -p ' + re_pth)
    run('tar -xzf /tmp/{} -C {}/'.format(arch_nm, re_pth))
    run('rm {}'.format(up_pth))
    mv = 'mv ' + re_pth + '/web_static/* ' + re_pth + '/'
    run(mv)
    run('rm -rf ' + re_pth + '/web_static')
    run('rm -rf /data/web_static/current')
    run('ln -s ' + re_pth + ' /data/web_static/current')
    return True


def deploy():
    """
    The script should take the following steps:

    Call the do_pack() function and store the path of the created archive
    Return False if no archive has been created
    Call the do_deploy(archive_path) function,
    using the new path of the new archive
    Return the return value of do_deploy
    """
    path = do_pack()
    if (path is None):
        return False
    deploy = do_deploy(path)
    if (deploy is False):
        return False
    return deploy
