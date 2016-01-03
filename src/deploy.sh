#!/bin/bash

rsync --exclude="*.pyc" -avz registry/ arwmar@codeleet.com:/home/arwmar/rails/budget/registry/
ssh arwmar@codeleet.com "touch /home/arwmar/rails/budget/tmp/restart.txt"
