#!/usr/bin/env python
# -*- coding: utf-8 -*-

import yaml

from os import path as p
from pprint import pprint
from io import open
from flask import current_app as app
from flask.ext.script import Manager
from app import create_app

manager = Manager(create_app)
manager.add_option(
	'-m', '--cfgmode', dest='config_mode', default='Development')
manager.add_option('-f', '--cfgfile', dest='config_file', type=p.abspath)


def make_safe(name):
	return name.replace(' ', '_').replace('&', 'and').replace('/', '-').lower()

def render_app(app, style):
	"""Renders the markup"""
	with app.test_client() as c:
		response = c.get('/render/%s/' % style)
		encoding = response.charset
		return response.data.decode(encoding)


@manager.option('-i', '--info', help='the client info file, defaults to info.yml')
@manager.option('-s', '--style', help='the proposal style, defaults to development')
def propose(info=None, style=None):
	"""Create Proposal"""
	style = (style or app.config['STYLE'])
	app.config['INFO_PATH'] = (info or app.config['INFO_PATH'])
	stream = file(app.config['INFO_PATH'], 'r')
	details = yaml.safe_load(stream)
	client_name = details['short_company_name']
	projec_name = details['project_name']
	safe_name = make_safe('%s_%s' % (client_name, projec_name) )
	html_file = p.join(app.config['EXPORT_DIR'], '%s_proposal.html' % safe_name)
	content = render_app(app, style)

	with open(html_file, 'w', encoding='utf-8') as f:
		f.write(content)


if __name__ == '__main__':
	manager.run()