# Python imports
import logging

# Zope imports
from zope.interface import implements
from AccessControl import ClassSecurityInfo
from zope.component import getUtility

# Plone imports
from Products.Archetypes.public import Schema
from Products.ATContentTypes.content.base import registerATCT
from Products.CMFCore.permissions import View

# PloneFormGen imports
from Products.PloneFormGen.content.actionAdapter import \
    FormActionAdapter, FormAdapterSchema

# DB imports
from collective.lead.interfaces import IDatabase

logger = logging.getLogger("PloneFormGen")
from Products.sqlpfgadapter.config import PROJECTNAME

schema = FormAdapterSchema.copy() + Schema((
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
        """ The essential method of a PloneFormGen Adapter:
        - collect the submitted form data
        - save the data in SQL and check the result
        """
        print "onSuccess called!"
        db = getUtility(IDatabase, name='sqlpfgadapter.mysqldb')

registerATCT(MySQLPFGAdapter, PROJECTNAME)
