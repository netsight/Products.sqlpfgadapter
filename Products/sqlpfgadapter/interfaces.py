from z3c.form import interfaces

from zope import schema
from zope.interface import Interface

from zope.i18nmessageid import MessageFactory
_ = MessageFactory('Products.sqlpfgadapter')
        
class ISQLPFGSettings(Interface):
    """Database connection and other settings.
    """
    
    drivername = schema.ASCIILine(title=_(u"Database driver name"),
                                  description=_(u"The database driver name"),
                                  default='mysql',
                                  required=True)

    hostname = schema.ASCIILine(title=_(u"Database host name"),
                                description=_(u"The database host name"),
                                default='localhost',
                                required=True)
                                
    port = schema.Int(title=_(u"Database port number"),
                      description=_(u"The database port number. Leave blank to use the default."),
                      required=False)
                                
    username = schema.ASCIILine(title=_(u"Database user name"),
                                description=_(u"The database user name"),
                                required=True)

    password = schema.Password(title=_(u"Database user password"),
                                description=_(u"The database password"),
                                required=False)
                                
    database = schema.ASCIILine(title=_(u"Database name"),
                                description=_(u"The name of the database on this server"),
                                required=True)        
        
class ISQLPFGAdapter(Interface):
    """ Marker interface for SQLPFGAdapter content
    """
