from plone.app.registry.browser import controlpanel

from Products.sqlpfgadapter.interfaces import ISQLPFGSettings
from Products.sqlpfgadapter.interfaces import _

class SQLPFGSettingsEditForm(controlpanel.RegistryEditForm):
    schema = ISQLPFGSettings
    label = _(u"SQL-PFG Adapter Settings")
    description = _(u"""""")

    def updateFields(self):
        super(SQLPFGSettingsEditForm, self).updateFields()
        
    def updateWidgets(self):
        super(SQLPFGSettingsEditForm, self).updateWidgets()

class SQLPFGSettingsControlPanel(controlpanel.ControlPanelFormWrapper):
    form = SQLPFGSettingsEditForm
