#!/usr/bin/python

import os
import os.path as op
from flask import Flask
from flask_sqlalchemy import SQLAlchemy

import pprint
import uuid
import os


from wtforms import validators

import flask_admin as admin
from flask_admin.contrib import sqla
from flask_admin.contrib.sqla import filters

from flask import render_template

import runner

# Create application
app = Flask(__name__)

# Create dummy secrey key so we can use sessions
app.config['SECRET_KEY'] = '123456790'

# Create in-memory database
app.config['DATABASE_FILE'] = 'sample_db.sqlite'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + app.config['DATABASE_FILE']
app.config['SQLALCHEMY_ECHO'] = True
db = SQLAlchemy(app)

def get_inventory(playbook_id):
    groups = models.Group.query.all()
    return render_template("show_inventory.txt", groups = groups)


# Flask views
@app.route('/playbook/<int:playbook_id>')
def get_playbook(playbook_id):
    playbook = models.Playbook.query.get(playbook_id)
    if not playbook:
        abort(404)
    render = render_template("show_playbook.txt",playbook=playbook)
    return render, 200, {'Content-Type': 'text/plain; charset=utf-8'}

@app.route('/playbook/<int:playbook_id>/run')
def run_playbook(playbook_id):
    playbook = models.Playbook.query.get(playbook_id)
    if not playbook:
        abort(404)
    render = render_template("show_playbook.txt",playbook=playbook)
    job_id = str(uuid.uuid4())
    os.mkdir("/tmp/" + job_id)
    with open("/tmp/{0}/playbook.yml".format(job_id),'w') as f:
        f.write(render)
    with open("/tmp/{0}/inventory".format(job_id),'w') as f:
        f.write(get_inventory(playbook_id))
    runner.put(job_id)
    return job_id


if __name__ == '__main__':
    import models
    import modelviews
    
    admin = admin.Admin(app, name='Ansible Front', template_mode='bootstrap3')

    # Add views
    admin.add_view(modelviews.HostAdmin(models.Host, db.session))
    admin.add_view(modelviews.GroupAdmin(models.Group, db.session))
    admin.add_view(modelviews.TaskAdmin(models.Task, db.session))
    admin.add_view(modelviews.PlayAdmin(models.Play, db.session))
    admin.add_view(sqla.ModelView(models.Playbook, db.session))
    admin.add_view(modelviews.JobAdmin(models.Job, db.session))
    
    
    
    # Start app
    runner = runner.Runner()
    runner.run()
    app.run(debug=True,host="10.0.255.255",port=3000,use_reloader=False)
    runner.stop()
