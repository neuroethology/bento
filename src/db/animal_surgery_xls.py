# xls.py
"""
animal_surgery_xls.py
Import experimental animal and surgery data in xls (Excel spreadsheet) format
into Python Bento's database, using SQLAlchemy and xlrd.
"""

import xlrd
from db.schema_sqlalchemy import new_session, Investigator, Animal, LateralityEnum, SexEnum, Surgery
from os.path import abspath

def check_value(field, fieldname, value):
    if field == value:
        return False
    if field:
          print(f"Existing value in field {fieldname} ({field}) didn't match supplied value: {value}")
    return True

def laterality_from_xls(value):
    val = value.lower()
    if val == 'uni':
        return LateralityEnum.Left
    if val == 'r':
        return LateralityEnum.Right
    if val == 'bi':
        return LateralityEnum.Bilateral
    return LateralityEnum.Nothing

def import_row(investigator, xls_sheet, row, session):
    """
    Import a row of animal/surgery data

    Column info:
        0:  Section (not imported)
        1:  Stain (not imported)
        2:  Picture (not imported)
        3:  <what is this called?> (not imported)
        4:  Nickname (imported)
        5:  Strain (imported as genotype)
        6:  Animal ID
        7:  date of birth
        8:  Surgery date
        9:  age in weeks (not imported)
        10: weeks after surgery (not imported)
        11: Injected virus (imported as "procedure", along with "amount")
        12: Purpose (not imported)
        13: Amount (imported as part of "procedure")
        14: Injection site (not imported)
        15: Uni/Bi (imported as "injection_side")
        16: implant (not imported)
        17: Uni/Bi (imported as "implant_side")
        18: Perfusion date (not imported)
        19: Comments (not imported)
        20: Behavior test (not imported)
        21: Body weight in grams (not imported)
        22: Anesthetic (imported as "anesthesia")
        23: Analgesic (impoted as "followup_care")
    """
    
    animal_id = int(xls_sheet.cell_value(row, 6))
    print(f"Importing animal and surgery on row {row}, animal id {animal_id}")

    dob = xlrd.xldate_as_datetime(xls_sheet.cell_value(row, 7), 0).date()
    genotype = xls_sheet.cell_value(row, 5).strip()
    sex = SexEnum.F if genotype.find('female') >= 0 else SexEnum.M
    query = session.query(Animal)
    query = query.filter(Animal.animal_services_id == animal_id)
    query = query.filter(Animal.dob == dob)
    query = query.filter(Animal.genotype == genotype)
    query = query.filter(Animal.investigator_id == investigator.id)
    animals = query.all()
    if len(animals) > 1:
        print(f"Database error: more than one animal with the same ID: {animals[0].id}")
        return
    nickname = xls_sheet.cell_value(row, 4).replace('#', '').strip()
    if len(animals) == 0:
        # import the animal information
        animal = Animal()
        animal.animal_services_id = animal_id
        animal.dob = dob
        animal.sex = sex
        animal.genotype = genotype
        animal.nickname = nickname
        animal.investigator_id = investigator.id
        session.add(animal)
        session.commit()
    else:
        # check and update the animal information as necessary
        animal = animals[0]
        if check_value(animal.sex, 'animal.sex', sex):
            animal.sex = sex
        if check_value(animal.nickname, 'animal.nickname', nickname):
            animal.nickname = nickname
        session.commit()

    # import surgery data
    surgeries = session.query(Surgery).filter(Surgery.animal_id == animal.id, Surgery.investigator_id == investigator.id).all()
    if len(surgeries) > 0:
        return    # previously entered; skip

    surgery = Surgery()

    surgery.animal_id = animal.id
    surgery.investigator_id = investigator.id
    surgery.date = xlrd.xldate_as_datetime(xls_sheet.cell_value(row, 8), 0).date()
    surgery.injection_side = laterality_from_xls(xls_sheet.cell_value(row, 15))
    surgery.implant_side = laterality_from_xls(xls_sheet.cell_value(row, 17))
    surgery.procedure = xls_sheet.cell_value(row, 11) + ", " + xls_sheet.cell_value(row, 13)
    surgery.anesthesia = xls_sheet.cell_value(row, 22)
    surgery.follow_up_care = xls_sheet.cell_value(row, 23)

    session.add(surgery)
    session.commit()

def import_xls_file(file_path, db_session, investigator):
    abs_path = abspath(file_path)
    xls = xlrd.open_workbook(abs_path)
    sheet = xls.sheets()[0]

    for row in range(1, sheet.nrows):
        if sheet.cell_type(row, 6) != xlrd.XL_CELL_NUMBER:
            continue
        import_row(investigator, sheet, row, db_session)

def do_import(investigator_name, rel_path):
    db_sessionMaker = new_session()
    db_sess = db_sessionMaker()
    investigators = db_sess.query(Investigator).filter(Investigator.user_name == investigator_name).all()
    assert len(investigators) == 1
    investigator = investigators[0]

    import_xls_file(rel_path, db_sess, investigator)

