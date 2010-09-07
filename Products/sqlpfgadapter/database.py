from collective.lead import Database
import sqlalchemy as sa

class MySQLDatabase(Database):
    """ database utility """

    @property
    def _url(self):
        return sa.engine.url.URL(
            drivername='mysql',
            username='zope',
            password='zope',
            host='localhost',
            database='test',
            )

    def _setup_tables(self, metadata, tables):
        pass

    def _setup_mappers(self, mappers, tables):
        pass 
