#!/usr/bin/env python

import os
import sys
from facts import get_facts
import getpass
import subprocess
from docker import DockerService, DockerContainerBuilder

def main():
    facts = get_facts()

    if not DockerService.is_running():
        DockerService.start()

    if not os.path.exists(facts['project']['docker_workspace_path']):
        os.mkdir(facts['project']['docker_workspace_path'])

    print "FIXME: disabling x access control"
    os.system('xhost +')

    DockerContainerBuilder() \
        .with_image('django') \
        .with_volume(host_path = facts['project']['path'], docker_path = '/opt/sources/budget') \
        .with_volume(host_path = facts['x']['socket_dir'], docker_path = facts['x']['socket_dir']) \
        .with_volume(host_path = facts['project']['docker_workspace_path'], docker_path = os.path.join(facts['user']['home_dir'], facts['user']['login'])) \
        .with_env(name = 'DISPLAY', value = facts['x']['display']) \
        .with_tty() \
        .with_interactive() \
        .with_publish('8000:8000') \
        .run()

if __name__ == '__main__':
    sys.exit(main())
