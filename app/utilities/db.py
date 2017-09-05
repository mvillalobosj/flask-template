from flask import current_app
from sqlalchemy import create_engine, event, exc
from sqlalchemy.orm import scoped_session, sessionmaker

from app.utilities.config import get_config

config = get_config()


def get_db():
    if not hasattr(current_app, 'db'):
        engine = create_engine(
            config.db.postgres.url,
            pool_size=5,
            pool_timeout=60,
            pool_recycle=3500,
            echo=config.db.postgres.echo,
        )

        # bind event handlers on the engine
        event.listen(engine, 'checkout', checkout)

        db_session = scoped_session(sessionmaker(
            autocommit=False, autoflush=False, bind=engine))

        current_app.db = db_session
    return current_app.db()


def checkout(dbapi_connection, connection_record, connection_proxy):
    """Do a ping query on the database to ensure connection is not closed.
    This is to ensure the connection is always fresh if was closed when it was
    checked out from the pool."""

    cursor = dbapi_connection.cursor()
    try:
        cursor.execute("""SELECT 1""")
    except:
        current_app.logger.error('msg=connection was lost;')
        raise exc.DisconnectionError()
    finally:
        cursor.close()
