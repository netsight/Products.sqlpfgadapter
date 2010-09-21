from collective.lead import Database
import sqlalchemy as sa

# For using the database settings from registry
from zope.component import getUtility
from plone.registry.interfaces import IRegistry
from Products.sqlpfgadapter.interfaces import ISQLPFGSettings

class SQLDatabase(Database):
    """ database utility """

    @property
    def _url(self):
        registry = getUtility(IRegistry)
        settings = registry.forInterface(ISQLPFGSettings)

        return sa.engine.url.URL(
            drivername=settings.drivername,
            username=settings.username,
            password=settings.password,
            host=settings.hostname,
            database=settings.database,
            )

    def _setup_tables(self, metadata, tables):
        pass

    def _setup_mappers(self, mappers, tables):
        pass 
