from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from MyKlaus2 import app
engine = create_engine(
    app.config['SQLALCHEMY_DATABASE_URI'],
    connect_args = {
        'port': int(app.config['SQLALCHEMY_DATABASE_PORT'])
    },
    echo='debug',
    echo_pool=True
)

db_session = scoped_session(
    sessionmaker(
        bind=engine,
        autocommit=False,
        autoflush=False
    )
)

Base = declarative_base()

def init_db():
    import MyKlaus2.models
    Base.metadata.create_all(engine)

    from MyKlaus2.models import Department
    db_session.add_all([
        Department(name='Angewandte Naturwissenschaften'),
        Department(name='Bauwesen'),
        Department(name='Elektortechnik & Informatik'),
        Department(name='Maschinenbau & Wirtschaft')
    ])
    db_session.commit()

    print('Initialized the database.')
