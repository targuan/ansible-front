import itertools
from main import db


def group_variables(variables):
    v = []
    for key, group in itertools.groupby(variables, lambda x: x.key):
        e = {"key": key,"value":[thing.value for thing in group]}
        if len(e['value']) < 2:
            e['value'] = e['value'][0]
        v.append(e)
    return v

class Task(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    action = db.Column(db.String(100))

    # Required for administrative interface. For python 3 please use __str__ instead.
    def __unicode__(self):
        return self.name
    
    def get_grouped_variables(self):
        return group_variables(self.variables)


class TaskVariable(db.Model):
    id = db.Column(db.Integer, primary_key=True)

    key = db.Column(db.String(64), nullable=False)
    value = db.Column(db.String(64))

    task_id = db.Column(db.Integer(), db.ForeignKey(Task.id))
    task = db.relationship(Task, backref='variables')

    def __unicode__(self):
        return '%s - %s' % (self.key, self.value)

host_groups_table = db.Table('host_groups', db.Model.metadata,
                           db.Column('host_id', db.Integer, db.ForeignKey('host.id')),
                           db.Column('group_id', db.Integer, db.ForeignKey('group.id')))

class Host(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    
    groups = db.relationship('Group', secondary=host_groups_table, backref='hosts')
    
    def __unicode__(self):
        return self.name

class HostVariable(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    key = db.Column(db.String(64), nullable=False)
    value = db.Column(db.String(64))
    
    host_id = db.Column(db.Integer(), db.ForeignKey(Host.id))
    host = db.relationship(Host, backref='variables')
    
    def __unicode__(self):
        return '%s - %s' % (self.key, self.value)

class Group(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    
    def __unicode__(self):
        return self.name

class GroupVariable(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    key = db.Column(db.String(64), nullable=False)
    value = db.Column(db.String(64))
    
    group_id = db.Column(db.Integer(), db.ForeignKey(Group.id))
    group = db.relationship(Group, backref='variables')
    
    def __unicode__(self):
        return '%s - %s' % (self.key, self.value)

play_groups_table = db.Table('play_groups', db.Model.metadata,
                           db.Column('play_id', db.Integer, db.ForeignKey('play.id')),
                           db.Column('group_id', db.Integer, db.ForeignKey('group.id')))
play_tasks_table = db.Table('play_tasks', db.Model.metadata,
                           db.Column('play_id', db.Integer, db.ForeignKey('play.id')),
                           db.Column('task_id', db.Integer, db.ForeignKey('task.id')))
play_handlers_table = db.Table('play_handlers', db.Model.metadata,
                           db.Column('play_id', db.Integer, db.ForeignKey('play.id')),
                           db.Column('task_id', db.Integer, db.ForeignKey('task.id')))

class Play(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    
    groups = db.relationship('Group', secondary=play_groups_table)
    tasks = db.relationship('Task', secondary=play_tasks_table)
    handlers = db.relationship('Task', secondary=play_handlers_table)
    
    def __unicode__(self):
        return self.name

class PlayVariable(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    key = db.Column(db.String(64), nullable=False)
    value = db.Column(db.String(64))
    
    play_id = db.Column(db.Integer(), db.ForeignKey(Play.id))
    play = db.relationship(Play, backref='variables')
    
    def __unicode__(self):
        return '%s - %s' % (self.key, self.value)

playbook_plays_table = db.Table('playbook_plays', db.Model.metadata,
                           db.Column('playbook_id', db.Integer, db.ForeignKey('playbook.id')),
                           db.Column('play_id', db.Integer, db.ForeignKey('play.id')))

class Playbook(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    
    plays = db.relationship('Play', secondary=playbook_plays_table)
    
    def __unicode__(self):
        return self.name


class Job(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    
    playbook_id = db.Column(db.Integer(), db.ForeignKey(Playbook.id))
    playbook = db.relationship(Playbook)
    
    def __unicode__(self):
        return self.name 

#db.drop_all()
#db.create_all()
