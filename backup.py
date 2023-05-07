#!/usr/bin/env python

# Python
import os
import shutil
from datetime import datetime
from subprocess import Popen, PIPE

# Subprocess
from dotenv import load_dotenv


load_dotenv()

# DATABASES
DB_USER = os.getenv('DB_ROOT_USER')
DB_PASSWORD = os.getenv('DB_ROOT_PASSWORD')
DB_NAME = os.getenv('DB_NAME')

# CONTAINERS
MAIN_APP_NAME = os.getenv('MAIN_APP_NAME')      # based on docker-compose's `container_name`
DB_SERVICE_NAME = os.getenv('DB_SERVICE_NAME')  # based docker-compose's "service" name

# LOCAL BACKUP DIR
BACKUP_DIR = os.getenv('BACKUP_DIR')
BACKUP_FILE = os.getenv('BACKUP_FILE')


def execute_shell(command, strip=False, input=None):
    p = Popen(command, stdout=PIPE, stdin=PIPE, stderr=PIPE)
    out, err = p.communicate(input=input)
    if err:
        raise Exception(err.decode())
    if strip:
        return out.decode().strip()
    return out.decode()


def get_main_container_id(app_name):
    cmd = 'docker ps -qf name=%s' % app_name
    id = execute_shell(cmd.split(), strip=True)
    return id


def run_backup_sequence(container_id):
    dump = 'mysqldump -h {db_host} -u {db_user} --password="{db_pass}" {db_name} > {file}'  # noqa
    dump = dump.format(
        db_host=DB_SERVICE_NAME,
        db_user=DB_USER,
        db_pass=DB_PASSWORD,
        db_name=DB_NAME,
        file=BACKUP_FILE
    )
    cmd = ["docker", "exec", container_id, "sh", "-c", dump]  # noqa
    execute_shell(cmd)


def resolve_backup_file_name():
    date_str = datetime.today().strftime('%Y-%m-%d')

    name, ext = BACKUP_FILE.split('.')
    filename = f'{name}_{date_str}.{ext}'
    return filename


def move_file():
    curr_dir = os.path.dirname(__file__)
    backup_file = os.path.join(curr_dir, BACKUP_FILE)
    new_backup_filename = resolve_backup_file_name()
    new_backup = os.path.join(BACKUP_DIR, new_backup_filename)
    shutil.move(backup_file, new_backup)


def main():
    c_id = get_main_container_id(MAIN_APP_NAME)
    run_backup_sequence(c_id)
    move_file()



if __name__ == '__main__':
    main()
