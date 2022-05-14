from cgitb import text
import os
import json
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent

def get_config():
    config = {}
    fpath = '{0}/conf/settings.json'.format(BASE_DIR)
    with open(fpath, 'r', encoding='utf8') as fp:
        config = json.load(fp)
    return config

def write_to_temp_file(fname, text):
    fpath = '{0}/temp/{1}'.format(BASE_DIR,fname)
    with open(fpath, 'w', encoding='utf8') as fp:
        fp.write(text)
    return fpath

def create_uwsgi_ini_file(config):
    fpath = '{0}/conf/uwsgi_template.ini'.format(BASE_DIR)
    text = ''
    with open(fpath, 'r', encoding='utf8') as fp:
        text = fp.read()
    webname = config['website']
    config_text = text.format(config['port'], BASE_DIR, webname)
    fname = '{0}_uwsgi.ini'.format(webname)
    return write_to_temp_file(fname, config_text)

def create_nginx_config_file(config):
    fpath = '{0}/conf/nginx_template.conf'.format(BASE_DIR)
    text = ''
    with open(fpath, 'r', encoding='utf8') as fp:
        text = fp.read()
    server_names = ' '.join(config['server_names'])
    webname = config['website']
    config_text = text.format(webname, config['port'], server_names, BASE_DIR)
    fname = '{0}_nginx.conf'.format(webname)
    return write_to_temp_file(fname, config_text)

if __name__ == '__main__':
    config = get_config()
    create_nginx_config_file(config)
    create_uwsgi_ini_file(config)
