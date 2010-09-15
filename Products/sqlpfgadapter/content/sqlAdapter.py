# Python imports
import logging

# Zope imports
from zope.interface import implements
from AccessControl import ClassSecurityInfo
from zope.component import getUtility

# Plone imports
from Products.Archetypes.public import Schema, StringField, StringWidget
from Products.ATContentTypes.content.base import registerATCT
from Products.CMFCore.permissions import View

# PloneFormGen imports
from Products.PloneFormGen.content.actionAdapter import FormActionAdapter, \
    FormAdapterSchema

# DB imports
from collective.lead.interfaces import IDatabase

# sqlalchemy imports
from sqlalchemy import MetaData, Table

logger = logging.getLogger("PloneFormGen")
from Products.sqlpfgadapter.config import PROJECTNAME

schema = FormAdapterSchema.copy() + Schema((
    StringField('table_id',
        widget=StringWidget(
            label = "Table",
            description = "Database table name",
            label_msgid = "label_table_id",
            description_msgid = "help_table_id",
            i18n_domain = "Products.sqlpfgadapter",
            ),
        required = True,
        ),
))

class MySQLPFGAdapter(FormActionAdapter):
    """ An adapter for PloneFOrmGen that saves results in a MySQL table
    """
    schema = schema
    security = ClassSecurityInfo()

    meta_type = portal_type = 'SQLPFGAdapter'
    archetype_name = 'MySQL Adapter'

    security.declareProtected(View, 'onSuccess')
    def onSuccess(self, fields, REQUEST=None):
        """ The essential method of a PloneFormGen Adapter.

        - collect the submitted form data
        - create a dictionary of fields which have a counterpart in the
          table
        - add a row to the table where we set the value for these fields

        """

        # Get the table, find out which columns we have.
        table_id = getattr(self, 'table_id', None)
        db = getUtility(IDatabase, name='sqlpfgadapter.mysqldb')
        engine = db.engine
        meta = MetaData(engine)
        table = Table(table_id, meta, autoload=True)
        columns = table.columns.keys()

        # Create a dictionary with the form fields. 
        # Include only fields for which a record exists.
        new_record = {}
        for field in fields:
            field_id = field.getId()
            field_value = getattr(REQUEST, field_id)
            if field_value and field_id in columns:
                new_record[field_id] = field_value
        print new_record

        # Add row. This will add an empty row if no keys from the new_record
        # dictionary are in the table.
        if new_record:
            result = table.insert().execute(new_record)

registerATCT(MySQLPFGAdapter, PROJECTNAME)
