#!/usr/bin/python3
"""
This script deletes out-of-date archives,
using the function do_clean
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


def do_clean(number=0):
    """
    clean arch
    """
    try:
        number = int(number)
    except Exception:
        return False
    nb_of_arch = local('ls -ltr versions | wc -l', capture=True).stdout
    nb_of_arch = int(nb_of_arch) - 1
    if nb_of_arch <= 0 or nb_of_arch == 1:
        return True
    if number == 0 or number == 1:
        arch_to_rm = nb_of_arch - 1
    else:
        arch_to_rm = arch_to_rm - number
        if arch_to_rm <= 0:
            return True
    archives = local("ls -ltr versions | tail -n " + str(nb_of_arch) + "\
            | head -n \
            " + str(arch_to_rm) + "\
            | awk '{print $9}'", capture=True)
    archives_list = archives.rsplit('\n')
    if len(archives_list) >= 1:
        for arch in archives_list:
            if (arch != ''):
                local("rm versions/" + arch)
                run('rm -rf /data/web_static/releases/\
                    ' + arch.split('.')[0])
