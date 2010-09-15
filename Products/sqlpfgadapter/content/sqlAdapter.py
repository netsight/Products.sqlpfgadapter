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
from sqlalchemy import MetaData, Table, Column, Integer, String

logger = logging.getLogger("PloneFormGen")
from Products.sqlpfgadapter.config import PROJECTNAME

schema = FormAdapterSchema.copy() + Schema((
    StringField('table_id',
        widget=StringWidget(
            label = "Database table name",
            description = """A database table with this name was added when the action adapter was created. The submitted forms will be stored in this table. Its name is provided here so you know where to find the saved forms.  """,
            label_msgid = "label_table_id",
            description_msgid = "help_table_id",
            i18n_domain = "Products.sqlpfgadapter",
            visible = {'edit': 'hidden', 'view': 'visible'},
            ),
        required = False,
        ),
))

class MySQLPFGAdapter(FormActionAdapter):
    """ An adapter for PloneFOrmGen that saves results in a MySQL table
    """
    schema = schema
    security = ClassSecurityInfo()

    meta_type = portal_type = 'SQLPFGAdapter'
    archetype_name = 'MySQL Adapter'

    def _getDB(self):
        return getUtility(IDatabase, name='sqlpfgadapter.mysqldb')
            
    security.declareProtected(View, 'onSuccess')
    def onSuccess(self, fields, REQUEST=None):
        """ The essential method of a PloneFormGen Adapter.

        - collect the submitted form data
        - create a dictionary of fields which have a counterpart in the
          table
        - add a row to the table where we set the value for these fields

        """

        # Get the table, find out which columns we have.
        db = self._getDB()
        meta = MetaData(db)
        engine = db.engine
        meta.bind = engine
        table = Table(self.table_id, meta, autoload=True)
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

    def createTable(self):
        """ Create a table in the database.
        This method is called after the action adapter is created.
        """
        db = self._getDB()
        meta = MetaData(db)

        table_id = self.generateTableId()

        # Create a "bare" table (python object)
        table = Table(
            table_id, 
            meta,
            Column('id', Integer, primary_key=True),
            )
        # Add the form fields to the table.
        for field in self.fgFields():
            f_name = field.getName()
            print f_name, field.type()
            if field.type == 'string':
                table.append_column(Column(
                    f_name, 
                    String(255), 
                    nullable=True,
                    default=None,
                    ))

        # Store the table in the database
        meta.create_all(db.engine)
        # Store the table's id
        self.setTable_id(table_id)
        
    def generateTableId(self):
        """ Generate a useful name for the table. 

        For now, we di this:
        - take the action adapter's parent (the Form Folder) 's id
        - prepend it with 'pfg'
        - replace dashes with underscores (good practice in SQL)

        In the future we might make the table id's customizable. 
        """
        return 'pfg_' + self.getParentNode().getId().replace('-','_')

registerATCT(MySQLPFGAdapter, PROJECTNAME)
