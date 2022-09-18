"""
Database access module
~~~~~~~~~~~~~~~~~~~~~

Helper functions to connect and work with sql data
"""

import pandas as pd
from sqlalchemy import create_engine, text as sqlalchemytext
from snowflake.sqlalchemy import URL

def get_pymssql_url(host, dbname, user, password):
    "Get SQL Alchemy URL for MSSQL database"
    return f"mssql+pymssql://{user}:{password}@{host}/{dbname}"

def get_snowflake_url(account,user,password,database,schema,warehouse,role):
    "Get SQL Alchemy URL for Snowflake database"
    return URL(
            account=account,
            user=user,
            password=password,
            database=database,
            schema=schema,
            warehouse=warehouse,
            role=role
            #timezone=config_dict["SNOWFLAKE_TIMEZONE"],
        )

# def get_sqla_engine(**connection_kwargs):
#     '''Get/Create SQLAlchemy engine'''
#     engine = create_engine(config.SQLALCHEMY_URI, convert_unicode=True, **connection_kwargs)
#     return engine

# def get_sqla_session(**kwargs):
#     '''Get new SQLAlchemy session'''
#     # create a configured "Session" class
#     Session = sessionmaker(bind=get_sqla_engine(), **kwargs) #pylint: disable=invalid-name
#     # create a Session
#     session = Session()
#     return session

class DBSession():
    """ Database session to access and work with sql data """
    conn = None

    def __init__(self,connection_url, **connection_kwargs):
        self.connection_url = connection_url
        self.engine = create_engine(self.connection_url, **connection_kwargs)

    def connect(self):
        """ Connect to the database server """
        self.conn = self.engine.connect()

    def is_connected(self):
        """ Is connected """
        return self.conn is not None

    def close(self, silent=True):
        """ Close connection """
        if self.conn is not None:
            # if commit:
            #     self.conn.commit()
            self.conn.close()
            self.engine.dispose()
            if not silent:
                print('Database connection closed.')

    def execute_sql(self, sql):
        """ Execute sql """
        return self.conn.execute(sqlalchemytext(sql))
        # with self.conn.cursor() as cur:
        #     cur.execute(sql)

    def execute_with_data(self, sql, data):
        """ Execute sql with data """
        with self.conn.cursor() as cur:
            cur.execute(sql,data)

    def fetch_one(self, sql):
        """ Return single row from sql dataset """
        self.execute_sql(sql).fetchone()
        # with self.conn.cursor() as cur:
        #     cur.execute(sql)
        #     return cur.fetchone()

    def fetch_all(self, sql):
        """ Returns all rows from a sql dataset """
        result = self.execute_sql(sql).fetchall()
        return result
        # with self.conn.cursor(cursor_factory = DictCursor) as cur:
        #     cur.execute(sql)
        #     return cur.fetchall()

    def fetch_all_as_pd(self, sql):
        """ Fetch results of query as pandas data frame """
        return pd.read_sql_query(sql, self.conn)

    def fetch_all_as_parquet(self, sql, output_file, compression='gzip'):
        """ Fetch results of query as parquet data file"""
        data = pd.read_sql_query(sql, self.conn)
        data.to_parquet(output_file, compression=compression)


def fetch_data_to_parquet_file(db_url, input_sql, output_file, compression='gzip'):
    '''Save dataset from sql into local parquet file'''
    print("Persisting data to local file: {0}".format(output_file))
    ldf = pd.read_sql_query(input_sql, db_url)
    ldf.to_parquet(output_file, compression=compression)
    return ldf
