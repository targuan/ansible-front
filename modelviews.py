from flask_admin.contrib import sqla
from flask.ext.admin.actions import action
import models

class TaskAdmin(sqla.ModelView):
    inline_models = (models.TaskVariable,)

class HostAdmin(sqla.ModelView):
    form_columns = ('name', 'groups', 'variables')
    inline_models = (models.HostVariable,)

class GroupAdmin(sqla.ModelView):
    inline_models = (models.GroupVariable,)
    column_list = ('name','hosts',)

class PlayAdmin(sqla.ModelView):
    inline_models = (models.PlayVariable,)
    column_list = ('name','groups','tasks','handlers',)

class JobAdmin(sqla.ModelView):
    form_columns = ('name', 'playbook')
    
    @action("run","Run")
    def run(self, ids):
        pass