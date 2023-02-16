#!/usr/local/bin/python3
from subprocess import call


def run():
    call(["python", "manage.py", "collectstatic", "--noinput"])
    call(["python", "manage.py", "migrate", "--noinput"])


if __name__ == '__main__':
    run()
