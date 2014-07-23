# Python imports
import logging

# Zope imports
from zope.interface import implements
from AccessControl import ClassSecurityInfo
from AccessControl import getSecurityManager
from AccessControl import Unauthorized
from zope.component import getUtility
from DateTime import DateTime as ZopeDateTime
from datetime import datetime

# Plone imports
from Products.Archetypes.public import Schema, StringField, StringWidget
from Products.ATContentTypes.content.base import registerATCT
from Products.CMFCore.permissions import View
from Products.CMFCore.permissions import ModifyPortalContent
from plone import api

# PloneFormGen imports
from Products.PloneFormGen.content.actionAdapter import FormActionAdapter, \
    FormAdapterSchema
from Products.PloneFormGen.interfaces import IStatefulActionAdapter

# DB imports
from collective.lead.interfaces import IDatabase

# sqlalchemy imports
from sqlalchemy import MetaData, Table, Column
# sqlalchemy column types
from sqlalchemy import Integer, String, Text, Boolean, DateTime, Float

logger = logging.getLogger("Products.sqlpfgadapter")
from Products.sqlpfgadapter.config import PROJECTNAME

# Used for storing multiple values in a column
DELIMITER = '\nXXX'

# DB Columns (field names) must be shorter than this
MAX_COLUMN_SIZE = 64

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


class SQLPFGAdapter(FormActionAdapter):
    """ An adapter for PloneFormGen that saves results in an SQL table
    """
    schema = schema
    security = ClassSecurityInfo()
    implements(IStatefulActionAdapter)

    meta_type = portal_type = 'SQLPFGAdapter'
    archetype_name = 'SQL Adapter'

    def _getDB(self):
        return getUtility(IDatabase, name='sqlpfgadapter.sqldb')

    security.declareProtected(View, '_getTable')
    def _getTable(self):
        if not self.table_id:
            # not yet initialised
            return None

        db = self._getDB()
        meta = MetaData(db)
        engine = db.engine
        # For debugging: Show what we put into SQL
        #engine.echo = True
        meta.bind = engine
        return Table(self.table_id, meta, autoload=True)

    security.declareProtected(View, 'onSuccess')
    def onSuccess(self, fields, REQUEST=None):
        """ The essential method of a PloneFormGen Adapter.

        - collect the submitted form data
        - create a dictionary of fields which have a counterpart in the
          table
        - add a row to the table where we set the value for these fields

        """
        table = self._getTable()
        column_keys = table.columns.keys()

        # Create a dictionary with the form fields.
        # Include only fields for which a record exists.
        new_record = {}
        for field in fields:
            field_id = field.getId()
            if field_id in column_keys:
                value = field.getValue(REQUEST)
                if value is not None:
                    value = self._massageValue(value, field)
                    new_record[field_id] = value
                else:
                    # if it's a boolean and missing from the request
                    # then we need to set to False
                    if field.meta_type == 'FormBooleanField':
                        new_record[field_id] = False

        if self.getAllowEditPrevious():
            # Check userkey column
            if '_user_key' not in column_keys:
                logger.error('No userkey column found in database')
            # Add userkey to record
            userkey = self.getUserKey()
            new_record['_user_key'] = userkey
            # Is this the final submission?
            if self.useFinaliseWorkflow() and 'form_finalise' in REQUEST:
                new_record['_finalised'] = True
            # Look for existing rows
            whereclause = '_user_key = "%s"' % userkey
            existing = table.select(whereclause=whereclause).execute().rowcount
            if existing:
                table.update(whereclause=whereclause,
                             values=new_record).execute()
                return

        # Add new row. This will add an empty row if no keys from the new_record
        # dictionary are in the table.
        if new_record:
            table.insert().execute(new_record)

    security.declareProtected(View, 'checkUserKey')
    def checkUserKey(self, userkey):
        """ require the 'modify' permission to access
            data for userkeys other than your own """
        if userkey == self.getUserKey():
            return
        sm = getSecurityManager()
        if not sm.checkPermission(ModifyPortalContent, self):
            raise Unauthorized("You do not have permission to download this form data")

    security.declareProtected(View, 'isFinalised')
    def isFinalised(self, userkey):
        self.checkUserKey(userkey)

        table = self._getTable()
        if table is None:
            logger.error('SQL Table not initialised!')
            return False

        whereclause = '_user_key = "%s"' % userkey
        existing = table.select(whereclause=whereclause).execute().fetchone()
        if existing is None:
            return False

        value = existing['_finalised']
        return bool(value)

    security.declareProtected(View, 'hasExistingValuesFor')
    def hasExistingValuesFor(self, userkey):
        self.checkUserKey(userkey)

        table = self._getTable()
        if table is None:
            logger.error('SQL Table not initialised!')
            return False

        column_keys = table.columns.keys()
        if '_user_key' not in column_keys:
            logger.error('No userkey column found in database')
            return False

        whereclause = '_user_key = "%s"' % userkey
        existing = table.select(whereclause=whereclause).execute().fetchone()
        return existing is not None

    security.declareProtected(View, 'getExistingValueFor')
    def getExistingValueFor(self, field, userkey):
        self.checkUserKey(userkey)

        field_id = field.getId()
        table = self._getTable()
        if table is None:
            logger.error('SQL Table not initialised!')
            return None

        column_keys = table.columns.keys()
        if field_id not in column_keys:
            return None

        if '_user_key' not in column_keys:
            logger.error('No userkey column found in database')
            return None

        whereclause = '_user_key = "%s"' % userkey
        existing = table.select(whereclause=whereclause).execute().fetchone()
        if existing is None:
            return None

        value = existing[field_id]
        return self._unmassageValue(value, field)

    def createTable(self):
        """ Create a table in the database.
        This method is called after the action adapter is created.
        """
        db = self._getDB()
        meta = MetaData(db)

        table_id = self._generateTableId()

        # Create a "bare" table (python object)
        table = Table(
            table_id,
            meta,
            Column('id', Integer, primary_key=True),
        )

        # If editing previous submissions allowed
        # we need to add a user key column
        if self.getAllowEditPrevious():
            column = Column('_user_key', String(255),
                            nullable=False, default=None)
            table.append_column(column)

        # Add the form fields to the table.
        for field in self.fgFields():
            # Rename the fields if they're too big
            if len(field.__name__) > MAX_COLUMN_SIZE:
                # The field object we want to rename is in the Form folder
                ob = self[field.__name__]
                api.content.rename(obj=ob, new_id=ob.getId()[:32], safe_id=True)

            column = self._createColumn(field)
            if column is not None:
                table.append_column(column)

        # If using the finalise workflow we need to store
        # a finalised flag
        if self.useFinaliseWorkflow():
            column = Column('_finalised', Boolean(),
                            nullable=False, default=False)
            table.append_column(column)

        # Store the table in the database
        meta.create_all(db.engine)
        # Store the table's id
        self.setTable_id(table_id)

    def _generateTableId(self):
        """ Generate a useful name for the table:

        - take the action adapter's parent (the Form Folder) 's id
        - prepend it with 'pfg', append the action adapter's id
        - replace dashes with underscores (good practice in SQL)
        """
        generated_id = 'pfg_' + self.getParentNode().getId() + '_' + \
            self.getId()
        table_id = generated_id.replace('-', '_')
        return table_id

    def _createColumn(self, field):
        """ Convert a PloneFormGen field to an SQLAlchemy Column object.

        The main FormGen Field meta_types and the type they return are:
        string
            Products.Archetypes.Field.StringField
            Products.PloneFormGen.content.fieldsBase.LinesVocabularyField
            Products.PloneFormGen.content.fieldsBase.StringVocabularyField
        text
            Products.PloneFormGen.content.fields.PlainTextField
            Products.PloneFormGen.content.fields.HtmlTextField
        lines
            Products.Archetypes.Field.LinesField
        boolean
            Products.PloneFormGen.content.fields.NRBooleanField
        integer
            Products.Archetypes.Field.IntegerField
        datetime
            FormDateField
        file
            Products.Archetypes.Field.FileField
        fixedpoint
            Products.Archetypes.Field.FixedPointField
        likert
            Products.PloneFormGen.content.likertField.LikertField
        """
        column = None
        f_name = field.getName()
        logger.info('Trying to create column for: %s %s %s' % (f_name, field.type, field.__class__))
        if field.type == 'string':
            # larger storage needed for encrypted values
            if getattr(field, 'encrypted', False):
                column = Column(f_name, Text())
            else:
                column = Column(f_name, String(255), nullable=True, default=None)
        elif field.type in ['text', 'lines', 'likert']:
            column = Column(f_name, Text())
        elif field.type == 'boolean':
            column = Column(f_name, Boolean())
        elif field.type == 'integer':
            column = Column(f_name, Integer())
        elif field.type == 'datetime':
            column = Column(f_name, DateTime())
        elif field.type == 'fixedpoint':
            column = Column(f_name, Float())
        else:
            logger.error('Unsupported column type: %s' % field.type)
        return column

    def _massageValue(self, value, field):
        """ Do some extra massaging for the case of:
        - list types (store as delimited text)
        """
        if field.meta_type == 'FormDateField':
            # Use Zope's easy DateTime conversion
            zope_dt = ZopeDateTime(value)
            value = datetime.fromtimestamp(zope_dt.timeTime())
        elif field.meta_type == 'FormLikertField':
            # converts the likert dict to a comma-separated string of
            # question: answer
            items = []
            for i in range(len(value)):
                label = field.fgField.questionSet[i]
                items.append('%s: %s' % (label, value.get(str(i + 1), '')))
            value = items

        # Convert list values
        if isinstance(value, list):
            # Store lines newline-separated?
            value = DELIMITER.join(value)
        return value

    def _unmassageValue(self, value, field):
        """ Reverse the storage massaging
        """
        if field.meta_type in [
                'FormMultiSelectionField',
        ]:
            value = value and value.split(DELIMITER)
        elif field.meta_type == 'FormLikertField':
            # convert back to likert-style dict
            items = value.split(DELIMITER)
            value_dict = {}
            for i, item in enumerate(items):
                question, answer = item.split(': ', 1)
                value_dict[str(i + 1)] = answer
            value = value_dict
        return value

registerATCT(SQLPFGAdapter, PROJECTNAME)
