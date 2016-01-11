#!/usr/bin/python

import os
import subprocess


class DockerfileBuilder(object):
    def __init__(self):
        self.__reset()

    def with_template(self, path):
        self.__template_path = path
        return self

    def with_vars(self, variables):
        self.__variables.update(variables)
        return self

    def with_output(self, path):
        self.__output_path = path
        return self

    def build(self):

        try:
            contents = self.__read_template()
            contents = self.__fill_template(contents)
            self.__write_dockerfile(contents)
        finally:
            self.__reset()

        return self.__output_path

    def __read_template(self):
        with open(self.__template_path) as f:
            return f.read()

    def __fill_template(self, contents):
        return contents.format(**self.__variables)

    def __write_dockerfile(self, contents):
        with open(self.__output_path, 'w') as f:
            f.writelines(contents)

    def __reset(self):
        self.__variables = {}
        self.__template_path = None
        self.__output_path = None

class DockerService(object):
    @staticmethod
    def is_running():
        return subprocess.call('service docker status >/dev/null 2>&1', shell=True) == 0

    @staticmethod
    def start():
        subprocess.check_call('sudo service docker start', shell=True)


class Docker(object):
    def build(self, path, tag=None):
        command = 'docker build --no-cache'
        
        if tag:
            command += ' -t %s' % tag

        command += ' "%s"' % path

        self.__call(command)

    def run(self, image, volumes=None): # DEPRECATED
        command = 'docker run -it --rm'
        if volumes:
            command += ''.join([' -v %s ' % volume for volume in volumes])
        command += ' -e DISPLAY=%s' % os.environ.get('DISPLAY') # FIXME fx this ugliness
        command += ' %s' % image
        self.__call(command)

    def __call(self, *args):
        print args
        subprocess.call(*args, shell=True)

class DockerContainerBuilder(object):
    def __init__(self):
        self.__reset()

    def with_volume(self, host_path, docker_path, read_only = False):
        volume = '%s:%s' % (host_path, docker_path)

        if read_only:
            volume += ':ro'

        self.__volumes.append(volume)
        return self

    def with_mirror_volume(self, path, read_only = False):
        return self.with_volume(host_path = path, docker_path = path, read_only = read_only)

    def with_interactive(self):
        self.__interactive = True
        return self

    def with_tty(self):
        self.__tty = True
        return self

    def with_privileged(self):
        self.__privileged = True
        return self

    def with_image(self, image):
        self.__image = image
        return self

    def with_env(self, name, value):
        self.__envs.append('%s=%s' % (name, value))
        return self

    def with_command(self, command):
        self.__command = command
        return self

    def with_publish_all(self):
        self.__publish_all = True
        return self

    def with_publish(self, spec):
        self.__publish.append(spec)
        return self

    def run(self, remove_on_exit=True):
        assert self.__image, "Docker image must be provided"

        command = 'docker run'

        if remove_on_exit:
            command += ' --rm'

        command += ' --privileged=%d' % self.__boolToInt(self.__privileged)
        command += ' --interactive=%d' % self.__boolToInt(self.__interactive)
        command += ' --publish-all=%d' % self.__boolToInt(self.__publish_all)
        command += ' --tty=%d' % self.__boolToInt(self.__tty)
        command += ''.join([' --volume %s' % volume for volume in self.__volumes])
        command += ''.join([' --env %s' % env for env in self.__envs])
        command += ''.join([' --publish %s' % spec for spec in self.__publish])

        command += ' %s' % self.__image

        if self.__command:
            command += ' %s' % command

        subprocess.check_call(command, shell=True)

        self.__reset()

    def __reset(self):
        self.__volumes = []
        self.__envs = []
        self.__publish = []
        self.__image = None
        self.__tty = False
        self.__interactive = False
        self.__privileged = False
        self.__publish_all = False
        self.__command = None

    def __boolToInt(self, value):
        return 1 if value else 0

    def __call(self, *args):
        print args
        return 
