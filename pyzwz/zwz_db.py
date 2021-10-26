from sqlalchemy import create_engine


def db_engine(dbinfo):
    engine = create_engine(
        "mysql+pymysql://{}:{}@{}/{}?charset={}".format(dbinfo['user'], dbinfo['password'], dbinfo['host']+':'+str(dbinfo['port']),
                                                        dbinfo['database'], 'utf8'))
    return engine
