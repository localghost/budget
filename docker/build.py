#!/usr/bin/env python

import os
import sys
from facts import get_facts
import docker

def main():
    facts = get_facts()

    if not docker.DockerService.is_running():
        docker.DockerService.start()

    try:
        docker.DockerfileBuilder() \
            .with_template(os.path.join(facts['project']['path'], 'docker', 'Dockerfile.tpl')) \
            .with_vars(facts['user']) \
            .with_output(os.path.join(facts['project']['path'], 'docker', 'Dockerfile')) \
            .build()

        docker.Docker().build(path=os.path.join(facts['project']['path'], 'docker'), tag='django')
    finally:
        if os.path.exists('Dockerfile'):
           os.unlink('Dockerfile')

if __name__ == '__main__':
    sys.exit(main())
