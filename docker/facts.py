#!/usr/bin/env python

import os

def _user_facts():
    import getpass, pwd
    login = getpass.getuser()
    pw_entry = pwd.getpwnam(login)
    return dict(
        login = login,
        uid = pw_entry.pw_uid,
        gid = pw_entry.pw_gid,
        home_dir = '/home',
    )

def _x_facts():
    return dict(
        display = os.environ.get('DISPLAY'),
        socket_dir = '/tmp/.X11-unix',
    )

def _project_facts():
    script_path = os.path.dirname(os.path.realpath(__file__))
    return dict(
        path = os.path.join(script_path, '..'),
        docker_workspace_path = os.path.join(script_path, 'home'),
        display = os.environ.get('DISPLAY'),
    )


def get_facts():
    return dict(
        x = _x_facts(),
        user = _user_facts(),
        project = _project_facts()
    )
