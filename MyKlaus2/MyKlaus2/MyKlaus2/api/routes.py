from flask import Blueprint, request, jsonify, send_from_directory, send_file
from sqlalchemy import desc, or_, and_, func
from sqlalchemy_paginator import Paginator
from MyKlaus2 import app
from MyKlaus2.database import db_session
from MyKlaus2.models import Exam, Course, Department, ExamType, Professor
from pydrive.auth import GoogleAuth
from pydrive.drive import GoogleDrive
import os.path
import json
import zipfile
import smtplib

api = Blueprint("api", __name__)

def to_serializable_dict(lst):
    res = []
    for item in lst:
        res.append(item.to_serializable_dict())
    return res

def order_by(query, field, table, subfield, doDesc):
    query = query.join(table, field) 
    if doDesc:
        return query.order_by(desc(subfield))
    else:
        return query.order_by(subfield)

def sort_exams(exams_query, data):
    if data.get("sort[0]") in ["0", "1"]: #Fachbereich
        exams_query = order_by(exams_query, Exam.department, Department, Department.name, int(data.get("sort[0]")))

    if data.get("sort[1]") in ["0", "1"]: #Fach
        exams_query = order_by(exams_query, Exam.course, Course, Course.name, int(data.get("sort[1]")))

    if data.get("sort[2]") in ["0", "1"]: #Typ
        exams_query = order_by(exams_query, Exam.examType, ExamType, ExamType.name, int(data.get("sort[2]")))

    if data.get("sort[3]") in ["0", "1"]: #Dozent
        exams_query = order_by(exams_query, Exam.professor, Professor, Professor.lastName, int(data.get("sort[3]")))
        
    if data.get("sort[4]") == "0": #Semester
        exams_query = exams_query.order_by(Exam.year)
    elif data.get("sort[4]") == "1":
        exams_query = exams_query.order_by(desc(Exam.year))

    return exams_query

def pager(data):
    if data.get("page"):
        page = int(data.get("page"))
    else:
        page = 1

    if data.get("per_page"):
        per_page = int(data.get("per_page"))
    else:
        per_page = 25

    return page, per_page

@api.route('/api/getExam', methods=['GET'])
def getExam():
    data = request.args
    exams_query = db_session.query(Exam)
    has_filter = False
    filter_condition = None
    #filterung
    if data.get("filter[0]"): #Fachbereich
        exams_query = exams_query.join(Department, Exam.department)
        if not has_filter:
            filter_condition = Department.name.like("%" + data.get("filter[0]") + "%")
        has_filter = True

    if data.get("filter[1]"): #Fach
        exams_query = exams_query.join(Course, Exam.course)
        cond = Course.name.like("%" + data.get("filter[1]") + "%")
        if not has_filter:
            filter_condition = cond
        else:
            filter_condition = and_(filter_condition, cond)
        has_filter = True

    if data.get("filter[2]"): #Typ
        exams_query = exams_query.join(ExamType, Exam.examType)
        cond = ExamType.name.like("%" + data.get("filter[2]") + "%")
        if not has_filter:
            filter_condition = cond
        else:
            filter_condition = and_(filter_condition, cond)
        has_filter = True

    if data.get("filter[3]"): #Dozent
        exams_query = exams_query.join(Professor, Exam.professor)
        cond = func.concat(Professor.firstName, ' ', Professor.lastName).like("%" + data.get("filter[3]") + "%")
        if not has_filter:
            filter_condition = cond
        else:
            filter_condition = and_(filter_condition, cond)
        has_filter = True

    if data.get("filter[4]"): #Semester
        cond = func.concat(Exam.year, ' ', Exam.semester).like("%" + data.get("filter[4]") + "%")
        if not has_filter:
            filter_condition = cond
        else:
            filter_condition = and_(filter_condition, cond)
        has_filter = True
    
    if has_filter:
        exams_query = exams_query.filter(filter_condition)
    
    #sortiertung
    exams_query = sort_exams(exams_query, data)

    #pagination
    page, per_page = pager(data)
    
    ret = {"total_rows": exams_query.count(), "rows": []}

    for doc in to_serializable_dict(Paginator(exams_query, per_page).page(page).object_list):
        ret["rows"].append({
            "Fachbereich": doc["department"]["name"],
            "Fach": doc["course"]["name"],
            "Typ": doc["examType"]["name"],
            "Dozent": doc["professor"]["lastName"] + ", " + doc["professor"]["firstName"],
            "Semester": ("%d " + doc["semester"]) % doc["year"],
            "ID": doc["idExam"]
        })

    return jsonify(ret)

@api.route('/api/getList', methods=['GET'])
def getList():
    data = request.args
    if not data.get("ids"):
        return jsonify({"total_rows": 0, "rows": []})

    filter_condition = None
    has_filter = False
    exams_query = db_session.query(Exam)

    #filterung
    if data.get("filter[0]"): #Fachbereich
        exams_query = exams_query.join(Department, Exam.department)
        if not has_filter:
            filter_condition = Department.name.like("%" + data.get("filter[0]") + "%")
        has_filter = True

    if data.get("filter[1]"): #Fach
        exams_query = exams_query.join(Course, Exam.course)
        cond = Course.name.like("%" + data.get("filter[1]") + "%")
        if not has_filter:
            filter_condition = cond
        else:
            filter_condition = and_(filter_condition, cond)
        has_filter = True

    if data.get("filter[2]"): #Typ
        exams_query = exams_query.join(ExamType, Exam.examType)
        cond = ExamType.name.like("%" + data.get("filter[2]") + "%")
        if not has_filter:
            filter_condition = cond
        else:
            filter_condition = and_(filter_condition, cond)
        has_filter = True

    if data.get("filter[3]"): #Dozent
        exams_query = exams_query.join(Professor, Exam.professor)
        cond = func.concat(Professor.firstName, ' ', Professor.lastName).like("%" + data.get("filter[3]") + "%")
        if not has_filter:
            filter_condition = cond
        else:
            filter_condition = and_(filter_condition, cond)
        has_filter = True

    if data.get("filter[4]"): #Semester
        cond = func.concat(Exam.year, ' ', Exam.semester).like("%" + data.get("filter[4]") + "%")
        if not has_filter:
            filter_condition = cond
        else:
            filter_condition = and_(filter_condition, cond)
        has_filter = True
    
    if has_filter:
        filter_condition = and_(Exam.idExam.in_(json.loads(data.get("ids"))), filter_condition)
    else:
        filter_condition = Exam.idExam.in_(json.loads(data.get("ids")))

    exams_query = exams_query.filter(filter_condition)
    
    #sortiertung
    exams_query = sort_exams(exams_query, data)

    #pagination
    page, per_page = pager(data)
    
    ret = {"total_rows": exams_query.count(), "rows": []}

    for doc in to_serializable_dict(Paginator(exams_query, per_page).page(page).object_list):
        ret["rows"].append({
            "Fachbereich": doc["department"]["name"],
            "Fach": doc["course"]["name"],
            "Typ": doc["examType"]["name"],
            "Dozent": doc["professor"]["lastName"] + ", " + doc["professor"]["firstName"],
            "Semester": ("%d " + doc["semester"]) % doc["year"],
            "ID": doc["idExam"]
        })

    return jsonify(ret)

@api.route('/api/getDoc', methods=['GET'])
def getDoc():
    data = request.args
    if data.get("docID"):
        exam = db_session.query(Exam).filter(Exam.idExam == data.get("docID")).first()
        if exam:
            filePath = os.path.join(app.config['DOCUMENT_PATH'], exam.filePath)
            if os.path.exists(filePath):
                return send_file(filePath)
    
    return "<h2>Error 404: File not Found!</h2>"

def zip_list(docIDs):
    toZip = db_session.query(func.concat(app.config['DOCUMENT_PATH'], Exam.filePath)).filter(Exam.idExam.in_(json.loads(docIDs))).all()
    outputFile = os.path.join(app.config['DOCUMENT_PATH'], 'Zips/', 'filename' + '.zip')
    
    zip_file = zipfile.ZipFile(outputFile, 'w')
    with zip_file:
        for file in toZip:
            zip_file.write(file[0])
    return outputFile

def upload_file(file, filename):
    gauth = GoogleAuth()
    gauth.LocalWebserverAuth()
    drive = GoogleDrive(gauth)
    f = open(file, "r")
    drive_file = drive.CreateFile({'title': filename})
    drive_file.SetContentFile(file)
    drive_file.Upload()
    drive_file.InsertPermission({
        'type': 'anyone',
        'value': 'anyone',
        'role': 'reader'})
    return drive_file['alternateLink']

def send_mail(empfaenger, link):
    FROM = app.config['MAIL_USERNAME']
    TO = empfaenger
    SUBJECT = "Klausuren"
    TEXT = "Deine Klausuren findest du unter folgendem Link: %s" % link
    message = """From: %s\nTo: %s\nSubject: %s\n\n%s""" % (FROM, ", ".join(TO), SUBJECT, TEXT)
    s = smtplib.SMTP(app.config['MAIL_SERVER'], app.config['MAIL_PORT'])
    s.ehlo()
    s.starttls()
    s.login(app.config['MAIL_USERNAME'], app.config['MAIL_PASSWORD'])
    s.sendmail(app.config['MAIL_USERNAME'], empfaenger, message)
    s.quit()

@api.route('/api/dlList', methods=['POST'])
def dlList():
    data = request.form
    if data.get("docIDs"):
        zip_file = zip_list(data.get("docIDs"))
        filename = os.path.basename(zip_file)
        path = os.path.abspath(zip_file)[0:0 - len(filename)]
        return send_from_directory(path,
                                   filename,
                                   mimetype="application/zip,application/octet-stream,application/x-zip-compressed,multipart/x-zip",
                                   as_attachment=True)
    return ""

@api.route('/api/sendList', methods=['POST'])
def sendList():
    data = request.form
    if data.get("docIDs") and data.get("empf"):
        zip_file = zip_list(data.get("docIDs"))
        filename = os.path.basename(zip_file)
        path = os.path.abspath(zip_file)[0:0 - len(filename)]

        url = upload_file(zip_file, filename)

        send_mail(data.get("empf"), url)

        return "Done"
    return "Fail"


