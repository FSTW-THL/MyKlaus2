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
    data = {
        'Elektrotechnik und Informatik': [
            'Elektrotechnik - Energiesysteme und Automation',
            'Elektrotechnik - Kommunikationssysteme',
            'Informatik/ Softwaretechnik',
            'Informationstechnologie und Design',
            'Medieninformatik Online',
            'Regenerative Energien Online',
            'Angewandte Informationstechnik'],
        'Angewandte Naturwissenschaften': [
            'Biomedizintechnik',
            'Chemie- und Umwelttechnik (auslaufend)',
            'Hörakustik',
            'Hörakustik und Audiologische Technik',
            'Physikalische Technik',
            'Biomedical Engineering',
            'Technische Biochemie',
            'Angewandte Chemie',
            'Umweltingenieurwesen und -management',
            'Regulatory Affairs'],
        'Bauwesen': [
            'Environmental Engineering',
            'Bauingenieurwesen',
            'Architektur',
            'Städtebau und Ortsplanung',
            'Energie- und Gebäudeingenieurwesen'],
        'Maschinenbau und Wirtschaft': [
            'Betriebswirtschaftslehre',
            'Maschinenbau',
            'Mechanical Engineering',
            'Wirtschaftsingenieurwesen',
            'Wirtschaftsingenieurwesen Lebensmittelindustrie (vormals Food Processing)',
            'Wirtschaftsingenieurwesen Online']
    }

    import MyKlaus2.models
    Base.metadata.create_all(engine)

    from MyKlaus2.models import Department, CourseOfStudy

    for department in data:
        dep = Department(name=department)
        db_session.add(dep)
        db_session.commit()
        for courseofstudy in data[department]:
            cos = CourseOfStudy(courseofstudy, dep)
            db_session.add(cos)
    
    db_session.commit()
    #db_session.add_all([
    #    Department(name='Angewandte Naturwissenschaften'),
    #    Department(name='Bauwesen'),
    #    Department(name='Elektortechnik & Informatik'),
    #    Department(name='Maschinenbau & Wirtschaft')
    #])
    #db_session.commit()

    print('Initialized the database.')
