#!/usr/bin/python3
"""
 generates a .tgz archive from the contents
of the web_static folder
and deploy it to web servers
"""

from datetime import datetime
from fabric.api import local, put, run, env
import os.path

env.hosts = ['35.196.31.36', '35.237.103.48']


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
