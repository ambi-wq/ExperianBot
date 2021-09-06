### multi language,ticket creation,chat history,notification
from __future__ import print_function
from flask import Flask, request, redirect,render_template,url_for
import json
import flask
from langdetect import detect
from chatterbot import ChatBot
from chatterbot.trainers import ChatterBotCorpusTrainer
import ssl
from model.MySQLHelpertemp import insertquery, create_query
from flask_cors import CORS
from nltk.tokenize import word_tokenize
from autocorrect import spell
import itertools
from dateutil import parser
xrange=range
#from nltk.stem.wordnet import WordNetLemmatizer
from fuzzywuzzy import fuzz
from model.AES_Encryption import encrypt, decrypt
from flask_mail import Mail, Message
import re
import logging
import logging.handlers
from logging.handlers import TimedRotatingFileHandler
import traceback
from translate import Translator, translate
from datetime import datetime, timedelta
from pyfcm import FCMNotification
import os.path
import pickle
from datetime import  timezone
import datefinder
from google.auth.transport.requests import Request
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
import schedule
# from google.cloud import translate_v2 as translate
from random import randint
import requests
from dateparser.search import search_dates
#import schedule

# try:
#     _create_unverified_https_context = ssl._create_unverified_context
# except AttributeError:
#     pass
# else:
#     ssl._create_default_https_context = _create_unverified_https_context


logger = logging.getLogger("Rotating Log")
logger.setLevel(logging.INFO)
handler = TimedRotatingFileHandler('log//bot.log', when='midnight', interval=1, backupCount=10)
# create console handler and set leve to debug
handler = logging.FileHandler('log//bot.log'.format(datetime.now()))
# create formatter
formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
handler.setFormatter(formatter)
logger.addHandler(handler)

BasePathAttachment = " http://127.0.0.1:8000/static/notifications_attachments/"
BasePathDocumnets = " http://127.0.0.1:8000/static/document_files/"

video_path_BaseURL="https://mgenius.in/mobitrail/DemoBot/Video"
# image_path_BAseURL="http://mgenius.in/IIFLBotHtml/iiflimages/"
image_path_BAseURL = "https://askpanda.iifl.in/ServiceBot/iiflimages/"
scopes = ['https://www.googleapis.com/auth/calendar']
app = Flask(__name__)
CORS(app)
app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 465
app.config['MAIL_USERNAME'] = 'mobitrail.technology@gmail.com'
app.config['MAIL_PASSWORD'] = 'mobitrail@1234'
app.config['MAIL_USE_TLS'] = False
app.config['MAIL_USE_SSL'] = True
mail = Mail(app)


UPLOAD_FOLDER = 'temp'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

garbage_list = ["im", "kindly", "Actually", "dear", "are", "employee", "about", "above", "across", "after",
                "afterwards", "help", "Dear","i am","I am","pm","am",
                "asap", "solve", "again", "against", "all", "almost", "alone", "along", "already", "also", "although",
                "always","p","a",
                "among", "amongst", "amoungst", "amount", "an ", "and", "another", "any", "anyhow", "anyone",
                "anything",
                "anyway", "anywhere", "are", "around", "as", "at", "back", "be", "became", "because", "become",
                "becomes", "becoming", "been", "before", "beforehand", "behind", "being", "below", "beside", "besides",
                "between", "beyond", "both", "bottom", "but", "by", "call", "can", "co",
                "con", "could", "cry", "de", "describe", "detail", "do", "did", "does", "done", "down",
                "due", "during", "each", "eg", "eight", "either", "eleven", "else", "elsewhere", "empty", "enough",
                "etc", "even", "ever", "every", "everyone", "everything", "everywhere", "except", "few", "fifteen",
                "fify", "fill", "fire", "first", "five", "for", "former", "formerly", "forty", "found", "four",
                "from", "front", "full", "further", "get", "give", "go", "had", "has", "having", "have", "he",
                "hence", "her", "here", "hereafter", "hereby", "herein", "hereupon", "hers", "herself", "him",
                "himself", "his", "however", "hundred", "ie", "if", "in", "inc", "indeed", "interest", "into",
                "is", "it", "its", "itself", "keep", "last", "latter", "latterly", "least", "less", "ltd", "made",
                "many", "may", "me", "meanwhile", "might", "mill", "mine", "more", "moreover", "most", "mostly", "move",
                "much", "must", "my", "myself", "namely", "neither", "never", "nevertheless", "next", "nine",
                "no", "nobody", "none", "noone", "nor", "nothing", "now", "nowhere", "of", "often", "on",
                "once", "one", "only", "onto", "or", "other", "others", "otherwise", "our", "ours", "ourselves", "out",
                "over", "own", "part", "per", "perhaps", "please", "put", "rather", "re", "same", "see", "seem",
                "seemed", "seeming", "seems", "serious", "several", "she", "should", "side", "since", "sincere",
                "six", "sixty", "so", "some", "somehow", "someone", "something", "sometime", "sometimes", "somewhere",
                "still", "such", "ten", "than", "that", "the", "their", "them", "themselves", "then",
                "thence", "there", "thereafter", "thereby", "therefore", "therein", "thereupon", "these", "they",
                "thickv", "thin", "third", "this", "those", "though", "three", "through", "throughout", "thru", "thus",
                "to", "together", "too", "top", "toward", "towards", "twelve", "twenty", "two", "un", "under", "until",
                "up", "upon", "us", "very", "via", "was", "we", "well", "were", "what", "whatever", "when", "whence",
                "whenever", "where", "whereafter", "whereas", "whereby", "wherein", "whereupon", "wherever", "whether",
                "which", "while", "whither", "who", "whoever", "whole", "whom", "whose", "why", "will", "with",
                "within", "without", "would", "yet", "you", "your", "yours", "yourself", "yourselves", "the", "facing",
                "Assist", "resolve", "Resolve", "resolv", "resolved", "pls", "please", "resolution", "looking", "look",
                "solution", "issue", "issues", "issu", "isue", "problem", "problm", "prblm", "assist", "asist", "assit",
                "Problem", "Issue", "Issues", "Problems", "problems", "u", "U", "resolving", "working", "work", "hey",
                "error", "eror", "unable", "properly", "proper", "properer", "plss", "want", "let", "Tell", "tell","know","pus","mal"]

stopwordsss = ['i', 'me', 'my', 'myself', 'we', 'our', 'ours', 'ourselves', 'you', "you're", "you've", "you'll", "u",
               "you'd",
               'your', 'yours', 'yourself', 'yourselves', 'he', 'him', 'his', 'himself', 'she', "she's", 'her', 'hers',
               'herself',
               'it', "it's", 'its', 'itself', 'they', 'them', 'their', 'theirs', 'themselves', 'what', 'which', 'who',
               'whom',
               'this', 'that', "that'll", 'these', 'those', 'am', 'is', 'are', 'was', 'were', 'be', 'been', 'being',
               'have', 'has',
               'had', 'having', 'do', 'does', 'did', 'doing', 'an', 'the', 'and', 'but', 'if', 'or', 'because', 'as',
               'until',
               'while', 'of', 'at', 'by', 'for', 'with', 'about', 'against', 'between', 'into', 'through', 'during',
               'before',
               'after', 'above', 'below', 'to', 'from', 'up', 'down', 'in', 'out', 'on', 'over', 'under',
               'again',
               'further', 'then', 'once', 'here', 'there', 'when', 'where', 'why', 'how', 'all', 'any', 'both', 'each',
               'few',
               'more', 'most', 'other', 'some', 'such', 'no', 'nor', 'not', 'only', 'own', 'same', 'so', 'than', 'too',
               'very',
               's', 't', 'can', 'will', 'just', 'don', "don't", 'should', "should've", 'now', 'd', 'll', 'm', 'o', 're',
               've', 'y',
               'ain', 'aren', "aren't", 'couldn', "couldn't", 'didn', "didn't", 'doesn', "doesn't", 'hadn', "hadn't",
               'hasn',
               "hasn't", 'haven', "haven't", 'isn', "isn't", 'ma', 'mightn', "mightn't", 'mustn', "mustn't", 'needn',
               "needn't",
               'shan', "shan't", 'shouldn', "shouldn't", 'wasn', "wasn't", 'weren', "weren't", 'won', "won't", 'wouldn',
               "wouldn't"]

stop_words = set(garbage_list)
stop_words.update(stopwordsss)

text_ext = ['textFile', 'doc', 'docx', 'docm', 'odt', 'pdf', 'txt', 'rtf', 'pages', 'pfb', 'mobi', 'chm', 'tex', 'bib', 'dvi', 'abw', 'text', 'epub', 'nfo', 'log', 'log1', 'log2', 'wks', 'wps', 'wpd', 'emlx', 'utf8', 'ichat', 'asc', 'ott', 'fra', 'opf']
image_ext = ['imageFile', 'img','jpg', 'jpeg', 'png', 'png0', 'ai', 'cr2', 'ico', 'icon', 'jfif', 'tiff', 'tif', 'gif', 'bmp', 'odg', 'djvu', 'odg', 'ai', 'fla', 'pic', 'ps', 'psb', 'svg', 'dds', 'hdr', 'ithmb', 'rds', 'heic', 'aae', 'apalbum', 'apfolder', 'xmp', 'dng', 'px', 'catalog', 'ita', 'photoscachefile', 'visual', 'shape', 'appicon', 'icns']
spreadsheet_ext = ['spreadsheetFile', 'csv', 'odf', 'ods', 'xlr', 'xls', 'xlsx', 'numbers', 'xlk']
archive_ext = ['archiveFile', 'zip', 'gz', 'rar', 'cab', 'iso', 'tar', 'lzma', 'bz2', 'pkg', 'xz', '7z', 'vdi', 'ova', 'rpm', 'z', 'tgz', 'deb', 'vcd', 'ost', 'vmdk', '001', '002', '003', '004', '005', '006', '007', '008', '009', 'arj', 'package', 'ims']
audio_ext = ['audioFile', 'mp3', 'm3u', 'm4a', 'wav', 'ogg', 'flac', 'midi', 'oct', 'aac', 'aiff', 'aif', 'wma', 'pcm', 'cda', 'mid', 'mpa', 'ens', 'adg', 'dmpatch', 'sngw', 'seq', 'wem', 'mtp', 'l6t', 'lng', 'adx', 'link']
presentation_ext = ['presentationFile', 'ppt', 'pptx', 'pps', 'ppsx', 'odp', 'key']
video_ext = ['videoFile', 'mpg', 'mpeg', 'avi', 'mp4', 'flv', 'h264', 'mov', 'mk4', 'swf', 'wmv', 'mkv', 'plist', 'm4v', 'trec', '3g2', '3gp', 'rm', 'vob']
allcats = [text_ext,image_ext,spreadsheet_ext,archive_ext,audio_ext,presentation_ext,video_ext]


def categorize(extension):
	for category in allcats:
		if extension in category:
			entry = category[category.index(extension)]
			if ((entry in extension) and (extension in entry)):
				return category[0]
	else:
		#print('    dont know how to bin:  ' + extension)
		return "file"

#lem = WordNetLemmatizer()
#english_bot = ChatBot("Chatterbot", storage_adapter="chatterbot.storage.SQLStorageAdapter")
english_bot = ChatBot("Chatterbot", storage_adapter="chatterbot.storage.MongoDatabaseAdapter",database="chatterbot-MobitrailBot")
english_bot.set_trainer(ChatterBotCorpusTrainer)
english_bot.train("chatterbot.corpus.ExperianBot")


list11 = ["today","tomorrows","tomorrow","weekly","week","weekly","monthly","month","all"]
# function for date format
def chFormat(rem_date):
    wdate = rem_date.split("-")
    new_Date = wdate[2] + "-" + wdate[1] + "-" + wdate[0]
    return new_Date

# function to check month
def monthchk(text):
    month = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"];
    for a in text.split(" "):
        print(a)
        res = [i for i in month if i.lower() in a.lower()]
        print(res)
    if len(res)>0:
        return True
    else:
        return False

def PushReminders(token, title, description):

        print("push notify")
        push_service = FCMNotification(api_key="AIzaSyCHHic6EYsAoQ7wiDehDz8IOjW7C2hiaUQ")

        message_title = title
        message_body = description

        if isinstance(token, list):
            print("====",token)
            registration_ids = token
            print("inside if")
            result = push_service.notify_multiple_devices(registration_ids=registration_ids,
                                                          message_title=message_title,
                                                          message_body=message_body)

        else:
            print("inside else")
            print("====", token)
            registration_id = token
            result = push_service.notify_single_device(registration_id=registration_id, message_title=message_title,
                                                       message_body=message_body)
        print("result==",result)

def daily_notify():
    currentdate = datetime.now().strftime("%Y-%m-%d")
    query = "SELECT notify_list.user_token, notify_list.userID," \
            " reminder_detail.emp_name,reminder_detail.rem_type,reminder_detail.rem_desc," \
            " reminder_detail.time FROM notify_list INNER JOIN reminder_detail" \
            " ON notify_list.userID=reminder_detail.emp_id where reminder_detail.date = '" + currentdate + "'"
    #print(query)
    output = create_query(query)
    #print(output)

    tag_list = list(output)
    print('def notify taglist== ',tag_list)
    for entry in tag_list:
        token = entry[0]
        user_id = entry[1]
        user_name = entry[2]
        type = entry[3]
        desc = entry[4]
        time = entry[5]
        title = type + " at " + time
        PushReminders(token, title, desc)
        #print(time)

def remind_notify():
    currentdate = datetime.now().strftime("%Y-%m-%d")

    query = "SELECT notify_list.user_token, notify_list.userID," \
            " reminder_detail.emp_name,reminder_detail.rem_type,reminder_detail.rem_desc," \
            " reminder_detail.time FROM notify_list INNER JOIN reminder_detail" \
            " ON notify_list.userID=reminder_detail.emp_id where reminder_detail.date = '" + currentdate + "'"
    #print(query)
    output = create_query(query)
    #print(output)
    now = datetime.now()
    a = now.strftime("%H:%M")
    current_time = datetime.strptime(a, "%H:%M")

    tag_list = list(output)
    print('remind taglist== ',tag_list)
    for entry in tag_list:
        token = entry[0]
        user_id = entry[1]
        user_name = entry[2]
        type = entry[3]
        desc = entry[4]
        time = entry[5]
        title = type + " at " + time
        # PushReminders(token,title,desc)
        #print(time)
        if "PM" in time and "12" not in time:
            temp = time.split(":")
            t = int(temp[0]) + 12
            time = str(t) + ":" + str(temp[1])
        stime = time[:-3]
        d1 = datetime.strptime(stime, "%H:%M")
        # d2 = datetime.strptime("00:15", "%H:%M")
        # print("15 min")
        temp = (d1 - current_time)
        # print(temp)
        # print(temp.total_seconds())
        if temp.total_seconds() <= 900 and temp.total_seconds() >= 0:
            #print(desc)
            PushReminders(token, title, desc)

@app.route("/showNotifications", methods=["POST", "GET"])
def Notifications():
    if request.method == "POST":

        details = request.form
        title = details['title1']
        description = details['desc1']
        sender = details['sender']

        query = "select user_token from notify_list where group_id = 1"
        output = create_query(query)
        tag_list = list(output)
        notify_list_ids = []
        for t in tag_list:
            notify_list_ids.append(t[0])
        print("notify_list_ids----------> ",notify_list_ids)
        push_service = FCMNotification(api_key="AIzaSyCHHic6EYsAoQ7wiDehDz8IOjW7C2hiaUQ")


        # Send to multiple devices by passing a list of ids.
        registration_ids = notify_list_ids
        message_title = title
        message_body = description
        result = push_service.notify_multiple_devices(registration_ids=registration_ids, message_title=message_title,
                                                      message_body=message_body)

        print(result)
        currentdate = datetime.now().strftime("%Y-%m-%d")
        leave_query = "INSERT INTO `notify`( `Title`, `Description`, `Sender`, `date`) " \
                      "VALUES ('" + str(title) + "','" + str(description) + "','" + str(sender) + "','" + currentdate + "')"
        lev = insertquery(leave_query)

        return render_template('index1.html')
    return render_template('index.html')


#--------------- reminder api
# api for todays reminder that should be display first after login

@app.route("/showSurveyData",methods=["POST","GET"])
def show_survey_data():
    if request.method == "POST":
        survey_title = request.form['surveytitle']
        print(survey_title)

        query = "select survey_id from survey where title = '" + survey_title + "'"
        output = create_query(query)
        survey_id = output[0][0]
        print("survey id ========= ", survey_id)

        sr_query = "select Distinct emp_id,emp_name,cast(submitted_date as date),survey_id from survey_submit_details" \
                   " where survey_id = '" + str(survey_id) + "' order by emp_id"
        print("########",sr_query)
        output1 = create_query(sr_query)
        details = list(output1)
        print(details)
        if len(details)>0:
            message = "Here Are Details of " + survey_title + " Survey"
        else:
            message = "No Details Found"

        return render_template('survey_details.html', message=message, details=details)
    return render_template('survey_details.html')


@app.route("/showSurveyAnswers",methods=["POST","GET"])
def show_survey_ans():
    message1 = request.get_data()
    #message = decrypt(message1)
    objectreceived = json.loads(message1)
    userID = objectreceived.get('userID')
    surveyID = objectreceived.get('surveyID')

    ans_query = "select survey_submit_details.emp_id,survey_submit_details.question_id,survey_submit_details.answer,survey_details.question " \
               "from survey_submit_details INNER JOIN survey_details ON survey_submit_details.question_id = survey_details.question_id " \
               "where survey_submit_details.survey_id = '" + str(surveyID) + "' and survey_submit_details.emp_id = '" + str(userID) + "'"
    print(ans_query)
    ans_list = create_query(ans_query)
    ans_tags = list(ans_list)
    return render_template('survey_details_ans.html',ans_tags=ans_tags)


@app.route("/todaysReminder",methods=["POST","GET"])
def show():
    message1 = request.get_data()
    message = decrypt(message1)
    objectreceived = json.loads(message)
    print("today rem==",objectreceived)
    userID = objectreceived.get('userID')
    language = objectreceived.get('language')
    language_flag = False
    print("language++++++", language)
    if language == "gu" or language == "hi" or language == "ml" or language == "mr" or language == "ta" or language == "te" or language == "ur" or language == "pa":
        language_flag = True
    else:
        language_flag = False
    print(language_flag)
    currentdate = datetime.now().strftime("%Y-%m-%d")
    query = "select * from reminder_detail where date = '" + currentdate + "' and emp_id = '" + userID + "' order by time"
    output = create_query(query)
    print(output)

    tag_list = list(output)
    print(tag_list)
    remindertoday = "Here are the details of your Reminders for Today"
    if language_flag:
        remindertoday = gettext(remindertoday, language)
    noremindertoday = "No Reminders for today."
    if language_flag:
        noremindertoday = gettext(noremindertoday, language)
    json_array = []
    if len(tag_list)>0:
        for t in tag_list:
            sim1 = {
                "Rem_desc": t[4],
                "Rem_title": t[3], "buttontext": "",
                "imagepath": "",
                "Rem_type": t[3],
                "Rem_date": chFormat(str(t[5])),
                "Rem_time": t[6],
                "status": "",
                "Rem_set_date": t[9],
                "no_of_days": "",
                "name": t[2],
                "redirectlink": "", "topright": "", "bottomtight": "",
                "action": "", "message": "",
                "ParameterTitle": ""}

            json_array.append(sim1)

        json_data = {
            "message": remindertoday,
            "ParameterTitle": "CarausialView",
            "ParameterType": "ReminderView",
            "action": json_array
        }
    else:
        json_data = {
            "message":noremindertoday,
            "ParameterTitle": "CarausialView",
            "ParameterType": "ReminderView",
            "action": json_array
        }
    data1 = json.dumps(json_data, sort_keys=True, indent=4 * ' ')
    data = data1
    data2 = json.dumps(json_data, ensure_ascii=False)
    print(data)
    resp = flask.Response(encrypt(data))
    return resp

def show_todays_reminder():
    message1 = request.get_data()
    message = decrypt(message1)
    objectreceived = json.loads(message)
    print("today rem==",objectreceived)
    userID = objectreceived.get('userID')

    currentdate = datetime.now().strftime("%Y-%m-%d")
    query = "select * from reminder_detail where date = '" + currentdate + "' and emp_id = '" + userID + "' order by time"
    output = create_query(query)
    print(output)

    tag_list = list(output)
    print(tag_list)
    return tag_list

#for google calender
def create_event(start_time_str, summary, duration,attendees, description, location):
        print("in create event")
        creds = None
        # The file token.pickle stores the user's access and refresh tokens, and is
        # created automatically when the authorization flow completes for the first
        # time.
        if os.path.exists('token.pickle'):
            with open('token.pickle', 'rb') as token:
                creds = pickle.load(token)
        # If there are no (valid) credentials available, let the user log in.
        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                creds.refresh(Request())
            else:

                #flow = InstalledAppFlow.from_client_secrets_file("Credentials/client_secret.json", scopes=scopes)
                flow = InstalledAppFlow.from_client_secrets_file("Credentials/client_secret.json", scopes=scopes)

                creds = flow.run_local_server(port=0)
            # Save the credentials for the next run
            with open('token.pickle', 'wb') as token:
                pickle.dump(creds, token)

        service = build('calendar', 'v3', credentials=creds)

        matches = list(datefinder.find_dates(start_time_str))
        print("match====",matches)
        if len(matches):
            start_time = matches[0]
            #print("===", start_time)

            if start_time.day <= 12:
                st_time = start_time.strftime("%Y-%d-%mT%H:%M:%S")
                end_time = (start_time + timedelta(hours=duration)).strftime("%Y-%d-%mT%H:%M:%S")
                print("2 st====", st_time)
                print("end", end_time)
            else:
                st_time = start_time.strftime("%Y-%m-%dT%H:%M:%S")
                end_time = (start_time + timedelta(hours=duration)).strftime("%Y-%m-%dT%H:%M:%S")
                print("2 st====", st_time)
                print("end", end_time)


        event = {
                'summary': summary,
                'location': location,
                'description': description,
                'start': {
                    'dateTime': st_time,
                    'timeZone': "UTC +5:30",
                },
                'end': {
                    'dateTime': end_time,
                    'timeZone': "UTC +5:30",
                },
                'attendees': [
                    {'email': attendees},
                ],
                'reminders': {
                    'useDefault': False,
                    'overrides': [
                        {'method': 'email', 'minutes': 24 * 60},
                        {'method': 'popup', 'minutes': 10},
                    ],
                },
            }
        print(event)
        # event = json.dumps(event)
        # print(event)
        event = service.events().insert(calendarId='primary',body=event).execute()
        print("event==",event)
        print(f"The event has been created! View it at {event.get('htmlLink')}!")

@app.route("/setReminder",methods=["POST","GET"])
def set_reminder_def():
    try:
        message1 = request.get_data()
        message = decrypt(message1)
        objectreceived = json.loads(message)
        print("reminder obj==",objectreceived)
        platform = objectreceived.get('platform')
        userID = objectreceived.get('userID')
        userName = objectreceived.get('userName')
        rem_type = objectreceived.get('rem_type')
        rem_desc = objectreceived.get('rem_desc')
        rem_date = objectreceived.get('rem_date')
        rem_time = objectreceived.get('rem_time ')
        remGoogleFlag = objectreceived.get('remGoogleFlag')
        remOutlookFlag = objectreceived.get('remOutlookFlag')
        language = objectreceived.get('language')
        language_flag = False
        print("language++++++", language)
        if language == "gu" or language == "hi" or language == "ml" or language == "mr" or language == "ta" or language == "te" or language == "ur" or language == "pa":
            language_flag = True
        else:
            # language= detect_lang(usertext)
            language_flag = False
        location = ""
        message = "Please help me with the below mentioned details for your Reminder.##Remform##"
        if language_flag:
            message = gettext(message,language)
        messagesucc = "Your reminder has been set successfully."
        if language_flag:
            messagesucc = gettext(messagesucc, language)
        currenttime = datetime.now().strftime("%Y-%m-%d %H:%M:%S")


        print("-----",rem_date)
        wdate = rem_date.split("-")
        new_Date = wdate[2] + "-" + wdate[1] + "-" + wdate[0]
        print("new date===",new_Date)


        if remGoogleFlag == "true" or remGoogleFlag == 'True':
            email_query = "select `email` from mastertable where userID = '" + str(userID) + "'"
            output = create_query(email_query)
            email = output[0][0]
            print("email==", email)
            print("---google")
            date_str = rem_date + " " + rem_time
            print(date_str)
            create_event(date_str,rem_type,1,email,rem_desc,location)
            print("event created")
        else:
            print("out of if")
        a = insertreminder(userID,userName,rem_type,rem_desc,new_Date,rem_time,remGoogleFlag,remOutlookFlag)

        his_data = "select reminder_detail.rem_type,reminder_detail.rem_desc,reminder_detail.date,reminder_detail.time," \
                   "reminder_detail.googleFlag,reminder_detail.outlookFlag,reminder_detail.insert_time, " \
                   "chat_history.asked_on,chat_history.query,chat_history.flag from reminder_detail INNER JOIN chat_history " \
                   "ON reminder_detail.emp_id = chat_history.userID where reminder_detail.insert_time > chat_history.asked_on " \
                   "order by chat_history.id desc limit 1"

        output = create_query(his_data)
        tags_list = list(output)
        json_array = []

        if len(tags_list) > 0:
            for data in tags_list:
                sim = {
                    "rem_type": data[0],
                    "rem_desc": data[1],
                    "date": str(data[2]),
                    "time": data[3],
                    "googleFlag" : data[4],
                    "outlookFlag" : data[5],
                    #"query": data[8],
                    #"flag" : data[9],
                    "message":message,
                    "response":message,

                }
                json_array.append(sim)
            json_data = {"message": message,
                "ParameterTitle": "",
                "ParameterType": "",
                "action": json_array}
            data1 = json.dumps(json_data, sort_keys=True, indent=4 * ' ')
            data = data1
            data2 = json.dumps(json_data, ensure_ascii=False)
            print("json data ==> ", data)
            formdata = "UPDATE chat_history SET query = '" + data2 + "' where asked_on < '" + currenttime + "' order by id desc limit 1"
            query = insertquery(formdata)
            print(query)


        if a == "somthing went wrong":
            json_data = {
                "error": "something went wrong",

                "response": "something went wrong",
            }
        else:
            json_data = {
                "error": messagesucc,

                "response": messagesucc,
            }
        data1 = json.dumps(json_data, sort_keys=True, indent=4 * ' ')
        data = data1
        data2 = json.dumps(json_data, ensure_ascii=False)
        print("json data = ", data)
        # dbInsertion(temtext, data2, "answered", username, userID, "-1", mainIssue, "--", "-1")
        resp = flask.Response(encrypt(data))
        #resp = flask.Response(data)
       #logger.info(f'{userID} [get] Response:' + str(json_data))
        return resp

    except:
        json_data = {
            "error": "something went wrong",
            "response": "something went wrong",
        }
        data = json.dumps(json_data)
        print("json data = ", data)
        resp = flask.Response(encrypt(data))
        #resp = flask.Response(data)
       #logger.info(f'{userID} [get] Response:' + str(json_data))
        return resp

def insertreminder(userID,userName,rem_type,rem_desc,rem_date,rem_time,remGoogleFlag,remOutlookFlag):
    try:
        currenttime = datetime.now().strftime("%d-%m-%Y")
        
        reminder_query = "INSERT INTO `reminder_detail`(`emp_id`,`emp_name`,`rem_type`,`rem_desc`,`date`,`time`,`googleFlag`,`outlookFlag`,`rem_set_on`)" \
                         " VALUES ('" + str(userID) + "','" + str(userName) + "','" + str(rem_type) + "','" + str(rem_desc) + "','" + str(rem_date) + "','" + str(rem_time) + "','" + str(remGoogleFlag) + "','" + str(remOutlookFlag) + "','" + str(currenttime) + "')"
        print("reminder query==",reminder_query)
        rem = insertquery(reminder_query) 
        print(rem)

    except Exception as e:
        logger.error(f'{userID} [insertLeave] Exception occurred', exc_info=True)

        print("Exception occured ", e)
        traceback.print_exc()
        return "somthing went wrong"

# ------------------------leave api
@app.route("/applyleave", methods=["POST", "GET"])
def applyleavedef():
    try:

        message1 = request.get_data()
        message = decrypt(message1)

        objectrecived = json.loads(message)
        print("leave obj==",objectrecived)
        platform = objectrecived.get('platform')
        userID = objectrecived.get('userID')
        userName = objectrecived.get('userName')
        type = objectrecived.get('type')
        from_date = objectrecived.get('from_date')
        to_date = objectrecived.get('to_date')
        days = objectrecived.get('days')
        status = "Pending"
        approver_id = 1001
        approver_name = "Vikas Kedia"
        language = objectrecived.get('language')
        language_flag = False
        print("language++++++", language)
        if language == "gu" or language == "hi" or language == "ml" or language == "mr" or language == "ta" or language == "te" or language == "ur" or language == "pa":
            language_flag = True
        else:
            # language= detect_lang(usertext)
            language_flag = False
        mes = "Your leave has been applied successfully. It has been forwarded to your Superior Mr. VIkas Kedia for approval."
        if language_flag:
            mes = gettext(mes,language)
        currenttime = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        if type:
            print(type)
        else:
            type = "Personal Leave"
        a = insertLeave(userID, type, from_date, to_date, days , status, approver_id, approver_name,userName)
        send_email_attendance(userName,type,from_date,to_date,days,approver_name)
        print("history---")
        his_data = "SELECT leave_detail.emp_id,leave_detail.type,leave_detail.from_date,leave_detail.to_date," \
                   "leave_detail.insert_time,chat_history.asked_on,chat_history.query,chat_history.flag " \
                   "FROM leave_detail INNER JOIN chat_history ON leave_detail.emp_id = chat_history.userID " \
                   "WHERE leave_detail.insert_time > chat_history.asked_on order by chat_history.id desc limit 1"
        output = create_query(his_data)
        tags_list = list(output)
        json_array = []

        if len(tags_list) > 0:
            for data in tags_list:
                sim = {
                     "emp_id": data[0],
                     "leave_type": data[1],
                     "from_date": str(data[2]),
                     "to_date": str(data[3]),
                     "message": "Apply for Leave.##form##",
                     "response": "Apply for Leave.##form##",

                }
                json_array.append(sim)
            json_data = {"message": "Apply for Leave.##form##",
                         "ParameterTitle": "",
                         "ParameterType": "",
                         "action": json_array}
            data1 = json.dumps(json_data, sort_keys=True, indent=4 * ' ')
            data = data1
            data2 = json.dumps(json_data, ensure_ascii=False)
            print("json data ==> ", data)
            leaveform = "UPDATE chat_history SET query = '" + data2 + "' where asked_on < '" + currenttime + "' order by id desc limit 1"

            query = insertquery(leaveform)
            #insertHistory(currenttime, data2, "response", userName, userID)

        if a == "somthing went wrong":
            json_data = {
                "error": "somthing went wrong",

                "response": "somthing went wrong",
            }
        else:
            json_data = {
                "error": mes,

                "response": mes,
            }
        data1 = json.dumps(json_data, sort_keys=True, indent=4 * ' ')
        data = data1
        print("json data = ", data)
        resp = flask.Response(encrypt(data))
        #resp = flask.Response(data)
       #logger.info(f'{userID} [get] Response:' + str(json_data))
        return resp
    except:
        json_data = {
            "error": "somthing went wrong",
            "response": "somthing went wrong",
        }
        data = json.dumps(json_data)
        print("json data = ", data)
        resp = flask.Response(encrypt(data))
        #resp = flask.Response(data)
       #logger.info(f'{userID} [get] Response:' + str(json_data))
        return resp

def send_email_attendance(userName,type,from_date,to_date,days,approver_name):
     try:
        userMail= "mobitrail.technology @ gmail.com"
        msg = Message(subject="Leave Request from "+str(userName), sender=userMail,
                      recipients=['vedanti@mobitrail.com'])
        if days==1 or days =="1":
            msg.body = "Dear "+approver_name+", \n\n" \
                           "User {0} have applied for {1} on {2} \n" \
                           "Number of days: {3}. \n\n" \
                           "Request you to please check and respond for same from following link:. \n" \
                           "http://192.168.0.84:8383/ServiceBot25_02_2020/chat.html?userName=Vikas&userId=1001 \n\n" \
                           "Regards \n\n" \
                           "SuperE \n" \
                           "(Fullerton India Service Bot)".format(userName, type, from_date, days)
        else:
            msg.body = "Dear " + approver_name + ", \n\n" \
                                                 "User {0} have applied for {1} from {2} to {3} \n" \
                                                 "Number of days: {4}. \n\n" \
                                                 "Request you to please check and respond for same from following link:. \n" \
                                                 "http://192.168.0.84:8383/ServiceBot25_02_2020/chat.html?userName=Vikas&userId=1001 \n\n" \
                                                 "Regards \n\n" \
                                                 "SuperE \n" \
                                                 "(Fullerton India Service Bot)".format(userName, type, from_date, to_date, days)
        mail.send(msg)
        return "Email sent successfully"
     except:
        return "Email not sent"

def insertLeave(userID,type,from_date,to_date,days,status,approver_id,approver_name,userName):
    try:
        currenttime = datetime.now().strftime("%Y-%m-%d")


        leave_query = "INSERT INTO `leave_detail`(`emp_id`, `type`, `from_date`, `to_date`, `days`, `applied_on`, `status`, `approver_id`, `approver_name`,`emp_name`) " \
                           "VALUES ('"+str(userID)+"','"+str(type)+"','"+str(from_date)+"','"+str(to_date)+"',"+str(days)+",'"+str(currenttime)+"','"+str(status)+"','"+str(approver_id)+"','"+str(approver_name)+"','"+str(userName)+"')"

        print(leave_query)
        lev = insertquery(leave_query)
        print(lev)

        title = "Leave request from " + userName
        description = "From:" + from_date + "  To:" + to_date + "\n" \
                                                                   "as " + type + " for " + str(days) + " days."
        noti = "select user_token from notify_list where userID = " + str(approver_id)
        output = create_query(noti)

        tag_list = list(output)
        print(tag_list)

        list1 = []
        for entry in tag_list:
            token = entry[0]
            print(token)
            list1.append(token)
        print("----",list1)
        PushReminders(list1, title, description)

    except Exception as e:
        logger.error(f'{userID} [insertLeave] Exception occurred', exc_info=True)

        print("Exception occured ", e)
        traceback.print_exc()
        return "somthing went wrong"

@app.route("/updateleave", methods=["POST", "GET"])
def updateleavedef():
    try:
        message1 = request.get_data()
        message = decrypt(message1)

        objectrecived = json.loads(message)
        print("update leave obj==",objectrecived)
        platform = objectrecived.get('platform')
        userID = objectrecived.get('userID')
        userName = objectrecived.get('userName')
        leave_id = objectrecived.get('leave_id')
        status = objectrecived.get('status')
        approver_id = 1001
        approver_name = "Vikas Kedia"
        updateLeave(userID, status, leave_id)
        json_data = {
            "error": "Leave Responded Successfully",
            "response": "Leave Responded Successfully",
        }

        data = json.dumps(json_data)
        print("json data = ", data)
        resp = flask.Response(encrypt(data))
       #logger.info(f'{userID} [get] Response:' + str(json_data))
        return resp
    except:
        print("exception")

def updateLeave(userID,status,leave_id):
    try:
        leave_query = "UPDATE `leave_detail` SET `status`='"+str(status)+"' WHERE leave_id='"+str(leave_id)+"'"
        lev = insertquery(leave_query)
        print(lev)

        query = "SELECT leave_detail.emp_name,leave_detail.status,leave_detail.from_date,leave_detail.to_date,leave_detail.approver_name,leave_detail.type," \
                "notify_list.user_token FROM `leave_detail` INNER JOIN `notify_list`" \
                "ON leave_detail.emp_id = notify_list.userID where leave_detail.leave_id= '" + str(leave_id) + "'"


        output = create_query(query)
        lists = list(output)
        print("status==", lists)

        for ls in lists:
            title = "Leave status"
            leave = ""
            if "pprov" in ls[1]:
                leave = "Approved"
            else:
                leave = "Rejected"
            description = "Your " + ls[5] + " From " + ls[2] + " To " + ls[3] + " has been " + leave + " by " + ls[4] +"."
            token = ls[6]
            PushReminders(token, title, description)

        print(description)



    except Exception as e:
        logger.error(f'{userID} [updateLeave] Exception occurred', exc_info=True)

        print("Exception occured ", e)
        traceback.print_exc()

def chkFlags(meetingFlag,callFlag):
    if meetingFlag:
        type = "meeting"
    elif callFlag:
        type = "call"
    else:
        type = ""
    return type

def insertHistory(time,query,flag,username,userID):
    query = "insert into chat_history(asked_on,query,flag,username,userID)" \
            "values('" + str(time) + "','" + str(query) + "','" + flag + "','" + username + "','" + userID + "')"
    print("add==",insertquery(query))

@app.route('/chatHistory',methods=["POST","GET"])
def get_chat_history():
    message1 = request.get_data()
    message = decrypt(message1)
    objectreceived = json.loads(message)
    print("history==", objectreceived)
    userID = objectreceived.get('userID')

    date = datetime.now()
    currentdate = date.strftime("%Y-%m-%d")
    predate = (date -  timedelta(days=2)).strftime("%Y-%m-%d")
    print("predate==",predate)


    query = "select id,asked_on,query,flag from chat_history where (cast(asked_on as date) between '" + str(
        predate) + "'and '" + str(currentdate) + "') and userID = '" + str(userID) + "' order by id desc limit 10"
    print(query)
    output = create_query(query)
    # new_output = list(output).replace('"',"'").replace("/-","")
    print("op==", output)
    tags_list = list(output)

    json_array = []

    if len(tags_list) > 0:
        for data in tags_list[::-1]:
            sim = {
                "date_time": str(data[1]),
                "query": (data[2]).replace("/-", "").replace("\n", " ").replace("\r", " "),
                "flag": data[3],

            }

            json_array.append(sim)
        json_data = {
                "message": "History",
                "ParameterTitle": "",
                "ParameterType": "",
                "action": json_array
        }

        data = json.dumps(json_data,sort_keys=True,indent=4 * '')
        print(data)
        resp = flask.Response(encrypt(data))
        # resp = flask.Response(data)
        #logger.info(f'{userID} [get] Response:' + str(json_data))
        return resp
    else:
        json_data = {"message":"No history"}
        data = json.dumps(json_data, sort_keys=True, indent=4 * '')
        print(data)
        resp = flask.Response(encrypt(data))
        #resp = flask.Response(data)
        ##logger.info(f'{userID} [get] Response:' + str(json_data))
        return resp

@app.route('/survey',methods=['POST','GET'])
def get_survey():
    message1 = request.get_data()
    message = decrypt(message1)
    objectreceived = json.loads(message)
    print("survey ------> ",objectreceived)

    surveyID = objectreceived.get('surveyID')
    userID = objectreceived.get('userID')
    currentdate = datetime.now().strftime("%Y-%m-%d")
    print("survey date == ",currentdate)

    query = "select survey_id,title from survey where NOT EXISTS(select survey_id from survey_submit_details " \
            "where survey.survey_id = survey_submit_details.survey_id and survey_submit_details.emp_id = '" + userID + "') " \
             "and ( status = 'Active' and start_date <= '" + str(currentdate) + "' and end_date >= '" + str(currentdate) + "')"
    #query = "select survey_id,title,start_date,end_date from survey where survey_id= " + surveyID
    print('survey query----',query)
    output = create_query(query)
    print('survey o/p---->',output)
    tag_list = list(output)
    json_array = []

    if len(tag_list) > 0:
        for data in tag_list :
            sim ={
                "survey_id":str(data[0]),
                "title": data[1],
                # "start_date": str(data[2]),
                # "end_date":str(data[3]),
            }
            json_array.append(sim)

        json_data= {
                "message": "Survey",
                 "ParameterTitle": "",
                "ParameterType": "",
                "action": json_array
            }

        data = json.dumps(json_data, sort_keys=True, indent=4 * '')
        print(data)
        resp = flask.Response(encrypt(data))
        return resp
    else:
            json_data={
                "message":"No data found"
            }
            data = json.dumps(json_data, sort_keys=True, indent=4 * '')
            print(data)
            resp = flask.Response(encrypt(data))
            return resp

@app.route('/surveyDetails', methods=['POST', 'GET'])
def get_surveyDetails():
    message1 = request.get_data()
    message = decrypt(message1)
    objectreceived = json.loads(message)
    print("Survey Details ----------->", objectreceived)

    userID = objectreceived.get("userID")
    surveyID = objectreceived.get("surveyID")
    questionID = objectreceived.get("questionID")

    query = "select survey_id,question_id,question,type,options from survey_details where survey_id = '" + str(surveyID) + "' and status = 'Active' "

    print(query)
    #print(query)
    output = create_query(query)
    print("survey_details o/p------------>",output)
    tag_list = list(output)
    json_array = []

    if len(tag_list) > 0:
        for data in tag_list:
            options = data[4]

            if "," in options:
                optns_list = options.split(",")
                print("===",optns_list)


                sim = {
                    "surevey_id":str(data[0]),
                    "question_id":data[1],
                    "question":data[2],
                    "type":data[3].lower(),
                    "options":optns_list
                }
            else:
                sim = {
                    "surevey_id": str(data[0]),
                    "question_id": data[1],
                    "question": data[2],
                    "type": data[3].lower(),
                    "options": options
                }
            json_array.append(sim)

        json_data={
                "message":"Survey Questions",
                "ParameterTitle": "",
                "ParameterType": "",
                "action": json_array
             }

        data = json.dumps(json_data, sort_keys=True, indent=4* '')
        print(data)
        resp = flask.Response(encrypt(data))
        return resp
    else:
        json_data = {"message":"No data found"}
        data = json.dumps(json_data, sort_keys=True, indent=4* '')
        print(data)
        resp = flask.Response(encrypt(data))
        return resp

@app.route('/survey_submittedDetails',methods=["POST","GET"])
def  set_survey_submittedDetails():
    message1 = request.get_data()
    message = decrypt(message1)
    objectreceived = json.loads(message)
    print("Survey Submitted Details ------------------->", objectreceived)

    userID = objectreceived.get("empID")
    surveyID = objectreceived.get("surveyID")
    questionID = objectreceived.get("questionID")
    answer = objectreceived.get("answer")
    username = objectreceived.get("userName")

    query = "insert into survey_submit_details(emp_id,survey_id,question_id,answer,emp_name)values('" + str(userID) + "','" + str(surveyID) + "','" + str(questionID) + "','" + str(answer) + "','" + username + "')"
    print(query)
    output = insertquery(query)
    print(output)

    json_data = {"message": "data added"}
    data = json.dumps(json_data, sort_keys=True, indent=4 * '')
    print(data)
    resp = flask.Response(encrypt(data))
    return resp

def gettext(text,language):
    if text == "Are you looking for?":
        a={
            "gu":"તમે શું શોધી રહ્યા છો?",
            "hi": "आप क्या ढूंढ रहे हो?",
            "ml": "എന്താണ് നിങ്ങൾ തിരയുന്നത്?",
            "mr": "आपणास काय हवे आहे?",
            "ta": "நீங்கள் என்ன தேடுகிறீர்கள்?",
            "te": "మీరు ఏమి చూస్తున్నారు?",
            "ur": "تم کیا تلاش کر رہے ہو؟",
            "pa": "ਤੁਸੀਂ ਕੀ ਲੱਭ ਰਹੇ ਹੋ?",
        }
    elif text == "Please help me with the below mentioned details for your Reminder.##Remform##":
        a = {
            "gu": "કૃપા કરીને તમારી રીમાઇન્ડર માટે નીચે આપેલી વિગતો સાથે મને સહાય કરો.##Remform##",
            "hi": "कृपया अपने अनुस्मारक के लिए नीचे दिए गए विवरणों के साथ मेरी मदद करें।##Remform##",
            "ml": "നിങ്ങളുടെ ഓർമ്മപ്പെടുത്തലിനായി ചുവടെ സൂചിപ്പിച്ച വിശദാംശങ്ങൾ ദയവായി എന്നെ സഹായിക്കൂ.##Remform##",
            "mr": "कृपया आपल्या स्मरणपत्रासाठी खाली दिलेल्या तपशीलांसह मला मदत करा.##Remform##",
            "ta": "உங்கள் நினைவூட்டலுக்கு கீழே குறிப்பிடப்பட்டுள்ள விவரங்களுக்கு எனக்கு உதவுங்கள்.##Remform##",
            "te": "దయచేసి మీ రిమైండర్ కోసం క్రింద పేర్కొన్న వివరాలతో నాకు సహాయం చేయండి.##Remform##",
            "ur": "##Remform##براہ کرم اپنی یاد دہانی کے لئے نیچے دیئے گئے تفصیلات کے ساتھ میری مدد کریں۔",
            "pa": "ਕਿਰਪਾ ਕਰਕੇ ਆਪਣੀ ਯਾਦ ਦਿਵਾਉਣ ਲਈ ਹੇਠਾਂ ਦਿੱਤੇ ਵੇਰਵਿਆਂ ਦੀ ਮੇਰੀ ਮਦਦ ਕਰੋ.##Remform##",
        }
    elif text == "Apply for Leave.##form##":
        a = {
            "gu": "રજા માટે અરજી કરો.##form##",
            "hi": "छुट्टी के लिए आवेदन करें।##form##",
            "ml": "അവധിക്ക് അപേക്ഷിക്കുക.##form##",
            "mr": "रजेसाठी अर्ज करा.##form##",
            "ta": "விடுப்புக்கு விண்ணப்பிக்கவும்.##form##",
            "te": "సెలవు కోసం దరఖాస్తు చేసుకోండి.##form##",
            "ur": "##form##چھٹی کے لئے درخواست دیں۔",
            "pa": "ਛੁੱਟੀ ਲਈ ਅਰਜ਼ੀ ਦਿਓ.##form##",
        }
    elif text == "There was an error encountered for applying Leave.PLease try after sometime.##C##":
        a = {
            "gu": "રજા લાગુ કરવા માટે એક ભૂલ આવી હતી. કૃપા કરીને થોડા સમય પછી પ્રયત્ન કરો.##C##",
            "hi": "अवकाश लागू करने में त्रुटि हुई थी। बाद में पुन: प्रयास करें।##C##",
            "ml": "അവധി പ്രയോഗിക്കുന്നതിൽ ഒരു പിശക് ഉണ്ടായിരുന്നു. പിന്നീട് വീണ്ടും ശ്രമിക്കുക.##C##",
            "mr": "रजा लावताना त्रुटी आली. कृपया पुन्हा प्रयत्न करा.##C##",
            "ta": "விடுப்பு விண்ணப்பிப்பதில் பிழை ஏற்பட்டது. பின்னர் மீண்டும் முயற்சிக்கவும்.##C##",
            "te": "సెలవు దరఖాస్తులో లోపం ఉంది. దయచేసి తర్వాత మళ్లీ ప్రయత్నించండి.##C##",
            "ur": "##C##چھٹی کو درخواست دینے میں ایک خامی تھی۔ براہ کرم کچھ دیر بعد کوشش کریں.",
            "pa": "ਛੁੱਟੀ ਲਾਗੂ ਕਰਨ ਵੇਲੇ ਇੱਕ ਗਲਤੀ ਹੋਈ ਸੀ. ਬਾਅਦ ਵਿੱਚ ਦੁਬਾਰਾ ਕੋਸ਼ਿਸ਼ ਕਰੋ ਜੀ.##C##",
        }
    elif text == "I am sorry, we could not find a solution for your reported issue. Would you like to send a mail to Help Desk Team?":
        a={
            "gu": "માફ કરશો, અમે તમારી જાણ કરેલી સમસ્યા માટે કોઈ સમાધાન શોધી શક્યાં નથી. તમે તકનીકી ટીમને મેલ મોકલવા માંગો છો?",
            "hi": "मुझे खेद है, हमें आपकी रिपोर्ट की गई समस्या का समाधान नहीं मिला। क्या आप तकनीकी टीम को एक मेल भेजना चाहेंगे?",
            "ml": "ക്ഷമിക്കണം, നിങ്ങളുടെ റിപ്പോർട്ടുചെയ്‌ത പ്രശ്‌നത്തിന് ഞങ്ങൾക്ക് പരിഹാരം കണ്ടെത്താൻ കഴിഞ്ഞില്ല. സാങ്കേതിക ടീമിന് ഒരു മെയിൽ അയയ്ക്കാൻ നിങ്ങൾ ആഗ്രഹിക്കുന്നുണ്ടോ?",
            "mr": "मला माफ करा, आम्ही आपल्या नोंदविलेल्या समस्येचे निराकरण करू शकलो नाही. आपण तांत्रिक कार्यसंघाला मेल पाठवू इच्छिता?",
            "ta": "மன்னிக்கவும், நீங்கள் புகாரளித்த பிரச்சினைக்கு எங்களால் தீர்வு காண முடியவில்லை. தொழில்நுட்ப குழுவுக்கு ஒரு மெயில் அனுப்ப விரும்புகிறீர்களா?",
            "te": "క్షమించండి, మీ నివేదించిన సమస్యకు మేము పరిష్కారం కనుగొనలేకపోయాము. మీరు సాంకేతిక బృందానికి మెయిల్ పంపాలనుకుంటున్నారా?",
            "ur": "مجھے افسوس ہے ، ہم آپ کے بیان کردہ مسئلے کا حل نہیں ڈھونڈ سکے۔ کیا آپ تکنیکی ٹیم کو میل بھیجنا پسند کریں گے؟",
            "pa": "ਮੈਨੂੰ ਅਫ਼ਸੋਸ ਹੈ, ਅਸੀਂ ਤੁਹਾਡੇ ਰਿਪੋਰਟ ਕੀਤੇ ਮੁੱਦੇ ਦਾ ਕੋਈ ਹੱਲ ਨਹੀਂ ਲੱਭ ਸਕੇ. ਕੀ ਤੁਸੀਂ ਤਕਨੀਕੀ ਟੀਮ ਨੂੰ ਮੇਲ ਭੇਜਣਾ ਚਾਹੋਗੇ?",

        }
    elif text == "I am sorry, we could not find a solution for your reported issue. Would you like to raise a ticket to the Help Desk Team?":
        a={
            "gu": "માફ કરશો, અમે તમારી જાણ કરેલી સમસ્યા માટે કોઈ સમાધાન શોધી શક્યાં નથી. શું તમે હેલ્પ ડેસ્ક ટીમમાં ટિકિટ વધારવા માંગો છો?",
            "hi": "मुझे खेद है, हमें आपकी रिपोर्ट की गई समस्या का समाधान नहीं मिला। क्या आप हेल्प डेस्क टीम को टिकट देना चाहेंगे?",
            "ml": "ക്ഷമിക്കണം, നിങ്ങളുടെ റിപ്പോർട്ടുചെയ്‌ത പ്രശ്‌നത്തിന് ഞങ്ങൾക്ക് പരിഹാരം കണ്ടെത്താൻ കഴിഞ്ഞില്ല. ഹെൽപ്പ് ഡെസ്ക് ടീമിലേക്ക് ടിക്കറ്റ് ഉയർത്താൻ നിങ്ങൾ ആഗ്രഹിക്കുന്നുണ്ടോ?",
            "mr": "मला माफ करा, आम्ही आपल्या नोंदविलेल्या समस्येचे निराकरण करू शकलो नाही. आपण मदत डेस्क कार्यसंघाचे तिकीट वाढवू इच्छिता?",
            "ta": "மன்னிக்கவும், நீங்கள் புகாரளித்த பிரச்சினைக்கு எங்களால் தீர்வு காண முடியவில்லை. ஹெல்ப் டெஸ்க் குழுவுக்கு டிக்கெட் உயர்த்த விரும்புகிறீர்களா?",
            "te": "క్షమించండి, మీ నివేదించిన సమస్యకు మేము పరిష్కారం కనుగొనలేకపోయాము. మీరు హెల్ప్ డెస్క్ బృందానికి టికెట్ పెంచాలనుకుంటున్నారా?",
            "ur": "مجھے افسوس ہے ، ہم آپ کے بیان کردہ مسئلے کا حل نہیں ڈھونڈ سکے۔ کیا آپ ہیلپ ڈیسک ٹیم کے لئے ٹکٹ بڑھانا چاہیں گے؟",
            "pa": "ਮੈਨੂੰ ਅਫ਼ਸੋਸ ਹੈ, ਅਸੀਂ ਤੁਹਾਡੇ ਰਿਪੋਰਟ ਕੀਤੇ ਮੁੱਦੇ ਦਾ ਕੋਈ ਹੱਲ ਨਹੀਂ ਲੱਭ ਸਕੇ. ਕੀ ਤੁਸੀਂ ਹੈਲਪ ਡੈਸਕ ਟੀਮ ਨੂੰ ਟਿਕਟ ਦੇਣਾ ਚਾਹੁੰਦੇ ਹੋ?",

        }
    elif text == "Sure, can you please enter the issue your are facing.":
        a = {
            "gu": "ઠીક છે, તમે જે મુદ્દો સામનો કરી રહ્યાં છો તે દાખલ કરી શકો છો?",
            "hi": "ठीक है, क्या आप कृपया उस समस्या को टाइप कर सकते हैं जिसका सामना आप कर रहे हैं?",
            "ml": "ശരി, നിങ്ങൾ അഭിമുഖീകരിക്കുന്ന പ്രശ്നം ടൈപ്പുചെയ്യാമോ?",
            "mr": "ठीक आहे, आपण ज्या समस्येस तोंड देत आहात तो कृपया टाइप करू शकता?",
            "ta": "சரி, நீங்கள் எதிர்கொள்ளும் சிக்கலை தயவுசெய்து தட்டச்சு செய்ய முடியுமா?",
            "te": "సరే, మీరు ఎదుర్కొంటున్న సమస్యను దయచేసి టైప్ చేయగలరా??",
            "ur": "ٹھیک ہے ، کیا آپ براہ کرم اس مسئلے کو ٹائپ کرسکتے ہیں جس کا سامنا آپ کر رہے ہیں؟",
            "pa": "ਠੀਕ ਹੈ, ਕੀ ਤੁਸੀਂ ਕਿਰਪਾ ਕਰਕੇ ਉਹ ਮੁੱਦਾ ਟਾਈਪ ਕਰ ਸਕਦੇ ਹੋ ਜਿਸਦਾ ਤੁਸੀਂ ਸਾਹਮਣਾ ਕਰ ਰਹੇ ਹੋ?",

        }
    elif text == "I am fine":
        a = {
            "gu": "હું મજામા છુ",
            "hi": "मैं ठीक हूँ",
            "ml": "എനിക്ക് സുഖമാണ്",
            "mr": "मी ठीक आहे",
            "ta": "நான் நன்றாக இருக்கிறேன்",
            "te": "నేను బాగున్నాను",
            "ur": "میں ٹھیک ہوں",
            "pa": "ਮੈਂ ਠੀਕ ਹਾਂ",

        }
    elif text == "I am SuperE - The Company Service Bot :)":
        a = {
            "gu": "હું સુપર ઇ છું - કંપની સેવા બોટ :)",
            "hi": "ममैं सुपर ई हूँ - कंपनी सेवा बॉट :)",
            "ml": "ഞാൻ സൂപ്പർ ഇ - കമ്പനി സർവീസ് ബോട്ട് :)",
            "mr": "मी सुपर ई - कंपनी सर्व्हिस बॉट :)",
            "ta": "நான் சூப்பர் இ - கம்பெனி சர்வீஸ் போட் :)",
            "te": "నేను సూపర్ ఇ - కంపెనీ సర్వీస్ బోట్ :)",
            "ur": "میں سپر ای ہوں - کمپنی سروس بیوٹی :)",
            "pa": "ਮੈਂ ਸੁਪਰ ਈ ਹਾਂ - ਕੰਪਨੀ ਸਰਵਿਸ ਬੋਟ :)",

        }
    elif text == "No leave pending to be approved by you.":
        a = {
            "gu": "તમારા દ્વારા માન્ય થવા માટે કોઈ રજા બાકી નથી.",
            "hi": "आपके द्वारा अनुमोदित होने के लिए कोई अवकाश लंबित नहीं है।",
            "ml": "നിങ്ങൾ അംഗീകരിക്കുന്നതിന് അവധി തീർപ്പുകൽപ്പിച്ചിട്ടില്ല.",
            "mr": "आपण मंजूर करण्यासाठी कोणतीही रजा शिल्लक नाही.",
            "ta": "நீங்கள் அங்கீகரிக்க எந்த விடுமுறையும் நிலுவையில் இல்லை.",
            "te": "మీరు ఆమోదించడానికి సెలవు పెండింగ్‌లో లేదు.",
            "ur": "آپ کے منظور ہونے کے لئے کوئی چھٹی باقی نہیں ہے۔",
            "pa": "ਤੁਹਾਡੇ ਦੁਆਰਾ ਮਨਜ਼ੂਰੀ ਲਈ ਕੋਈ ਛੁੱਟੀ ਬਕਾਇਆ ਨਹੀਂ.",

        }
    elif text == "I would be happy to tell you more. What would you like to know about":
        a = {
            "gu": "હું તમને વધુ જણાવવામાં ખુશી અનુભવું છું. તમે કયા વિશે જાણવા માગો છો",
            "hi": "मुझे आपको और बताने में खुशी होगी। आप किस बारे में जानना चाहेंगे",
            "ml": "നിങ്ങളോട് കൂടുതൽ പറയാൻ എനിക്ക് സന്തോഷമുണ്ട്. നിങ്ങൾ എന്തിനെക്കുറിച്ചറിയാൻ ആഗ്രഹിക്കുന്നു",
            "mr": "मी तुम्हाला आणखी सांगण्यात आनंदित होईल. आपण कशाबद्दल जाणून घेऊ इच्छिता?",
            "ta": "உங்களிடம் மேலும் சொல்வதில் மகிழ்ச்சி அடைவேன். நீங்கள் எதைப் பற்றி அறிய விரும்புகிறீர்கள்",
            "te": "మీకు మరింత చెప్పడం నాకు సంతోషంగా ఉంది. మీరు దేని గురించి తెలుసుకోవాలనుకుంటున్నారు",
            "ur": "میں آپ کو مزید بتا کر خوشی محسوس کروں گا۔ آپ کس چیز کے بارے میں جاننا چاہیں گے؟",
            "pa": "ਮੈਂ ਤੁਹਾਨੂੰ ਵਧੇਰੇ ਦੱਸਕੇ ਖੁਸ਼ ਮਹਿਸੂਸ ਕਰਾਂਗਾ. ਤੁਸੀਂ ਕਿਸ ਬਾਰੇ ਜਾਣਨਾ ਚਾਹੋਗੇ",

        }
    elif text == "Here are the details of your Applied Leaves":
        a = {
            "gu": "અહીં તમારી લાગુ રજાની વિગતો છે",
            "hi": "यहां आपके लागू अवकाश का विवरण दिया गया है",
            "ml": "നിങ്ങളുടെ അപേക്ഷിച്ച അവധിയുടെ വിശദാംശങ്ങൾ ഇതാ",
            "mr": "आपल्या लागू केलेल्या रजेचा तपशील येथे आहे",
            "ta": "நீங்கள் விண்ணப்பித்த விடுப்பின் விவரங்கள் இங்கே",
            "te": "మీరు దరఖాస్తు చేసుకున్న సెలవు వివరాలు ఇక్కడ ఉన్నాయి",
            "ur": "آپ کی درخواست کردہ رخصت کی تفصیلات یہ ہیں",
            "pa": "ਤੁਹਾਡੀ ਲਾਗੂ ਕੀਤੀ ਛੁੱਟੀ ਦਾ ਵੇਰਵਾ ਇਹ ਹੈ",

        }
    elif text == "No leaves for your ID yet.":
        a = {
            "gu": "તમારી આઈડી માટે હજી રજા નહીં.",
            "hi": "आपकी आईडी के लिए अभी तक कोई छुट्टी नहीं है।",
            "ml": "നിങ്ങളുടെ ഐഡിക്ക് ഇതുവരെ അവധിയില്ല.",
            "mr": "आपल्या आयडीसाठी अद्याप रजा नाही.",
            "ta": "உங்கள் ஐடிக்கு இன்னும் விடுப்பு இல்லை.",
            "te": "మీ ID కి ఇంకా సెలవు లేదు.",
            "ur": "ابھی آپ کی شناخت کے لئے کوئی رخصت نہیں ہے۔",
            "pa": "ਤੁਹਾਡੀ ID ਲਈ ਅਜੇ ਕੋਈ ਛੁੱਟੀ ਨਹੀਂ.",

        }
    elif text == "Here are the details of your Reminders for Today":
        a = {
            "gu": "તમારા આજનાં સ્મૃતિપત્રોની વિગતો અહીં છે",
            "hi": "यहां आपके आज के अनुस्मारक की जानकारी दी गई है",
            "ml": "ഇന്നത്തെ നിങ്ങളുടെ ഓർമ്മപ്പെടുത്തലുകളുടെ വിശദാംശങ്ങൾ ഇതാ",
            "mr": "आपल्या आजच्या स्मरणपत्रांचा तपशील येथे आहे",
            "ta": "இன்றைய உங்கள் நினைவூட்டல்களின் விவரங்கள் இங்கே",
            "te": "ఈ రోజు మీ రిమైండర్‌ల వివరాలు ఇక్కడ ఉన్నాయి",
            "ur": "آپ کی آج کی یاد دہانیوں کی تفصیلات یہ ہیں",
            "pa": "ਅੱਜ ਤੁਹਾਡੇ ਯਾਦ ਦਿਵਾਉਣ ਵਾਲੇ ਦੇ ਵੇਰਵੇ ਹੇਠ ਦਿੱਤੇ ਗਏ ਹਨ",

        }
    elif text == "No Reminders for today.":
        a = {
            "gu": "આજે માટે કોઈ રીમાઇન્ડર નહીં.",
            "hi": "आज के लिए कोई अनुस्मारक नहीं।",
            "ml": "ഇന്നത്തേക്ക് ഓർമ്മപ്പെടുത്തലൊന്നുമില്ല.",
            "mr": "आजसाठी कोणतेही स्मरणपत्र नाही.",
            "ta": "இன்று நினைவூட்டல் இல்லை.",
            "te": "ఈ రోజుకు రిమైండర్ లేదు.",
            "ur": "آج کے لئے کوئی یاد دہانی نہیں.",
            "pa": "ਅੱਜ ਲਈ ਕੋਈ ਯਾਦ ਨਹੀਂ.",
        }
    elif text == "Here are the details of your Reminders for Tommorow":
        a = {
            "gu": "તમારા આવતીકાલની સ્મૃતિપત્રોની વિગતો અહીં છે",
            "hi": "यहां आपके कल के अनुस्मारक की जानकारी दी गई है",
            "ml": "നാളത്തെ നിങ്ങളുടെ ഓർമ്മപ്പെടുത്തലുകളുടെ വിശദാംശങ്ങൾ ഇതാ",
            "mr": "आपल्या उद्याच्या स्मरणपत्रांचा तपशील येथे आहे",
            "ta": "உங்கள் நாளைய நினைவூட்டல்களுக்கான விவரங்கள் இங்கே",
            "te": "రేపటి మీ రిమైండర్‌ల వివరాలు ఇక్కడ ఉన్నాయి",
            "ur": "کل آپ کی یاد دہانیوں کے لئے تفصیلات یہ ہیں",
            "pa": "ਤੁਹਾਡੇ ਕੱਲ੍ਹ ਦੀਆਂ ਯਾਦ ਦਿਵਾਉਣ ਵਾਲਿਆਂ ਲਈ ਵੇਰਵਾ ਇਹ ਹੈ",

        }
    elif text == "No Reminders for Tommorow.":
        a = {
            "gu": "આવતી કાલ માટે કોઈ રીમાઇન્ડર નહીં.",
            "hi": "कल के लिए कोई अनुस्मारक नहीं।",
            "ml": "നാളത്തേക്ക് ഓർമ്മപ്പെടുത്തലൊന്നുമില്ല",
            "mr": "उद्याची कोणतीही स्मरणपत्रे नाहीत",
            "ta": "நாளைய நினைவூட்டல்கள் இல்லை",
            "te": "రేపటి రిమైండర్‌లు లేవు",
            "ur": "کل کی کوئی یاد دہانی نہیں",
            "pa": "ਕੱਲ੍ਹ ਦਾ ਕੋਈ ਰਿਮਾਈਂਡਰ ਨਹੀਂ",
        }

    elif text == "Here are the details of your Reminders for this Week":
        a = {
            "gu": "આ અઠવાડિયાના તમારા રિમાઇન્ડરની વિગતો અહીં છે",
            "hi": "इस सप्ताह के आपके अनुस्मारक के विवरण इस प्रकार हैं",
            "ml": "ഈ ആഴ്‌ചയിലെ നിങ്ങളുടെ ഓർമ്മപ്പെടുത്തലിന്റെ വിശദാംശങ്ങൾ ഇതാ",
            "mr": "या आठवड्यातील आपल्या स्मरणपत्राचा तपशील येथे आहे",
            "ta": "இந்த வாரத்தின் உங்கள் நினைவூட்டலின் விவரங்கள் இங்கே",
            "te": "ఈ వారం మీ రిమైండర్ వివరాలు ఇక్కడ ఉన్నాయి",
            "ur": "اس ہفتے کی آپ کی یاد دہانی کی تفصیلات یہاں ہیں",
            "pa": "ਇਸ ਹਫ਼ਤੇ ਦੇ ਤੁਹਾਡੇ ਯਾਦ ਕਰਾਉਣ ਦੇ ਵੇਰਵੇ ਹੇਠ ਦਿੱਤੇ ਗਏ ਹਨ",

        }
    elif text == "No Reminders for this week.":
        a = {
            "gu": "આ અઠવાડિયા માટે કોઈ રીમાઇન્ડર્સ નથી",
            "hi": "इस सप्ताह के लिए कोई अनुस्मारक नहीं",
            "ml": "ഈ ആഴ്‌ചയ്‌ക്കായി ഓർമ്മപ്പെടുത്തലുകളൊന്നുമില്ല",
            "mr": "या आठवड्यासाठी कोणतीही स्मरणपत्र नाही",
            "ta": "இந்த வாரத்திற்கு நினைவூட்டல் இல்லை",
            "te": "ఈ వారానికి రిమైండర్ లేదు",
            "ur": "اس ہفتے کے لئے کوئی یاد دہانی نہیں ہے",
            "pa": "ਇਸ ਹਫ਼ਤੇ ਲਈ ਕੋਈ ਰੀਮਾਈਂਡਰ ਨਹੀਂ",
        }

    elif text == "Here are the details of your Reminders for this Month":
        a = {
            "gu": "આ મહિનાના તમારા રિમાઇન્ડર્સની વિગતો અહીં છે",
            "hi": "इस महीने के लिए आपके अनुस्मारक का विवरण यहां दिया गया है",
            "ml": "ഈ മാസത്തെ നിങ്ങളുടെ ഓർമ്മപ്പെടുത്തലുകളുടെ വിശദാംശങ്ങൾ ഇതാ",
            "mr": "या महिन्यासाठी आपल्या स्मरणपत्रांचा तपशील येथे आहे",
            "ta": "இந்த மாதத்திற்கான உங்கள் நினைவூட்டல்களின் விவரங்கள் இங்கே",
            "te": "ఈ నెల మీ రిమైండర్‌ల వివరాలు ఇక్కడ ఉన్నాయి",
            "ur": "اس مہینے کی یاد دہانیوں کی تفصیلات یہ ہیں",
            "pa": "ਇਸ ਮਹੀਨੇ ਲਈ ਰਿਮਾਈਂਡਰ ਦਾ ਵੇਰਵਾ ਇਹ ਹੈ",

        }
    elif text == "No Reminders for this Month.":
        a = {
            "gu": "આ મહિના માટે કોઈ રીમાઇન્ડર્સ નથી.",
            "hi": "इस महीने के लिए कोई अनुस्मारक नहीं।",
            "ml": "ഈ മാസത്തേക്ക് ഓർമ്മപ്പെടുത്തലുകളൊന്നുമില്ല.",
            "mr": "या महिन्यासाठी कोणतीही स्मरणपत्रे नाहीत.",
            "ta": "இந்த மாதத்திற்கான நினைவூட்டல்கள் இல்லை.",
            "te": "ఈ నెలకు రిమైండర్‌లు లేవు.",
            "ur": "اس مہینے کے لئے کوئی یاد دہانی نہیں ہے۔",
            "pa": "ਇਸ ਮਹੀਨੇ ਲਈ ਕੋਈ ਰੀਮਾਈਂਡਰ ਨਹੀਂ.",
        }

    elif text == "Here are the details of your Reminders":
        a = {
            "gu": "અહીં તમારા રિમાઇન્ડર્સની વિગતો છે",
            "hi": "यहां आपके अनुस्मारक का विवरण दिया गया है",
            "ml": "നിങ്ങളുടെ ഓർമ്മപ്പെടുത്തലുകളുടെ വിശദാംശങ്ങൾ ഇതാ",
            "mr": "आपल्या स्मरणपत्रांचा तपशील येथे आहे",
            "ta": "உங்கள் நினைவூட்டல்களின் விவரங்கள் இங்கே",
            "te": "మీ రిమైండర్‌ల వివరాలు ఇక్కడ ఉన్నాయి",
            "ur": "آپ کی یاد دہانیوں کی تفصیلات یہ ہیں",
            "pa": "ਤੁਹਾਡੇ ਰਿਮਾਈਂਡਰ ਦਾ ਵੇਰਵਾ ਇਹ ਹੈ",
        }
    elif text == "No Reminders for your ID yet":
        a = {
            "gu": "હજી સુધી તમારી આઈડી માટે કોઈ રીમાઇન્ડર્સ નથી",
            "hi": "आपकी आईडी के लिए अभी तक कोई अनुस्मारक नहीं है",
            "ml": "നിങ്ങളുടെ ഐഡിക്കായി ഇതുവരെ ഓർമ്മപ്പെടുത്തലുകളൊന്നുമില്ല",
            "mr": "आपल्या आयडीसाठी अद्याप कोणतीही स्मरणपत्रे नाहीत",
            "ta": "உங்கள் ஐடிக்கு இன்னும் நினைவூட்டல்கள் இல்லை",
            "te": "మీ ఐడి కోసం ఇంకా రిమైండర్‌లు లేవు",
            "ur": "ابھی تک آپ کی شناخت کے لئے کوئی یاددہانی نہیں ہے",
            "pa": "ਅਜੇ ਤੁਹਾਡੀ ਆਈਡੀ ਲਈ ਕੋਈ ਰੀਮਾਈਂਡਰ ਨਹੀਂ",

        }
    elif text == "You have the below mentioned Notification(s) by the Company Admin":
        a = {
            "gu": "તમારી પાસે કંપની એડમિન દ્વારા નીચે જણાવેલ સૂચનાઓ છે",
            "hi": "आपके पास कंपनी व्यवस्थापक द्वारा नीचे दी गई अधिसूचनाएं हैं",
            "ml": "കമ്പനി അഡ്മിൻ നിങ്ങൾക്ക് ചുവടെ സൂചിപ്പിച്ച അറിയിപ്പുകൾ ഉണ്ട്",
            "mr": "आपल्याकडे कंपनी प्रशासनाच्या खाली नमूद केलेल्या सूचना आहेत",
            "ta": "நிறுவனத்தின் நிர்வாகியின் கீழே குறிப்பிடப்பட்ட அறிவிப்புகள் உங்களிடம் உள்ளன",
            "te": "కంపెనీ అడ్మిన్ మీకు క్రింద పేర్కొన్న నోటిఫికేషన్లు ఉన్నాయి",
            "ur": "کمپنی ایڈمن کے ذریعہ آپ کے پاس مذکورہ بالا نوٹیفیکیشن ہیں",
            "pa": "ਤੁਹਾਡੇ ਕੋਲ ਕੰਪਨੀ ਐਡਮਿਨ ਦੁਆਰਾ ਹੇਠਾਂ ਦੱਸੇ ਗਏ ਨੋਟੀਫਿਕੇਸ਼ਨ ਹਨ",

        }
    elif text == "Kindly contact your Local HR Admin.":
        a = {
            "gu": "કૃપા કરીને તમારા સ્થાનિક એચઆર એડમિનનો સંપર્ક કરો.",
            "hi": "कृपया अपने स्थानीय मानव संसाधन व्यवस्थापक से संपर्क करें।",
            "ml": "നിങ്ങളുടെ പ്രാദേശിക എച്ച്ആർ അഡ്‌മിനുമായി ദയവായി ബന്ധപ്പെടുക.",
            "mr": "कृपया आपल्या स्थानिक एचआर प्रशासनाशी संपर्क साधा.",
            "ta": "தயவுசெய்து உங்கள் உள்ளூர் மனிதவள நிர்வாகியைத் தொடர்பு கொள்ளுங்கள்.",
            "te": "దయచేసి మీ స్థానిక HR నిర్వాహకుడిని సంప్రదించండి.",
            "ur": "برائے مہربانی اپنے مقامی HR ایڈمن سے رابطہ کریں۔",
            "pa": "ਕਿਰਪਾ ਕਰਕੇ ਆਪਣੇ ਸਥਾਨਕ ਐਚਆਰ ਐਡਮਿਨ ਨਾਲ ਸੰਪਰਕ ਕਰੋ.",

        }
    elif text == "Your leave has been applied successfully. It has been forwarded to your Superior Mr. VIkas Kedia for approval.":
        a = {
            "gu": "તમારી રજા સફળતાપૂર્વક લાગુ થઈ છે. મંજૂરી માટે તે તમારા સુપિરિયર શ્રી વીકસ કેડિયાને મોકલવામાં આવ્યું છે.",
            "hi": "आपकी छुट्टी को सफलतापूर्वक लागू किया गया है। इसे आपके श्रेष्ठ श्री विकास केडिया के पास मंजूरी के लिए भेज दिया गया है।",
            "ml": "നിങ്ങളുടെ അവധി വിജയകരമായി പ്രയോഗിച്ചു. ഇത് നിങ്ങളുടെ സുപ്പീരിയർ ശ്രീ വികാസ് കെഡിയയ്ക്ക് അംഗീകാരത്തിനായി കൈമാറി.",
            "mr": "आपली रजा यशस्वीरित्या लागू केली गेली आहे. ते आपल्या वरिष्ठ श्री विकास केडियाकडे मंजुरीसाठी पाठविले गेले आहे.",
            "ta": "உங்கள் விடுப்பு வெற்றிகரமாக பயன்படுத்தப்பட்டது. இது உங்கள் உயர்ந்த திரு. விகாஸ் கெடியா ஒப்புதலுக்காக அனுப்பப்பட்டுள்ளது.",
            "te": "మీ సెలవు విజయవంతంగా వర్తించబడింది. ఇది ఆమోదం కోసం మీ సుపీరియర్ మిస్టర్ వికాస్ కేడియాకు పంపబడింది.",
            "ur": "آپ کی چھٹی کامیابی کے ساتھ لاگو کردی گئی ہے۔ منظوری کے ل It اسے آپ کے سپیریئر مسٹر وکاس کیڈیا کے پاس بھجوا دیا گیا ہے۔",
            "pa": "ਤੁਹਾਡੀ ਛੁੱਟੀ ਸਫਲਤਾਪੂਰਵਕ ਲਾਗੂ ਕੀਤੀ ਗਈ ਹੈ. ਇਸ ਨੂੰ ਪ੍ਰਵਾਨਗੀ ਲਈ ਤੁਹਾਡੇ ਉੱਤਮ ਸ੍ਰੀ ਵਿਕਾਸ ਕੇਡੀਆ ਨੂੰ ਭੇਜਿਆ ਗਿਆ ਹੈ.",

        }
    elif text == "Please help me with the below mentioned details for your Reminder.##Remform##":
        a = {
            "gu": "કૃપા કરીને તમારા રીમાઇન્ડર માટે નીચે આપેલી વિગતો સાથે મને સહાય કરો.##Remform##",
            "hi": "कृपया अपने अनुस्मारक के लिए नीचे दिए गए विवरणों के साथ मेरी मदद करें।##Remform##",
            "ml": "നിങ്ങളുടെ ഓർമ്മപ്പെടുത്തലിനായി ചുവടെ സൂചിപ്പിച്ച വിശദാംശങ്ങൾ ദയവായി എന്നെ സഹായിക്കൂ.##Remform##",
            "mr": "कृपया आपल्या स्मरणपत्रासाठी खाली दिलेल्या तपशीलांसह मला मदत करा.##Remform##",
            "ta": "உங்கள் நினைவூட்டலுக்கு கீழே குறிப்பிடப்பட்டுள்ள விவரங்களுக்கு எனக்கு உதவுங்கள்.##Remform##",
            "te": "దయచేసి మీ రిమైండర్ కోసం క్రింద పేర్కొన్న వివరాలతో నాకు సహాయం చేయండి.##Remform##",
            "ur": "##Remform##براہ کرم اپنی یاد دہانی کے لئے نیچے دیئے گئے تفصیلات کے ساتھ میری مدد کریں۔",
            "pa": "ਕਿਰਪਾ ਕਰਕੇ ਆਪਣੀ ਯਾਦ ਦਿਵਾਉਣ ਲਈ ਹੇਠਾਂ ਦਿੱਤੇ ਵੇਰਵਿਆਂ ਦੀ ਮੇਰੀ ਮਦਦ ਕਰੋ.##Remform##",

        }
    elif text == "Your reminder has been set successfully.":
        a = {
            "gu": "કતમારું રીમાઇન્ડર સફળતાપૂર્વક સેટ થયું છે.",
            "hi": "आपका अनुस्मारक सफलतापूर्वक सेट कर दिया गया है।",
            "ml": "നിങ്ങളുടെ ഓർമ്മപ്പെടുത്തൽ വിജയകരമായി സജ്ജമാക്കി.",
            "mr": "आपले स्मरणपत्र यशस्वीरित्या सेट केले गेले आहे.",
            "ta": "உங்கள் நினைவூட்டல் வெற்றிகரமாக அமைக்கப்பட்டுள்ளது.",
            "te": "మీ రిమైండర్ విజయవంతంగా సెట్ చేయబడింది.",
            "ur": "మీ రిమైండర్ విజయవంతంగా సెట్ చేయబడింది.",
            "pa": "ਤੁਹਾਡਾ ਰੀਮਾਈਂਡਰ ਸਫਲਤਾਪੂਰਵਕ ਸੈੱਟ ਕੀਤਾ ਗਿਆ ਹੈ.",

        }

    taglist = a.get(language)
    return taglist


@app.route('/get', methods=["POST", "GET"])
def get_bot_response():
    message1 = request.get_data()  # getting binary string
    message = decrypt(message1)
    user_text = json.loads(message)
    #user_text = json.loads(message1)  # converting  string to json object
    print("get obj== ", user_text)
    usertext = user_text.get('msg')
    print("user query = ", usertext)
    username = user_text.get('userName')
    userID = user_text.get('userID')
    statusFlag = user_text.get('searchFlag')
    temtext = user_text.get('msg')  # storing original text value
    mainIssue = user_text.get('mainIssue')
    platform = user_text.get('platform')
    operation_id = user_text.get('operation_id')
    main_op_id = user_text.get('main_op_id')
    userType = user_text.get('userType ')

    language = user_text.get('language')
    language_flag = False
    print("language++++++",language)
    if language == "gu" or language == "hi" or language == "ml" or language == "mr" or language == "ta" or language == "te" or language == "ur" or language == "pa":
        language_flag = True
        usertext = translate_text(usertext,'en')
    else:
        # language= detect_lang(usertext)
        language_flag = False
    print(language_flag)
    areyoulookingfor = "Are you looking for?"
    if language_flag:
        areyoulookingfor = gettext(areyoulookingfor, language)
        
    pleasehelp = "Please help me with the below mentioned details for your Reminder.##Remform##"
    if language_flag:
        pleasehelp = gettext(pleasehelp, language)
    applyleave = "Apply for Leave.##form##"
    if language_flag:
        applyleave = gettext(applyleave, language)

    leaveerror = "There was an error encountered for applying Leave.PLease try after sometime.##C##"
    if language_flag:
        leaveerror = gettext(leaveerror, language)
    #imsorry = "I am sorry, we could not find a solution for your reported issue. Would you like to send a mail to Help Desk Team?"
    imsorry = "I am sorry, we could not find a solution for your reported issue. Would you like to raise a ticket to the Help Desk Team?"
    if language_flag:
        imsorry = gettext(imsorry, language)


    enterissue = "Sure, can you please enter the issue your are facing."
    if language_flag:
        enterissue = gettext(enterissue, language)

    imfine = "I am fine"
    if language_flag:
        imfine = gettext(imfine, language)

    imsupere = "I am SuperE - The Company Service Bot :)"
    if language_flag:
        imsupere = gettext(imsupere, language)

    levpending = "No leave pending to be approved by you."
    if language_flag:
        levpending = gettext(levpending, language)

    wldhappy = "I would be happy to tell you more. What would you like to know about"
    if language_flag:
        wldhappy = gettext(wldhappy, language)




    
    if str(statusFlag).lower() == "type" or str(statusFlag).lower() == "click":
        word_tokens = word_tokenize(usertext.lower())
        filtered_sentence = []
        for w in word_tokens:
            w = spell(w.lower())
            # w = lem.lemmatize(w, 'v')
            # print("after spell check = ",w)
            if w.lower() not in stop_words:
                filtered_sentence.append(w)

        usertext = " ".join(filtered_sentence)

        print("removing stopwords = ", usertext)

    if "issue" == temtext:
        usertext = temtext
    text1 = str(temtext) + ""
    if "inc-" in usertext.lower() or "sr-" in usertext.lower():
        usertext = "ticket status"

    chkDate = parse_multiple(str(usertext).replace("(","").replace(")","").replace("/",""))
    print("chk date==",chkDate)



    # try:
    print("op== ",operation_id)
    print("main op== ",main_op_id)
    print("userID = ", userID)

    meetingFlag = False
    callFlag = False

    if "meeting" in usertext.lower():
        meetingFlag = True
    elif "call" in usertext.lower():
        callFlag = True
    rem_type = chkFlags(meetingFlag,callFlag)
    print("rem type==",rem_type)

    if ("create" in usertext.lower() or "set" in usertext.lower() or "add" in usertext.lower()) and ("reminder" in usertext.lower() or "reminders" in usertext.lower() or "Reminder(s)" in usertext or "appointment" in usertext):
            today = datetime.now().strftime("%d-%m-%Y")
            print("second block")
            if ("today" in usertext.lower() or "todays" in usertext.lower()):
                json_data = {
                                "message": pleasehelp,
                                "operation_id": "170",
                                "response": pleasehelp,
                                "userText": usertext,
                                "title": pleasehelp,
                                "cat1": "Reminder",
                                "cat2": "HR",
                                "cat3": "Queries",
                                "cat4": "",
                                "video_path": "",
                                "project_name": "",
                                "ParameterTitle": "",
                                "action": "",
                                "orignalText": "",
                                "typetext": "HR",
                                "mainIssue": mainIssue,
                                "emailFlag": "",
                                "date": today,
                                "rem_type": rem_type
                            }

                data1 = json.dumps(json_data, sort_keys=True, indent=4 * ' ')
                data = data1
                data2 = json.dumps(json_data,ensure_ascii=False)

                dbInsertion(temtext, data2, "answered", username,userType, userID, "-1", mainIssue, "--", "-1")
                resp = flask.Response(encrypt(data))
                #resp = flask.Response(data)
               #logger.info(f'{userID} [get] Response:' + str(json_data))
                return resp

            elif ("tomorrow" in usertext.lower() or "tomorrows" in usertext.lower()):
                currentdate = datetime.now()
                tom_date = (currentdate + timedelta(days=1)).strftime("%d-%m-%Y")


                json_data = {
                                "message": pleasehelp,
                                "operation_id": "170",
                                "response": pleasehelp,
                                "userText": usertext,
                                "title": pleasehelp,
                                "cat1": "Reminder",
                                "cat2": "HR",
                                "cat3": "Queries",
                                "cat4": "",
                                "video_path": "",
                                "project_name": "",
                                "ParameterTitle": "",
                                "action": "",
                                "orignalText": "",
                                "typetext": "HR",
                                "mainIssue": mainIssue,
                                "emailFlag": "",
                                "date": tom_date,
                                "rem_type": rem_type
                            }


                data1 = json.dumps(json_data, sort_keys=True, indent=4 * ' ')
                data = data1
                data2 = json.dumps(json_data,ensure_ascii=False)
                dbInsertion(temtext, data2, "answered", username,userType, userID, "-1", mainIssue, "--", "-1")
                resp = flask.Response(encrypt(data))
                #resp = flask.Response(data)
               #logger.info(f'{userID} [get] Response:' + str(json_data))
                return resp
            else:
                print("in elseee")
                today = datetime.now().strftime("%d-%m-%Y")
                # usertext1 = str(usertext).replace("(","").replace(")","")
                # print("@@@",usertext1)
                # ab = parse_multiple(usertext1)
                # print("reminder dates == ", ab)

                # if len(ab) >= 1:
                #     if ab[0].date().day <= 12 and not monthchk(usertext):
                #         date = datetime.strptime(str(ab[0].date()), "%Y-%d-%m").strftime("%d/%m/%Y")
                #     else:
                #         date = datetime.strptime(str(ab[0].date()), "%Y-%m-%d").strftime("%d/%m/%Y")
                if len(chkDate) >= 1:
                    if chkDate[0].date().day <= 12 and not monthchk(usertext):
                        date = datetime.strptime(str(chkDate[0].date()), "%Y-%d-%m").strftime("%d/%m/%Y")
                    else:
                        date = datetime.strptime(str(chkDate[0].date()), "%Y-%m-%d").strftime("%d/%m/%Y")
                    # print(date)
                    print("date==>", date)

                    json_data = {
                            "message": pleasehelp,
                            "operation_id": "170",
                            "response": pleasehelp,
                            "userText": usertext,
                            "title": pleasehelp,
                            "cat1": "Reminder",
                            "cat2": "HR",
                            "cat3": "Queries",
                            "cat4": "",
                            "video_path": "",
                            "project_name": "",
                            "ParameterTitle": "",
                            "action": "",
                            "orignalText": "",
                            "typetext": "HR",
                            "mainIssue": mainIssue,
                            "emailFlag": "",
                            "date": date,
                            "rem_type": rem_type
                        }

                    data1 = json.dumps(json_data, sort_keys=True, indent=4 * ' ')
                    data = data1
                    data2 = json.dumps(json_data,ensure_ascii=False)
                    dbInsertion(temtext, data2, "answered", username,userType, userID, "-1", mainIssue, "--", "-1")
                    resp = flask.Response(encrypt(data))
                    #resp = flask.Response(data)
                   #logger.info(f'{userID} [get] Response:' + str(json_data))
                    return resp

                else:
                    print("+_+_")
                    json_data = {
                            "message": pleasehelp,
                            "operation_id": "170",
                            "response": pleasehelp,
                            "userText": usertext,
                            "title": pleasehelp,
                            "cat1": "Reminder",
                            "cat2": "HR",
                            "cat3": "Queries",
                            "cat4": "",
                            "video_path": "",
                            "project_name": "",
                            "ParameterTitle": "",
                            "action": "",
                            "orignalText": "",
                            "typetext": "HR",
                            "mainIssue": mainIssue,
                            "emailFlag": "",
                            "date": today,
                            "rem_type": rem_type
                    }
                    data1 = json.dumps(json_data, sort_keys=True, indent=4 * ' ')
                    data = data1
                    data2 = json.dumps(json_data,ensure_ascii=False)
                    dbInsertion(temtext, data2, "answered", username,userType, userID, "-1", mainIssue, "--", "-1")
                    resp = flask.Response(encrypt(data))
                    #resp = flask.Response(data)
                   #logger.info(f'{userID} [get] Response:' + str(json_data))
                    return resp



    if "Apply for Leave(s)" in usertext:
            print("1")
            json_data = {
                "message": applyleave,
                "operation_id": "166",
                "response": applyleave,
                "userText": usertext,
                "title": applyleave,
                "cat1": "Leave",
                "cat2": "HR",
                "cat3": "Queries",
                "cat4": "",
                "video_path": "",
                "project_name": "",
                "ParameterTitle": "",
                "action": "",
                "orignalText": "",
                "typetext": "HR",
                "mainIssue": mainIssue,
                "emailFlag": ""
            }

            data1 = json.dumps(json_data, sort_keys=True, indent=4 * ' ')
            data = data1
            data2 = json.dumps(json_data,ensure_ascii=False)
            dbInsertion(temtext, data2, "answered", username,userType, userID, "-1", mainIssue, "--", "-1")
            resp = flask.Response(encrypt(data))
            #resp = flask.Response(data)
           #logger.info(f'{userID} [get] Response:' + str(json_data))
            return resp
    if "leave" in usertext.lower() and "approv" not in usertext.lower()\
                and "click" not in statusFlag \
                and "earn" not in usertext.lower() \
                and "compulsory" not in usertext.lower() \
                and "mandatory" not in usertext.lower() \
                and "maternity" not in usertext.lower() \
                and "saturday" not in usertext.lower() \
                and "compens" not in usertext.lower() \
                and "patern" not in usertext.lower() \
                and "parent" not in usertext.lower() \
                and "status" not in usertext.lower() \
                and "tus" not in usertext.lower() \
                and "cancel" not in usertext.lower()\
                and "comp" not in usertext.lower()\
                and "sat" not in usertext.lower() \
                and "balance" not in usertext.lower() \
                and "details" not in usertext.lower():

            ab = parse_multiple(usertext)
            print(ab)
            if len(ab) == 1:
                status = "Pending"
                approver_id = 1001
                approver_name = "Vikas Kedia"

                type = "Personal Leave"
                #from_date = datetime.strptime(str(ab[0].date()),"%Y-%m-%d").strftime("%d/%m/%Y")
                print("leave==", usertext)
                if ab[0].date().day <= 12 and not monthchk(usertext):
                    from_date = datetime.strptime(str(ab[0].date()), "%Y-%d-%m").strftime("%d/%m/%Y")
                else:
                    from_date = datetime.strptime(str(ab[0].date()), "%Y-%m-%d").strftime("%d/%m/%Y")
                print("from date====", from_date)
                a = insertLeave(userID, type, from_date, from_date, 1, status, approver_id, approver_name, username)
                send_email_attendance(username, type, from_date, from_date, 1, approver_name)
                if a == "somthing went wrong":
                    json_data = {"ParameterTitle": "", "action": "",
                                 "cat1": "HR related queries", "cat2": "HR",
                                 "cat3": "Queries", "cat4": "", "emailFlag": "",
                                 "mainIssue": "HR",
                                 "message": leaveerror, "operation_id": "",
                                 "orignalText": "", "project_name": "Service Request",
                                 "response": leaveerror,
                                 "title": "", "typetext": "Greetings", "userText": "",
                                 "video_path": ""}
                    data1 = json.dumps(json_data, sort_keys=True, indent=4 * ' ')
                    data = data1
                    data2 = json.dumps(json_data,ensure_ascii=False)
                    dbInsertion(temtext, data2, "answered", username,userType, userID, "-1", mainIssue, "--", "-1")
                    resp = flask.Response(encrypt(data))
                    #resp = flask.Response(data)

                   #logger.info(f'{userID} [get] Response:' + str(json_data))
                    return resp
                else:
                    message = "Your leave has been applied successfully. It has been forwarded to your Superior Mr. VIkas Kedia for approval."
                    if language_flag:
                        message = gettext(message,language)
                    json_data = {"ParameterTitle": "", "action": "",
                                 "cat1": "HR related queries", "cat2": "HR",
                                 "cat3": "Queries", "cat4": "", "emailFlag": "",
                                 "mainIssue": "HR",
                                 "message": message+"##C##", "operation_id": "",
                                 "orignalText": "", "project_name": "Service Request",
                                 "response": message+"##C##",
                                 "title": "", "typetext": "Greetings", "userText": "",
                                 "video_path": ""}
                    data1 = json.dumps(json_data, sort_keys=True, indent=4 * ' ')
                    data = data1
                    data2 = json.dumps(json_data,ensure_ascii=False)
                    dbInsertion(temtext, data2, "answered", username,userType, userID, "-1", mainIssue, "--", "-1")
                    resp = flask.Response(encrypt(data))
                    #resp = flask.Response(data)
                   #logger.info(f'{userID} [get] Response:' + str(json_data))
                    return resp
            elif len(ab) == 2:
                status = "Pending"
                approver_id = 1001
                approver_name = "Vikas Kedia"

                type = "Personal Leave"
                #from_date =datetime.strptime(str(ab[0].date()), "%Y-%m-%d").strftime("%d/%m/%Y")
                #to_date = datetime.strptime(str(ab[1].date()), "%Y-%m-%d").strftime("%d/%m/%Y")
                print("leave==",usertext)
                if ab[0].date().day <= 12 and not monthchk(usertext):
                    from_date = datetime.strptime(str(ab[0].date()), "%Y-%d-%m").strftime("%d/%m/%Y")
                    to_date = datetime.strptime(str(ab[1].date()), "%Y-%d-%m").strftime("%d/%m/%Y")
                else:
                    from_date = datetime.strptime(str(ab[0].date()), "%Y-%m-%d").strftime("%d/%m/%Y")
                    to_date = datetime.strptime(str(ab[1].date()), "%Y-%m-%d").strftime("%d/%m/%Y")

                print("==== from == ",from_date,"==to== ",to_date)
                date_format = "%d/%m/%Y"
                a = datetime.strptime(str(from_date), date_format)
                b = datetime.strptime(str(to_date), date_format)
                delta = b - a

                print(delta.days + 1)
                a = insertLeave(userID, type, from_date, to_date, delta.days + 1, status, approver_id, approver_name, username)
                send_email_attendance(username, type, from_date, to_date, delta.days + 1, approver_name)
                if a == "somthing went wrong":
                    json_data = {"ParameterTitle": "", "action": "",
                                 "cat1": "HR related queries", "cat2": "HR",
                                 "cat3": "Queries", "cat4": "", "emailFlag": "",
                                 "mainIssue": "HR",
                                 "message": leaveerror, "operation_id": "",
                                 "orignalText": "", "project_name": "Service Request",
                                 "response": leaveerror,
                                 "title": "", "typetext": "Greetings", "userText": "",
                                 "video_path": ""}
                    data1 = json.dumps(json_data, sort_keys=True, indent=4 * ' ')
                    data = data1
                    data2 = json.dumps(json_data,ensure_ascii=False)
                    dbInsertion(temtext, data2, "answered", username,userType, userID, "-1", mainIssue, "--", "-1")
                    resp = flask.Response(encrypt(data))
                    #resp = flask.Response(data)
                   #logger.info(f'{userID} [get] Response:' + str(json_data))
                    return resp
                else:
                    message = "Your leave has been applied successfully. It has been forwarded to your Superior Mr. VIkas Kedia for approval."
                    if language_flag:
                        message = gettext(message, language)
                    json_data = {"ParameterTitle": "", "action": "",
                                 "cat1": "HR related queries", "cat2": "HR",
                                 "cat3": "Queries", "cat4": "", "emailFlag": "",
                                 "mainIssue": "HR",
                                 "message": message+"##C##", "operation_id": "",
                                 "orignalText": "", "project_name": "Service Request",
                                 "response": message+"##C##",
                                 "title": "", "typetext": "Greetings", "userText": "",
                                 "video_path": ""}
                    data1 = json.dumps(json_data, sort_keys=True, indent=4 * ' ')
                    data = data1
                    data2 = json.dumps(json_data,ensure_ascii=False)
                    dbInsertion(temtext, data2, "answered", username,userType, userID, "-1", mainIssue, "--", "-1")
                    resp = flask.Response(encrypt(data))
                    #resp = flask.Response(data)
                   #logger.info(f'{userID} [get] Response:' + str(json_data))
                    return resp

                data1 = json.dumps(json_data, sort_keys=True, indent=4 * ' ')
                data = data1
                print("json data = ", data)
                data2 = json.dumps(json_data,ensure_ascii=False)
                dbInsertion(temtext, data2, "answered", username,userType, userID, "-1", mainIssue, "--", "-1")
                resp = flask.Response(encrypt(data))
                #resp = flask.Response(data)
               #logger.info(f'{userID} [get] Response:' + str(json_data))
                return resp

            elif len(ab) == 0 or len(ab)>=3:
                print("2")
                json_data = {
                    "message": applyleave,
                    "operation_id": "166",
                    "response": applyleave,
                    "userText": usertext,
                    "title": applyleave,
                    "cat1": "Leave",
                    "cat2": "HR",
                    "cat3": "Queries",
                    "cat4": "",
                    "video_path": "",
                    "project_name": "",
                    "ParameterTitle": "",
                    "action": "",
                    "orignalText": "",
                    "typetext": "HR",
                    "mainIssue": mainIssue,
                    "emailFlag": ""
                }
                data1 = json.dumps(json_data, sort_keys=True, indent=4 * ' ')
                data = data1
                data2 = json.dumps(json_data,ensure_ascii=False)
                dbInsertion(temtext, data2, "answered", username,userType, userID, "-1", mainIssue, "--", "-1")
                resp = flask.Response(encrypt(data))
                #resp = flask.Response(data)
               #logger.info(f'{userID} [get] Response:' + str(json_data))
                return resp

    if "approv" in usertext.lower() and "leave" in usertext.lower() :
            if userID == '1001':
                query = "select * from leave_detail where status = 'Pending' order by leave_id desc"
                output = create_query(query)

                tag_list = list(output)
                print(tag_list)

                json_array = []
                for t in tag_list:
                    dateapplied = str(t[6]).split('-')
                    date1 = str(dateapplied[2]) + "/" + str(dateapplied[1]) + "/" + str(dateapplied[0])
                    empName=t[10]
                    if "haris" in empName:
                        empName="Haris Shaikh"
                    if "pushpak" in empName:
                        empName="Pushpak Solanki"
                    if "vikas" in empName:
                        empName="Vikas Kedia"
                    status = t[7]
                    if "pprov" in status:
                        status="Approved"
                    if "eject" in status:
                        status="Rejected"
                    sim1 = {
                        "desc": t[2],
                        "title": t[2], "buttontext": "",
                        "imagepath": "",
                        "leave": t[2],
                        "from": t[3],
                        "to": t[4],
                        "status": status,
                        "applied_date": date1,
                        "no_of_days": t[5],
                        "approver_name": t[9],
                        "employee_name": empName,
                        "leave_id": t[0],
                        "redirectlink": "", "topright": "", "bottomtight": "",
                        "action": "", "message": "",
                        "ParameterTitle": ""}

                    json_array.append(sim1)
                if len(json_array) == 0:

                    json_data = {
                        "error": levpending,
                    }
                    data1 = json.dumps(json_data, sort_keys=True, indent=4 * ' ')
                    data = data1
                    data2 = json.dumps(json_data,ensure_ascii=False)
                    dbInsertion(temtext, data2, "answered", username,userType, userID, "-1", mainIssue, "--", "-1")
                    resp = flask.Response(encrypt(data))
                    #resp = flask.Response(data)
                   #logger.info(f'{userID} [get] Response:' + str(json_data))
                    return resp
                else:
                    message = "Leaves for Approval Approval"
                    if language_flag:
                        message = translate_text(message, language)
                    json_data = {
                        "message": message+"##formB##",
                        "title": message+"##formB##",
                        "ParameterTitle": "CarausialView",
                        "action": json_array}
                data1 = json.dumps(json_data, sort_keys=True, indent=4 * ' ')
                data = data1
                data2 = json.dumps(json_data,ensure_ascii=False)
                dbInsertion(temtext, data2, "answered", username,userType, userID, "-1", mainIssue, "--", "-1")
                resp = flask.Response(encrypt(data))
                #resp = flask.Response(data)
               #logger.info(f'{userID} [get] Response:' + str(json_data))
                return resp
            else:

                json_data = {
                    "error": levpending,
                }
                data1 = json.dumps(json_data, sort_keys=True, indent=4 * ' ')
                data = data1
                data2 = json.dumps(json_data,ensure_ascii=False)
                dbInsertion(temtext, data2, "answered", username,userType, userID, "-1", mainIssue, "--", "-1")
                resp = flask.Response(encrypt(data))
                #resp = flask.Response(data)

               #logger.info(f'{userID} [get] Response:' + str(json_data))
                return resp


    if main_op_id != None:
            print("in main_op_id iff")
            json_array = []
            query_data = create_query("select * from main_operations where main_op_id = '" + main_op_id + "' ")
            list_data = list(query_data)

            for ld in list_data:
                #print("ld================ ",ld)
                if language_flag:
                    if language == 'gu':
                        bot_resp = ld[11]
                    if language == 'hi':
                        bot_resp = ld[12]
                    if language == 'ml':
                        bot_resp = ld[13]
                    if language == 'mr':
                        bot_resp = ld[14]
                    if language == 'pa':
                        bot_resp = ld[15]
                    if language == 'ta':
                        bot_resp = ld[16]
                    if language == 'te':
                        bot_resp = ld[17]
                    if language == 'ur':
                        bot_resp = ld[18]
                else:
                    bot_resp = ld[7]
                if "|" in bot_resp:
                    sp_data = bot_resp.split("|")
                    for sp in sp_data:
                        if "$" in sp:
                            data = sp.split("$")
                            # print("id_op ",id_op)

                            sim = {
                                "title": data[0],
                                "desc": data[0],
                                "operation_id": "",
                                "main_op_id": data[1],
                                "message": "",
                                "buttontext": "",
                                "imagepath": "",
                                "redirectlink": "", "topright": "", "bottomtight": "",
                                "action": "",
                                "ParameterTitle": ""

                            }
                            json_array.append(sim)

                            json_data = {
                                "message":wldhappy,
                                "action": json_array,
                                "typetext": "HR",
                                "ParameterTitle": "ListView",
                                "mainIssue": "HR"
                            }
                        elif "#" in sp:
                            data = sp.split("#")
                            # print("id_op ",id_op)
                            sim = {
                                "title": data[0],
                                "desc": data[0],
                                "operation_id":  data[1],
                                "main_op_id":"",
                                "message": "",
                                "buttontext": "",
                                "imagepath": "",
                                "redirectlink": "", "topright": "", "bottomtight": "",
                                "action": "",
                                "ParameterTitle": ""

                            }
                            json_array.append(sim)

                            json_data = {
                                "message": wldhappy,
                                "action": json_array,
                                "typetext": "HR",
                                "ParameterTitle": "ListView",
                                "mainIssue": "HR"
                            }
                        else:
                            sim = {
                                "title": sp,
                                "desc": sp,
                                "operation_id":"" ,
                                "main_op_id": "",
                                "message": "",
                                "buttontext": "",
                                "imagepath": "",
                                "redirectlink": "", "topright": "", "bottomtight": "",
                                "action": "",
                                "ParameterTitle": ""

                            }
                            json_array.append(sim)

                            json_data = {
                                "message":  wldhappy,
                                "action": json_array,
                                "typetext": "HR",
                                "ParameterTitle": "ListView",
                                "mainIssue": "HR"
                            }


                    data = json.dumps(json_data)
                    data1 = json.dumps(json_data, ensure_ascii=False)
                    print("json data = ", data)
                    dbInsertion(temtext, data1, "answered", username,userType, userID, "-1", mainIssue, "HR", "-1")
                    resp = flask.Response(encrypt(data))
                    #resp = flask.Response(data)

                   #logger.info(f'{userID} [get] Response:' + str(json_data))
                    return resp

    if operation_id != None:
            print("operation_id iff")
            respon = "response"
            if language_flag:
                respon = language
            query_data = create_query("select "+respon+",heading from operations where operation_id = '" + str(operation_id) + "' ")
            #query_data = create_query("select response,heading from operations1 where operation_id = '" + str(operation_id) + "' ")
            print("res == ",query_data)



            bot_resp = query_data[0][0]
            headin = query_data[0][1]
            print(bot_resp)
            if language_flag:
                headin = translate_text(headin,language)
            if "|" in bot_resp and "#|#" not in bot_resp:
                sp_data = bot_resp.split("|")
                for sp in sp_data:
                    # if language_flag:
                        # sp = translate_text(sp,language)
                    sim = {
                        "title": sp,
                        "desc": sp,
                        "operation_id": "",
                        "main_op_id": "",
                        "message": "",
                        "buttontext": "",
                        "imagepath": "",
                        "redirectlink": "", "topright": "", "bottomtight": "",
                        "action": "",
                        "ParameterTitle": ""

                    }
                    json_array.append(sim)
                    json_data = {
                        "message": headin,
                        #"message": "",
                        "action": json_array,
                        "typetext": "HR",
                        "ParameterTitle": "ListView",
                        "mainIssue": "HR"
                    }
            else:
                print("+++++++++++++++++++++++++")
                print(bot_resp)
                bot_resp = bot_resp.replace("##LINK##", image_path_BAseURL)
                json_data = {
                        "ParameterTitle": "",
                        "action": "",
                        "cat1": "HR related queries",
                        "cat2": "HR",
                        "cat3": "Queries",
                        "cat4": "",
                        "emailFlag": "",
                        "mainIssue": mainIssue,
                        "message": bot_resp,
                        "operation_id": "",
                        "orignalText": "",
                        "project_name": "Service Request",
                        "response": bot_resp,
                        "title": temtext,
                        "typetext": "Greetings",
                        "userText": temtext,
                        "video_path": ""
                    }

            data = json.dumps(json_data)
            data1 = json.dumps(json_data,ensure_ascii=False)
            print("json data = ", data)
            dbInsertion(temtext, data1, "answered", username,userType, userID, "-1", mainIssue, "HR", "-1")
            resp = flask.Response(encrypt(data))
            #resp = flask.Response(data)

           #logger.info(f'{userID} [get] Response:' + str(json_data))
            return resp


    # else:
    #         print("op id is null")
    #         if str(statusFlag).lower() == "type":
    #             word_tokens = word_tokenize(usertext.lower())
    #             filtered_sentence = []
    #             for w in word_tokens:
    #                 w = spell(w.lower())
    #                 #w = lem.lemmatize(w, 'v')
    #                 # print("after spell check = ",w)
    #                 if w.lower() not in stop_words:
    #                     filtered_sentence.append(w)
    #
    #             usertext = " ".join(filtered_sentence)
    #             print("removing stopwords = ", usertext)

    print("abov txt")
        # condition for if after removing stopwords text becomes empty
    if usertext.lower() == "" and "where" not in temtext:
            print("inside 1")
            if "help" in str(temtext).lower():
                print("inside 2")
                json_data = {
                    "error": enterissue,
                    "operation_id": "",
                    "response": enterissue,
                    "userText": temtext,
                    "title": "",
                    "cat1": "Greeting",
                    "cat2": "",
                    "cat3": "",
                    "cat4": "",
                    "video_path": "",
                    "project_name": "",
                    "ParameterTitle": "",
                    "action": "",
                    "orignalText": "",
                    "typetext": "",
                    "mainIssue": mainIssue,
                    "emailFlag": ""



                }
                data1= json.dumps(json_data, ensure_ascii=False)
                data = json.dumps(json_data)
                print("json data = ", data)
                dbInsertion(temtext, data1, "answered", username,userType, userID, "-1", mainIssue, "Greetings", "-1")
                resp = flask.Response(encrypt(data))
                #resp = flask.Response(data)

               #logger.info(f'{userID} [get] Response:' + str(json_data))
                return resp

            # usertext is empty hence taking original text through temtext
            elif str(temtext).lower() in ["how are you", "how are you?", "how r you?", "how r you", "how r u", "how r u?",
                                          "hows u?"]:

                print("elif loop")
                json_data = {
                    "error": imfine,
                         "cat1": "Greetings",
                         "cat2": "",
                         "cat3": "",
                         "project_name": "",
                         "mainIssue": mainIssue

                }
                data = json.dumps(json_data)
                data1 = json.dumps(json_data, ensure_ascii=False)
                print("json data = ", data)
                dbInsertion(temtext, data1, "answered", username,userType, userID, "-1", mainIssue, "Greetings", "-1")
                resp = flask.Response(encrypt(data))
                #resp = flask.Response(data)

               #logger.info(f'{userID} [get] Response:' + str(json_data))
                return resp
            elif str(temtext).lower() in ["who are you","what is your name","who r u?","who are you?","who are u","whos this"]:
                print("inside 13")
                json_data = {
                    "error": imsupere,
                    "cat1": "Greetings",
                    "cat2": "",
                    "cat3": "",
                    "project_name": "",
                    "mainIssue": mainIssue

                }
                data = json.dumps(json_data)
                data1 = json.dumps(json_data, ensure_ascii=False)
                print("json data = ", data)
                dbInsertion(temtext, data1, "answered", username,userType, userID, "-1", mainIssue, "Greetings", "-1")
                resp = flask.Response(encrypt(data))
                #resp = flask.Response(data)

               #logger.info(f'{userID} [get] Response:' + str(json_data))
                return resp

            else:
                print("inside 21")
                json_data = {
                    "error": imsorry,
                    "operation_id": "",
                    "response": imsorry,
                    "userText": temtext,
                    "title": "",
                    "cat1": "Greeting",
                    "cat2": "",
                    "cat3": "",
                    "cat4": "",
                    "video_path": "",
                    "project_name": "",
                    "ParameterTitle": "",
                    "action": "",
                    "orignalText": "",
                    "typetext": "",
                    "mainIssue": mainIssue,
                    "emailFlag": ""


                }
                # print("else",type(json_data))
                print("json",json_data)
                data = json.dumps(json_data)
                data1 = json.dumps(json_data, ensure_ascii=False)
                print("json data = ", data)
                dbInsertion(temtext, data1, "unanswered", username,userType, userID, "-1", mainIssue, "Greetings", "-1")
                resp = flask.Response(encrypt(data))
                #resp = flask.Response(data)

               #logger.info(f'{userID} [get] Response:' + str(json_data))
                return (resp)



    elif str(temtext).lower() in ["how are you", "how are you?", "how r you?", "how r you", "how r u", "how r u?",
                                    "hows u?"]:
            # print("taking OG text")
            print("inside 5")
            json_data = {
                         "error": imfine,
                         "cat1": "Greetings",
                         "cat2": "",
                         "cat3": "",
                         "project_name": "",
                         "mainIssue": mainIssue

                         }
            data = json.dumps(json_data)
            data1 = json.dumps(json_data, ensure_ascii=False)
            print("json data = ", data)
            dbInsertion(temtext, data1, "answered", username,userType, userID, "-1", mainIssue, "Greetings", "-1")
            resp = flask.Response(encrypt(data))
            #resp = flask.Response(data)

           #logger.info(f'{userID} [get] Response:' + str(json_data))
            return resp

    if str(temtext).lower() in ["need help", "help me", "want help", "having issue", "i am having issue",
                                    "how to resolve issue", "need help to resolve issue",
                                    "i need help", "i want help", "can you help", "i am having problem", "problem", "resolve my issue",
                                    "need solution",
                                    "i need solution", "solution", "incident", "i am having incident", "i have incident",
                                    "have incident",
                                    "please help", "please help me", "help me please", "pls help", "help pls",
                                    "can u pls help me", "can you pls help me"
            , "pls me", "can you please help me"]:
            json_data = {
                "error": enterissue,
                "operation_id": "",
                "response": enterissue,
                "userText": temtext,
                "title": "",
                "cat1": "Greeting",
                "cat2": "",
                "cat3": "",
                "cat4": "",
                "video_path": "",
                "project_name": "",
                "ParameterTitle": "",
                "action": "",
                "orignalText": "",
                "typetext": "",
                "mainIssue": mainIssue,
                "emailFlag": ""
            }

            data = json.dumps(json_data)
            data1 = json.dumps(json_data, ensure_ascii=False)
            print("json data = ", data)
            dbInsertion(temtext, data1, "answered", username,userType, userID, "-1", mainIssue, "Greetings", "-1")
            resp = flask.Response(encrypt(data))
            #resp = flask.Response(data)

           #logger.info(f'{userID} [get] Response:' + str(json_data))
            return resp

    # taking response fromimsorry bot
    if usertext == "":
        usertext = temtext
    print("Origional Usertext ====> ", usertext)
    bot_resp = english_bot.get_response(usertext)
    #print(bot_resp)
    bot_confidence = bot_resp.confidence
    print("Confidence = ", bot_confidence)
    print("Response ====> ", bot_resp)
    bot_data = str(bot_resp)
    flag = False
    matchText = ""
    thirdvar = ""

    if '**' in bot_data:
        if language_flag:
            m = translate_text( bot_data[:-3],language)
        json_data = {

            "error": m,
                "cat1": "Greetings",
                "cat2": "",
                "cat3": "",
                "project_name": "",
                "mainIssue": mainIssue
        }
        data = json.dumps(json_data)
        data1 = json.dumps(json_data, ensure_ascii=False)
        print("json data = ", data)
        dbInsertion(temtext, data1, "answered", username,userType, userID, "-1", mainIssue, "Greetings", "-1")
        resp = flask.Response(encrypt(data))
        #resp = flask.Response(data)

       #logger.info(f'{userID} [get] Response:' + str(json_data))
        return resp


    elif '|' in bot_data:  # pipe separation
        print("| separation")
        matchText = bot_data.split("|")[1]  # to fetch text atching to usertext from data
        sp = bot_data.split("|")
        if len(sp) > 2:
            thirdvar = bot_data.split("|")[2]  # to fetch words like HR,Admin,Technology
        userTextSplit = usertext.split(" ")
        matchTextSplit = matchText.split(" ")
        usertext = ""

        for text in userTextSplit:
            for match in matchTextSplit:
                if fuzz.ratio(text.lower().strip(), match.lower().strip()) > 50:
                    if text.lower() != "" and match.lower() != "":
                        if text not in usertext:
                            usertext += " " + text
                        if fuzz.ratio(text.lower().strip(), match.lower().strip()) == 100:
                            flag = True
                            break
        fuzzymatch = fuzz.ratio(usertext.lower(), matchText.lower())
        print("fuzzymatch = ", fuzzymatch)

        if bot_confidence > 0.80:
            flag = True
        elif fuzzymatch > 80:
            flag = True
        else:
            flag = False

        bot_data = bot_data.split("|")[0]  # to fetch sql query from response
        bot_data = str(bot_data)
        print("Response with sql query ==> ",bot_data)            # displaying response of sql query

    elif "apply leave" in bot_data:
        print("3")
        json_data = {
            "message": applyleave,
            "operation_id": "166",
            "response": applyleave,
            "userText": usertext,
            "title": applyleave,
            "cat1": "Leave",
            "cat2": "HR",
            "cat3": "Queries",
            "cat4": "",
            "video_path": "",
            "project_name": "",
            "ParameterTitle": "",
            "action": "",
            "orignalText": "",
            "typetext": "HR",
            "mainIssue": mainIssue,
            "emailFlag": ""
        }


        data1 = json.dumps(json_data, sort_keys=True, indent=4 * ' ')
        data = data1
        data2 = json.dumps(json_data, ensure_ascii=False)
        dbInsertion(temtext, data2, "answered", username,userType, userID, "-1", mainIssue, "--", "-1")
        resp = flask.Response(encrypt(data))
        #resp = flask.Response(data)

       #logger.info(f'{userID} [get] Response:' + str(json_data))
        return resp

    elif "reminder form" in bot_data:
        today = datetime.now().strftime("%d-%m-%Y")
        time = datetime.now().strftime("%I:%M %p")
        json_data = {
            "message": pleasehelp,
            "operation_id": "170",
            "response": pleasehelp,
            "userText": usertext,
            "title": pleasehelp,
            "cat1": "Reminder",
            "cat2": "HR",
            "cat3": "Queries",
            "cat4": "",
            "video_path": "",
            "project_name": "",
            "ParameterTitle": "",
            "action": "",
            "orignalText": "",
            "typetext": "HR",
            "mainIssue": mainIssue,
            "emailFlag": "",
            "date":today,
            "time":time
        }

        data1 = json.dumps(json_data, sort_keys=True, indent=4 * ' ')
        data = data1
        data2 = json.dumps(json_data, ensure_ascii=False)
        dbInsertion(temtext, data2, "answered", username,userType, userID, "-1", mainIssue, "--", "-1")
        resp = flask.Response(encrypt(data))
        #resp = flask.Response(data)
       #logger.info(f'{userID} [get] Response:' + str(json_data))
        return resp
    elif "approve leaves" in bot_data:
        print()
        if userID == '1001':
            query = "select * from leave_detail where status = 'Pending'  order by leave_id desc"
            output = create_query(query)

            tag_list = list(output)
            print(tag_list)

            json_array = []
            for t in tag_list:
                dateapplied = str(t[6]).split('-')
                date1 = str(dateapplied[2]) + "/" + str(dateapplied[1]) + "/" + str(dateapplied[0])
                empName = t[10]
                if "haris" in empName:
                    empName="Haris Shaikh"
                if "pushpak" in empName:
                    empName="Pushpak Solanki"
                if "vikas" in empName:
                    empName="Vikas Kedia"
                status = t[7]
                if "pprov" in status:
                    status="Approved"
                if "eject" in status:
                    status="Rejected"
                sim1 = {
                    "desc": t[2],
                    "title": t[2], "buttontext": "",
                    "imagepath": "",
                    "leave": t[2],
                    "from": t[3],
                    "to": t[4],
                    "status": status,
                    "applied_date": date1,
                    "no_of_days": t[5],
                    "approver_name": t[9],
                    "employee_name": empName,
                    "leave_id": t[0],
                    "redirectlink": "", "topright": "", "bottomtight": "",
                    "action": "", "message": "",
                    "ParameterTitle": ""}

                json_array.append(sim1)

            json_data = {
                "message": "Leaves for Approval",
                "ParameterTitle": "CarausialView",
                "action": json_array}
            data1 = json.dumps(json_data, sort_keys=True, indent=4 * ' ')
            data = data1
            data2 = json.dumps(json_data, ensure_ascii=False)
            dbInsertion(temtext, data2, "answered", username,userType, userID, "-1", mainIssue, "--", "-1")
            resp = flask.Response(encrypt(data))
            #resp = flask.Response(data)

           #logger.info(f'{userID} [get] Response:' + str(json_data))
            return resp
        else:
            json_data = {
                "message": levpending,
                "ParameterTitle": "",
                "action": ""}
            data1 = json.dumps(json_data, sort_keys=True, indent=4 * ' ')
            data = data1
            data2 = json.dumps(json_data, ensure_ascii=False)
            dbInsertion(temtext, data2, "answered", username,userType, userID, "-1", mainIssue, "--", "-1")
            resp = flask.Response(encrypt(data))
            #resp = flask.Response(data)

           #logger.info(f'{userID} [get] Response:' + str(json_data))
            return resp

    elif "leave details" in bot_data:
        leavedetail = "Here are the details of your Applied Leaves"
        if language_flag:
            leavedetail = gettext(leavedetail, language)

        leaveid = "No leaves for your ID yet."
        if language_flag:
            leaveid = gettext(leaveid, language)
        query = "select * from leave_detail where emp_id = '"+userID+"'  order by leave_id desc"
        output = create_query(query)
        print(output)

        tag_list = list(output)
        print(tag_list)

        json_array = []
        if len(tag_list) >0:
            for t in tag_list:
                    print(t[6])
                    dateapplied = str(t[6]).split('-')
                    date1 = str(dateapplied[2])+"/"+str(dateapplied[1])+"/"+str(dateapplied[0])
                    empName = t[10]
                    if "haris" in empName:
                        empName = "Haris Shaikh"
                    if "pushpak" in empName:
                        empName = "Pushpak Solanki"
                    if "vikas" in empName:
                        empName = "Vikas Kedia"
                    status = t[7]
                    if "pprov" in status:
                        status = "Approved"
                    if "eject" in status:
                        status = "Rejected"
                    sim1 = {
                        "desc": t[2],
                        "title": t[2], "buttontext": "",
                        "imagepath": "",
                        "leave": t[2],
                        "from": t[3],
                        "to": t[4],
                        "status": status,
                        "applied_date":date1,
                        "no_of_days":t[5],
                        "approver_name":t[9],
                        "employee_name": empName,
                        "leave_id": t[0],
                        "redirectlink": "", "topright": "", "bottomtight": "",
                        "action": "", "message": "",
                        "ParameterTitle": ""}

                    json_array.append(sim1)

            json_data = {
                "message": leavedetail,
                "ParameterTitle": "CarausialView",
                "action": json_array}
        else:
            json_data = {
                "error": leaveid,
                }
        data1 = json.dumps(json_data, sort_keys=True, indent=4 * ' ')
        data = data1
        data2 = json.dumps(json_data, ensure_ascii=False)
        dbInsertion(temtext, data2, "answered", username,userType, userID, "-1", mainIssue, "--", "-1")
        resp = flask.Response(encrypt(data))
        #resp = flask.Response(data)

       #logger.info(f'{userID} [get] Response:' + str(json_data))
        return resp

    elif "document" in bot_data:
        document_msg = "You have the below mentioned Document(s) by the Company Admin"
        # if language_flag:
        #     document_msg = gettext(document_msg, language_flag)
        # currentdate = datetime.now().strftime("%Y-%m-%d")
        # query = "select * from reminder_detail where date = '" + currentdate + "' and emp_id = '" + userID+ "' order by time"
        query = "select * from manage_document where doc_status='Active' order by doc_id desc "
        output = create_query(query)
        print(output)

        tag_list = list(output)
        print(tag_list)

        json_array = []

        for t in tag_list:
            if t[3] != "":
                fl = str(t[3]).split(".")[1]
                file_type = categorize(fl.lower())
                path = BasePathDocumnets + str(t[3])
            else:
                fl = ""
                path = ""
                file_type = ""

            sim1 = {
                "desc": t[1],
                "title": t[1], "buttontext": "",
                "imagepath": "",
                "description": t[2],
                "sender_name": t[4],
                "attachment_path": path,
                "file_type": file_type,
                "date": chFormat(str(t[6])),
                "redirectlink": "", "topright": "", "bottomtight": "",
                "action": "", "message": "",
                "ParameterTitle": ""}
            json_array.append(sim1)

        json_data = {
            "message": document_msg,
            "ParameterTitle": "CarausialView",
            "ParameterType": "Notification",
            "action": json_array}
        data1 = json.dumps(json_data, sort_keys=True, indent=4 * ' ')
        data = data1
        data2 = json.dumps(json_data, ensure_ascii=False)
        dbInsertion(temtext, data2, "answered", username, userType, userID, "-1", mainIssue, "--", "-1")
        print(data)
        # resp = flask.Response(data)
        resp = flask.Response(encrypt(data))
        return resp

    elif "notify" in bot_data:
        notify = "You have the below mentioned Notification(s) by the Company Admin"
        # if language_flag:
        #     notify = gettext(notify, language_flag)
        # currentdate = datetime.now().strftime("%Y-%m-%d")
        # query = "select * from reminder_detail where date = '" + currentdate + "' and emp_id = '" + userID+ "' order by time"
        query = "select * from notify order by notification_id desc "
        output = create_query(query)
        print(output)

        tag_list = list(output)
        print(tag_list)

        json_array = []

        for t in tag_list:
            if t[7] != "":
                fl = str(t[7]).split(".")[1]
                file_type = categorize(fl.lower())
                path = BasePathAttachment + str(t[7])
            else:
                fl = ""
                path = ""
                file_type = ""

            sim1 = {
                "desc": t[1],
                "title": t[1], "buttontext": "",
                "imagepath": "",
                "description": t[2],
                "sender_name": t[3],
                "attachment_path": path,
                "file_type": file_type,
                "date": chFormat(str(t[5])),
                "redirectlink": "", "topright": "", "bottomtight": "",
                "action": "", "message": "",
                "ParameterTitle": ""}
            json_array.append(sim1)

        json_data = {
            "message": notify,
            "ParameterTitle": "CarausialView",
            "ParameterType": "Notification",
            "action": json_array}
        data1 = json.dumps(json_data, sort_keys=True, indent=4 * ' ')
        data = data1
        data2 = json.dumps(json_data, ensure_ascii=False)
        dbInsertion(temtext, data2, "answered", username, userType, userID, "-1", mainIssue, "--", "-1")
        print(data)
        # resp = flask.Response(data)
        resp = flask.Response(encrypt(data))
        return resp

    elif bot_data == "show ticket":
        try:
            json_array = []

            url = 'https://mgenius.in/ITSMTool/Service/find'
            headers = {"Accept": "application/json",
                       "Content-Type": "application/json",
                       "int-log-id": "qwertyasdfg",
                       "key": "2fb29d27-51a9-4074-82f5-45db3f450d24",
                       "token": "7560a221-28b3-4343-8848-2388fe788d51",
                       "Cache-Control": "no-cache"}
            data = {
                "project": {
                    "name": "Incident Management"
                },
                "pageNumber": 1,
                "pageSize": 100,
                "ticketState": "ALL",
                "submittedBy": userID
            }
            data = json.dumps(data)
            print("Incident data:", data)
            ticketjson = requests.post(url, data=data, headers=headers, verify=False)
            print("Jsonrequest:", ticketjson)
            Ticketsdata = json.loads(ticketjson.text)
            print('INC tic data---> ', Ticketsdata)
            ticket_details = Ticketsdata["tickets"]
            tick_length = len(ticket_details)
            # print("Tickets-Incident",tick_length)

            if tick_length > 0:
                ticketflag = True
            else:
                ticketflag = False

            url = 'https://mgenius.in/ITSMTool/Service/find'
            headers = {"Accept": "application/json",
                       "Content-Type": "application/json",
                       "int-log-id": "qwertyasdfg",
                       "key": "2fb29d27-51a9-4074-82f5-45db3f450d24",
                       "token": "7560a221-28b3-4343-8848-2388fe788d51",
                       "Cache-Control": "no-cache"}
            data = {
                "project": {
                    "name": "Service Request"
                },
                "pageNumber": 1,
                "pageSize": 100,
                "ticketState": "ALL",
                "submittedBy": userID
            }
            data = json.dumps(data)
            print("Service Request:", data)
            ticketjson1 = requests.post(url, data=data, headers=headers, verify=False)
            print("SR-Json", ticketjson1)
            Ticketsdata1 = json.loads(ticketjson1.text)
            print('SR tic data---> ', Ticketsdata1)
            ticket_details_incident = Ticketsdata1["tickets"]
            tick_length1 = len(ticket_details_incident)
            # print("Tickets-Service", tick_length1)

            if tick_length1 > 0:
                ticketflag = True
            else:
                ticketflag = False

            if ticketflag == True:

                ticket_details.extend(ticket_details_incident)
                ticket_details.sort(key=myFunc, reverse=True)
                print("show tic details---> ", ticket_details)
                count = 1
                for j in ticket_details:
                    if count < 11:
                        count = count + 1
                        ticketid = j["refId"]
                        status = j["currentState"]
                        ticket_description = j["probDescription"]
                        ticket_title = j["title"]

                        Ticket_Logged_Date1 = j["creationTime"]
                        Ticket_Logged_Date = datetime.strptime(str(Ticket_Logged_Date1),
                                                                     "%m/%d/%Y %I:%M:%S %p").strftime("%d/%m/%Y %I:%M:%S %p")
                        # ms = int(Ticket_Logged_Date)
                        # Ticket_creation_Date = datetime.fromtimestamp(ms / 1000.0)
                        # print(Ticket_creation_Date)
                        # onlycreationdate = Ticket_creation_Date.date()
                        # print("onlydate", onlycreationdate)
                        # Ticket_Logged_Date_final = datetime.strptime(str(Ticket_creation_Date),
                        #                                              "%Y-%m-%d %H:%M:%S").strftime(
                        #     "%d %B, %Y %H:%M:%S")
                        # print(Ticket_Logged_Date_final)

                        Ticket_resolve_Date_final = ""
                        if "Closed" in status:
                            ticket_resolved_Date1 = j["lastOperatedTime"]
                            ticket_resolved_Date = datetime.strptime(str(ticket_resolved_Date1),
                                                                     "%m/%d/%Y %I:%M:%S %p").strftime(
                                "%d/%m/%Y %I:%M:%S %p")
                            # ms1 = int(ticket_resolved_Date)
                            # ticket_resolved_Date1 = datetime.fromtimestamp(ms1 / 1000.0)
                            # print(ticket_resolved_Date1)
                            # # onlyresolveddate = ticket_resolved_Date1.date()
                            # # print("onlydate", onlyresolveddate)
                            # Ticket_resolve_Date_final = datetime.strptime(str(ticket_resolved_Date1),
                            #                                               "%Y-%m-%d %H:%M:%S").strftime(
                            #     "%d %B, %Y %H:%M:%S")
                            # print(Ticket_resolve_Date_final)
                        else:
                            pass

                        if len(Ticket_resolve_Date_final) > 0:
                            sim = {
                                "Ticketid": ticketid,
                                "status": status,
                                "Ticket_creation_Date": Ticket_Logged_Date,
                                "Ticket_resolved_Date": ticket_resolved_Date,
                                "ticket_description": ticket_description,
                                "title": "", "buttontext": "",
                                "imagepath": "",
                                "redirectlink": "", "topright": "", "bottomtight": "",
                                "action": "", "message": "",
                                "ParameterTitle": ""}
                            json_array.append(sim)
                            count = count
                        else:
                            sim = {
                                "Ticketid": ticketid,
                                "status": status,
                                "Ticket_creation_Date": Ticket_Logged_Date,
                                "ticket_description": ticket_description,
                                "title": "", "buttontext": "",
                                "imagepath": "",
                                "redirectlink": "", "topright": "", "bottomtight": "",
                                "action": "", "message": "",
                                "ParameterTitle": ""}
                            json_array.append(sim)
                            count = count

                    else:
                        break

                json_data = {
                    "message": "Ticket Status",
                    "ParameterTitle": "CarausialView",
                    "ParameterType": "TicketStatusView",
                    "action": json_array,
                    "resolve": "",
                    "rating": "no",
                    "mainIssue": mainIssue
                }
                data1 = json.dumps(json_data, sort_keys=True, indent=4 * ' ')
                data = data1
                data2 = json.dumps(json_data)
                print("show tic in if ---->", data2)
                dbInsertion(temtext, data2, "query", username, userType, userID, "-1", mainIssue, "Technology",
                            "-1")
                resp = flask.Response(encrypt(str(data)))
                resp.headers['Access-Control-Allow-Origin'] = '*'
                logger.info(f'{userID} [get] Response:' + str(json_data))
                return resp
            else:
                json_data = {
                    "message": "No Tickets are found",
                    "ParameterTitle": "",
                    "action": "",
                    "resolve": "",
                    "rating": "no",
                    "title": "",
                    "mainIssue": mainIssue,
                    "response": "No Tickets are found"
                }

                data1 = json.dumps(json_data, sort_keys=True, indent=4 * ' ')
                data = data1
                data2 = json.dumps(json_data)
                print("show tic in else ---->", data2)
                dbInsertion(temtext, data2, "query", username, userType, userID, "-1", mainIssue, "Technology", "-1")
                resp = flask.Response(encrypt(str(data)))
                resp.headers['Access-Control-Allow-Origin'] = '*'
                logger.info(f'{userID} [get] Response:' + str(json_data))
                return resp

        except Exception as e:
            json_data = {
                "message": "No Tickets are found",
                "ParameterTitle": "",
                "action": "",
                "resolve": "",
                "rating": "no",
                "title": "",
                "mainIssue": mainIssue,
                "response": "No Tickets are found"
            }
            data1 = json.dumps(json_data, sort_keys=True, indent=4 * ' ')
            data = data1
            data2 = json.dumps(json_data)
            print("show tic  ---->", data2)
            print(e)
            dbInsertion(temtext, data2, "query", username, userType, userID, "-1", mainIssue, "--", "-1")

            resp = flask.Response(encrypt(str(data)))
            resp.headers['Access-Control-Allow-Origin'] = '*'
            logger.info(f'{userID} [get] Response:' + str(json_data))
            return resp

    elif bot_data == "ticket":
        print("from yml tic text1 ==  ", text1)
        Ticket = ""
        # print("text1 ==  ",text1)
        if hasNumbers(text1):
            tempText = re.search(r'\d+', text1).group()
        if "sr-" in text1.lower():
            Ticket = "||SR-" + str(tempText)
        elif "inc-" in text1.lower():
            Ticket = "||INC-" + str(tempText)
        else:
            print("no numbers")

        # print(Ticket)

        json_data = {
            "message": "Please enter Ticket ID" + Ticket,
            "ParameterTitle": "Please enter Ticket ID" + Ticket,
            "action": "",
            "action1": "getTicStatus",
            "mainIssue": mainIssue}

        data1 = json.dumps(json_data, sort_keys=True, indent=4 * ' ')
        data = data1
        data2 = json.dumps(json_data)
        dbInsertion(temtext, data2, "query", username, userType, userID, "-1", mainIssue, "--", "-1")
        resp = flask.Response(encrypt(str(data)))
        resp.headers['Access-Control-Allow-Origin'] = '*'
        logger.info(f'{userID} [get] Response:' + str(json_data))
        return resp


    elif "today" in bot_data:
            remindertoday = "Here are the details of your Reminders for Today"
            if language_flag:
                remindertoday = gettext(remindertoday, language)

            noremindertoday = "No Reminders for today."
            if language_flag:
                noremindertoday = gettext(noremindertoday, language)
            currentdate = datetime.now().strftime("%Y-%m-%d")
            print("today==",currentdate)

            query = "select * from reminder_detail where date = '" + currentdate + "' and emp_id = '" + userID + "' "
            output = create_query(query)
            tags_data = list(output)
            print(tags_data)
            if len(tags_data) > 0:
                json_array = []
                for t in tags_data:
                    sim1 = {
                        "Rem_desc": t[4],
                        "Rem_title": t[3], "buttontext": "",
                        "imagepath": "",
                        "Rem_type": t[3],
                        "Rem_date":chFormat(str(t[5])),
                        "Rem_time": t[6],
                        "status": "",
                        "Rem_set_date": t[9],
                        "no_of_days": "",
                        "name": t[2],
                        "redirectlink": "", "topright": "", "bottomtight": "",
                        "action": "", "message": "",
                        "ParameterTitle": ""}

                    json_array.append(sim1)

                json_data = {
                    "message": remindertoday,
                    "ParameterTitle": "CarausialView",
                    "ParameterType": "ReminderView",
                    "action": json_array}
                data1 = json.dumps(json_data, sort_keys=True, indent=4 * ' ')
                data = data1
                data2 = json.dumps(json_data, ensure_ascii=False)
                dbInsertion(temtext, data2, "answered", username,userType, userID, "-1", mainIssue, "--", "-1")
                #resp = flask.Response(data)
                resp = flask.Response(encrypt(data))
               #logger.info(f'{userID} [get] Response:' + str(json_data))
                return resp

            else:
                json_data = {
                    "error": noremindertoday,
                }
            data1 = json.dumps(json_data, sort_keys=True, indent=4 * ' ')
            data = data1
            data2 = json.dumps(json_data, ensure_ascii=False)
            dbInsertion(temtext, data2, "answered", username,userType, userID, "-1", mainIssue, "--", "-1")
            resp = flask.Response(encrypt(data))
            #resp = flask.Response(data)

           #logger.info(f'{userID} [get] Response:' + str(json_data))
            return resp

    elif "tomorrow" in bot_data:


        remindertommo = "Here are the details of your Reminders for Tommorow"
        if language_flag:
            remindertommo = gettext(remindertommo, language)

        noremindertomm = "No Reminders for Tommorow."
        if language_flag:
            noremindertomm = gettext(noremindertomm, language)
        currentdate = datetime.now()
        tom_date = (currentdate + timedelta(days = 1)).strftime("%Y-%m-%d")
        print("tom date == ",tom_date)

        query = "select * from reminder_detail where date = '" + tom_date +"' and emp_id = '" + userID + "' "
        output = create_query(query)
        tags_data = list(output)
        print(tags_data)
        if len(tags_data)>0:
            json_array = []
            for t in tags_data:
                sim1 = {
                    "Rem_desc": t[4],
                    "Rem_title": t[3], "buttontext": "",
                    "imagepath": "",
                    "Rem_type": t[3],
                    "Rem_date": chFormat(str(t[5])),
                    "Rem_time": t[6],
                    "status": "",
                    "Rem_set_date": t[9],
                    "no_of_days": "",
                    "name": t[2],
                    "redirectlink": "", "topright": "", "bottomtight": "",
                    "action": "", "message": "",
                    "ParameterTitle": ""}

                json_array.append(sim1)

            json_data = {
                "message": remindertommo,
                "ParameterTitle": "CarausialView",
                "ParameterType": "ReminderView",
                "action": json_array}
            data1 = json.dumps(json_data, sort_keys=True, indent=4 * ' ')
            data = data1
            data2 = json.dumps(json_data, ensure_ascii=False)
            dbInsertion(temtext, data2, "answered", username,userType, userID, "-1", mainIssue, "--", "-1")
            #resp = flask.Response(data)
            resp = flask.Response(encrypt(data))
           #logger.info(f'{userID} [get] Response:' + str(json_data))
            return resp

        else:
            json_data = {
                "error": noremindertomm,
            }
        data1 = json.dumps(json_data, sort_keys=True, indent=4 * ' ')
        data = data1
        data2 = json.dumps(json_data, ensure_ascii=False)
        dbInsertion(temtext, data2, "answered", username,userType, userID, "-1", mainIssue, "--", "-1")
        resp = flask.Response(encrypt(data))
        #resp = flask.Response(data)
       #logger.info(f'{userID} [get] Response:' + str(json_data))
        return resp

    elif "week" in bot_data:


        reminderweek = "Here are the details of your Reminders for this Week"
        if language_flag:
            reminderweek = gettext(reminderweek, language)

        noreminderweek = "No Reminders for this Week."
        if language_flag:
            noreminderweek = gettext(noreminderweek, language)
        today = datetime.now().date()
        day = datetime.now().strftime("%Y-%m-%d")
        st = today - timedelta(days=today.weekday())
        start = st.strftime("%Y-%m-%d")
        end = (st + timedelta(days=6)).strftime("%Y-%m-%d")
        print("start==",start,"   end==",end)

        query = "select * from reminder_detail where date between '" + day + "' and '" + end + "' and emp_id = '" + userID + "' order by date"
        output = create_query(query)
        tags_data = list(output)
        print(tags_data)
        if len(tags_data) > 0:
            json_array = []
            for t in tags_data:
                sim1 = {
                    "Rem_desc": t[4],
                    "Rem_title": t[3], "buttontext": "",
                    "imagepath": "",
                    "Rem_type": t[3],
                    "Rem_date": chFormat(str(t[5])),
                    "Rem_time": t[6],
                    "status": "",
                    "Rem_set_date": t[9],
                    "no_of_days": "",
                    "name": t[2],
                    "redirectlink": "", "topright": "", "bottomtight": "",
                    "action": "", "message": "",
                    "ParameterTitle": ""}

                json_array.append(sim1)

            json_data = {
                "message": reminderweek,
                "ParameterTitle": "CarausialView",
                "ParameterType": "ReminderView",
                "action": json_array}
            data1 = json.dumps(json_data, sort_keys=True, indent=4 * ' ')
            data = data1
            data2 = json.dumps(json_data, ensure_ascii=False)
            dbInsertion(temtext, data2, "answered", username,userType, userID, "-1", mainIssue, "--", "-1")
            #resp = flask.Response(data)
            resp = flask.Response(encrypt(data))
           #logger.info(f'{userID} [get] Response:' + str(json_data))
            return resp

        else:
            json_data = {
                "error": noreminderweek,
            }
        data1 = json.dumps(json_data, sort_keys=True, indent=4 * ' ')
        data = data1
        data2 = json.dumps(json_data, ensure_ascii=False)
        dbInsertion(temtext, data2, "answered", username,userType, userID, "-1", mainIssue, "--", "-1")
        resp = flask.Response(encrypt(data))
        #resp = flask.Response(data)
       #logger.info(f'{userID} [get] Response:' + str(json_data))
        return resp

    elif "month" in bot_data:


        remindermonth = "Here are the details of your Reminders for this Month"
        if language_flag:
            remindermonth = gettext(remindermonth, language)

        noremindermonth = "No Reminders for this Month."
        if language_flag:
            noremindermonth = gettext(noremindermonth, language)
        today = datetime.now().date()
        day = datetime.now().strftime("%Y-%m-%d")
        month = today.month
        year = today.year
        if month < 10:
            month = "0" + str(month)
        print("month=", month, ", year=", year)
        query = "SELECT * FROM `reminder_detail` WHERE date  LIKE '" + str(year) + "-" + str(month) + "-%' and emp_id = '" + userID + "' and date >= '" + day +"' order by date"
        output = create_query(query)
        tags_data = list(output)
        print(tags_data)
        if len(tags_data) > 0:
            json_array = []
            for t in tags_data:
                sim1 = {
                    "Rem_desc": t[4],
                    "Rem_title": t[3], "buttontext": "",
                    "imagepath": "",
                    "Rem_type": t[3],
                    "Rem_date": chFormat(str(t[5])),
                    "Rem_time": t[6],
                    "status": "",
                    "Rem_set_date": t[9],
                    "no_of_days": "",
                    "name": t[2],
                    "redirectlink": "", "topright": "", "bottomtight": "",
                    "action": "", "message": "",
                    "ParameterTitle": ""}

                json_array.append(sim1)

            json_data = {
                "message": remindermonth,
                "ParameterTitle": "CarausialView",
                "ParameterType": "ReminderView",
                "action": json_array}
            data1 = json.dumps(json_data, sort_keys=True, indent=4 * ' ')
            data = data1
            data2 = json.dumps(json_data, ensure_ascii=False)
            dbInsertion(temtext, data2, "answered", username,userType, userID, "-1", mainIssue, "--", "-1")
            #resp = flask.Response(data)
            resp = flask.Response(encrypt(data))
           #logger.info(f'{userID} [get] Response:' + str(json_data))
            return resp

        else:
            json_data = {
                "error": noremindermonth,
            }
        data1 = json.dumps(json_data, sort_keys=True, indent=4 * ' ')
        data = data1
        data2 = json.dumps(json_data, ensure_ascii=False)
        dbInsertion(temtext, data2, "answered", username,userType, userID, "-1", mainIssue, "--", "-1")
        resp = flask.Response(encrypt(data))
        #resp = flask.Response(data)
       #logger.info(f'{userID} [get] Response:' + str(json_data))
        return resp


    elif "all" in bot_data:
        reminder1 = "Here are the details of your Reminders"
        if language_flag:
            reminder1 = gettext(reminder1, language)

        noreminder1 = "No Reminders for your ID yet"
        if language_flag:
            noreminder1 = gettext(noreminder1, language)
        day = datetime.now().strftime("%Y-%m-%d")
        query = "select * from `reminder_detail` where emp_id = '" + userID + "' and date >= '" + day +"' order by date"
        output = create_query(query)
        print(output)

        tags_data = list(output)
        print(tags_data)

        if len(tags_data) > 0:
            json_array = []
            for t in tags_data:

                sim1 = {
                    "Rem_desc": t[4],
                    "Rem_title": t[3], "buttontext": "",
                    "imagepath": "",
                    "Rem_type": t[3],
                    "Rem_date": chFormat(str(t[5])),
                    "Rem_time": t[6],
                    "status": "",
                    "Rem_set_date": t[9],
                    "no_of_days": "",
                    "name": t[2],
                    "redirectlink": "", "topright": "", "bottomtight": "",
                    "action": "", "message": "",
                    "ParameterTitle": ""}

                json_array.append(sim1)

            json_data = {
                "message": reminder1,
                "ParameterTitle": "CarausialView",
                "ParameterType": "ReminderView",
                "action": json_array}
            data1 = json.dumps(json_data, sort_keys=True, indent=4 * ' ')
            data = data1
            data2 = json.dumps(json_data, ensure_ascii=False)
            dbInsertion(temtext, data2, "answered", username,userType, userID, "-1", mainIssue, "--", "-1")
            #resp = flask.Response(data)
            resp = flask.Response(encrypt(data))
           #logger.info(f'{userID} [get] Response:' + str(json_data))
            return resp

        else:
            json_data = {
                "error": noreminder1,
            }
        data1 = json.dumps(json_data, sort_keys=True, indent=4 * ' ')
        data = data1
        data2 = json.dumps(json_data, ensure_ascii=False)
        dbInsertion(temtext, data2, "answered", username,userType, userID, "-1", mainIssue, "--", "-1")
        resp = flask.Response(encrypt(data))
        #resp = flask.Response(data)

       #logger.info(f'{userID} [get] Response:' + str(json_data))
        return resp

    elif "notify" in bot_data:
        notify = "You have the below mentioned Notification(s) by the Company Admin"
        if language_flag:
            notify = gettext(notify,language_flag)
        #currentdate = datetime.now().strftime("%Y-%m-%d")
        #query = "select * from reminder_detail where date = '" + currentdate + "' and emp_id = '" + userID+ "' order by time"
        query = "select * from notify order by notification_id desc"
        output = create_query(query)
        print(output)

        tag_list = list(output)
        print(tag_list)

        json_array = []

        for t in tag_list:

            sim1 = {
                "desc": t[1],
                "title": t[1], "buttontext": "",
                "imagepath": "",
                "description": t[2],
                "sender_name": t[3],
                 "date" : chFormat(str(t[5])),
                "redirectlink": "", "topright": "", "bottomtight": "",
                "action": "", "message": "",
                "ParameterTitle": ""}
            json_array.append(sim1)

        json_data = {
            "message": notify,
            "ParameterTitle": "CarausialView",
            "ParameterType": "Notification",
            "action": json_array}
        data1 = json.dumps(json_data, sort_keys=True, indent=4 * ' ')
        data = data1
        data2 = json.dumps(json_data, ensure_ascii=False)
        dbInsertion(temtext, data2, "answered", username,userType, userID, "-1", mainIssue, "--", "-1")
        print(data)
        #resp = flask.Response(data)
        resp = flask.Response(encrypt(data))
        return resp

    elif "Admin_default" in bot_data:
        addefault = "Kindly contact your Local HR Admin."
        if language_flag:
            addefault = gettext(addefault,language)
        json_data = {
            "message": addefault,
            "operation_id": "",
            "response": addefault,
            "userText": usertext,
            "title": "",
            "cat1": "Admin realted queries",
            "cat2": "Admin",
            "cat3": "Queries",
            "cat4": "",
            "video_path": "",
            "project_name": "",
            "ParameterTitle": "",
            "action": "",
            "orignalText": "",
            "typetext": "HR",
            "mainIssue": mainIssue,
            "emailFlag": ""
        }
        data1 = json.dumps(json_data, sort_keys=True, indent=4 * ' ')
        data = data1
        data2 = json.dumps(json_data, ensure_ascii=False)
        dbInsertion(temtext, data2, "answered", username,userType, userID, "-1", mainIssue, "--", "-1")
        print(data)
        #resp = flask.Response(data)
        resp = flask.Response(encrypt(data))
        return resp

    else:
        if bot_confidence >= 0.70:
            flag = True


    print("Usertext == ", usertext)
    print("flag == ", flag)
    print("bot confidence == ", bot_confidence)

    if flag:
        print("if flag is true")

        if bot_data == "ERROR":
            print("if error")

            json_data = {
                "error": imsorry,
                "cat1": "Application Services",
                "cat2": "Applications",
                "resolve": "",
                "rating": "err",
                "project_name": "MobitrailBot",
                "mainIssue": mainIssue
            }
            data1 = json.dumps(json_data, sort_keys=True, indent=4 * ' ')
            print("json data = ", data1)
            data = data1
            data2 = json.dumps(json_data, ensure_ascii=False)
            dbInsertion(temtext, data2, "answered", username,userType, userID,"-1",mainIssue,"--","-1")
            resp = flask.Response(encrypt(data))
            #resp = flask.Response(data)

           #logger.info(f'{userID} [get] Response:' + str(json_data))
            return resp

        elif "select" in bot_data:  # if data has sql query
            print("if select")
            if "operation" in bot_data:
                if language_flag:
                    bot_data = bot_data.replace("response",language)
            print(bot_data)
            output = create_query(bot_data)
            tag_list = list(output)
            print("list == ",tag_list)
            json_array = []
            lastFlag = False
            typetext = ""
            category = ""
            emailFlag = False
            for t_list in tag_list:
                print("in for loop")
                print(t_list)
                for idx, title in enumerate(t_list):

                    print(idx,",",title)
                    if len(t_list) == 2:
                        print("length is 2")
                        if idx == 0:
                            # if language_flag:
                            #     title = translate_text(title, language)
                            arr = {
                                "title": title,
                                "desc": title,
                                "buttontext": "",
                                "imagepath": "",
                                "redirectlink": "", "topright": "", "bottomtight": "",
                                "action": "", "message": "",
                                "ParameterTitle": ""
                            }
                            json_array.append(arr)
                            data1 = json.dumps(json_array)
                            data = data1
                            print("json data = ", data)
                        if idx == 1:
                            if language_flag:
                                title = translate_text(title, language)
                            head = title
                            print(head)
                    if len(t_list) == 8:
                        print("length is 8 ")
                        res_data = str(t_list[6])
                        if "|" in res_data:
                            list_data = res_data.split("|")
                            # print("list data == ",list_data)

                            for i in list_data:
                                if "#" in i:
                                    id_op = i.split("#")
                                    # print("id_op ",id_op)
                                    # if language_flag:
                                    #     t = translate_text(id_op[0], language)
                                    # else:


                                    t= id_op[0]
                                    sim = {
                                        "title": t,
                                        "desc": t,
                                        "operation_id": id_op[1],
                                        "main_op_id": "",
                                        "message": "",
                                        "buttontext": "",
                                        "imagepath": "",
                                        "redirectlink": "", "topright": "", "bottomtight": "",
                                        "action": "",
                                        "ParameterTitle": ""

                                    }
                                    json_array.append(sim)

                                    json_data = {
                                        "message": wldhappy,
                                        "action": json_array,
                                        "typetext": "HR",
                                        "ParameterTitle": "ListView",
                                        "mainIssue": "HR"
                                    }
                                elif "$" in i:
                                    id_main_op = i.split("$")
                                    # print("id main op ", id_main_op)
                                    # if language_flag:
                                    #     idmain = translate_text(id_main_op[0], language)
                                    # else:
                                    idmain = id_main_op[0]
                                    sim = {
                                        "title": idmain,
                                        "desc": idmain,
                                        "operation_id": "",
                                        "main_op_id": id_main_op[1],
                                        "message": "",
                                        "buttontext": "",
                                        "imagepath": "",
                                        "redirectlink": "", "topright": "", "bottomtight": "",
                                        "action": "",
                                        "ParameterTitle": ""

                                    }
                                    json_array.append(sim)

                                    json_data = {
                                        "message": wldhappy,
                                        "action": json_array,
                                        "typetext": "HR",
                                        "ParameterTitle": "ListView",
                                        "mainIssue": "HR"
                                    }
                                else:

                                    # if language_flag:
                                    #     i = translate_text(i, language)
                                    sim = {
                                        "title": i,
                                        "desc": i,
                                        "operation_id": "",
                                        "main_op_id": "",
                                        "message": "",
                                        "buttontext": "",
                                        "imagepath": "",
                                        "redirectlink": "", "topright": "", "bottomtight": "",
                                        "action": "",
                                        "ParameterTitle": ""

                                    }
                                    json_array.append(sim)

                                    json_data = {
                                        "message": wldhappy,
                                        "action": json_array,
                                        "typetext": "HR",
                                        "ParameterTitle": "ListView",
                                        "mainIssue": "HR"
                                    }
                            print("real",json_data)
                            data1 = json.dumps(json_data, sort_keys=True, indent=4 * ' ')
                            print("json data == ", data1)
                            data = data1
                            data2 = json.dumps(json_data, ensure_ascii=False)
                            dbInsertion(temtext, data2, "answered", username,userType, userID, "-1", mainIssue, "HR", "-1")
                            resp = flask.Response(encrypt(data))
                            #resp = flask.Response(data)


                            return resp
                    if len(t_list) == 17:
                        print("length is 17 ")
                        if str(t_list[3]) == "HR":
                            typetext = "HR"
                            category = "HR"
                        elif str(t_list[3]) == "Admin":
                            typetext = "Administration"
                            category = "Admin"
                        else:
                            typetext = "Operations"
                            category = "Operations"

                        query_response = str(t_list[6])
                        regex = '([\w+-]+@[\w-]+\.[\w\.-]+)'
                        email = re.search(regex, query_response)
                        if email:
                            emailFlag = True
                        print("Email flag == ", emailFlag)

                        video_path=t_list[15]
                        if video_path == None or video_path == "":
                            video_path = ""
                        else:
                            video_path = video_path_BaseURL + video_path

                        query_response = query_response.replace("##LINK##", image_path_BAseURL)


                        # if language_flag:
                        #
                        #     query_response = translate_text(query_response,language)
                        #     print(query_response)

                        # queryResponse = query_response.replace("##LINK##", image_path_BAseURL)

                        print("direct sql")
                        json_data = {
                                    "message": query_response,
                                    "operation_id": t_list[0],
                                    "response": query_response,
                                    "userText": temtext,
                                    "title": t_list[1],
                                    "cat1": t_list[2],
                                    "cat2": t_list[3],
                                    "cat3": t_list[4],
                                    "cat4": t_list[5],
                                    "video_path": video_path,
                                    "project_name": t_list[16],
                                    "ParameterTitle": "",
                                    "action": "",
                                    "orignalText": "",
                                    "typetext": typetext,
                                    "mainIssue": mainIssue,
                                    "emailFlag": emailFlag
                                }
                        lastFlag = True
                        data1 = json.dumps(json_data, sort_keys=True, indent=4 * ' ')
                        print("json data = ", data1)
                        data = data1
                        data2 = json.dumps(json_data, ensure_ascii=False)
                        dbInsertion(temtext, data2, "answered", username,userType, userID, "-1", mainIssue, category, "-1")
                        resp = flask.Response(encrypt(data))
                        #resp = flask.Response(data)

                        return resp
                    if len(t_list) == 9:
                        print("length is 9 ")
                        if str(t_list[3]) == "HR":
                            typetext = "HR"
                            category = "HR"
                        elif str(t_list[3]) == "Admin":
                            typetext = "Administration"
                            category = "Admin"
                        else:
                            typetext = "Operations"
                            category = "Operations"

                        query_response = str(t_list[6])
                        regex = '([\w+-]+@[\w-]+\.[\w\.-]+)'
                        email = re.search(regex, query_response)
                        if email:
                            emailFlag = True
                        print("Email flag == ", emailFlag)

                        video_path=t_list[7]
                        if video_path == None or video_path == "":
                            video_path = ""
                        else:
                            video_path = video_path_BaseURL + video_path
                        query_response = query_response.replace("##LINK##", image_path_BAseURL)


                        if language_flag:

                            query_response = translate_text(query_response,language)
                            print(query_response)

                        # queryResponse = query_response.replace("##LINK##", image_path_BAseURL)

                        print("direct sql")
                        json_data = {
                                    "message": query_response,
                                    "operation_id": t_list[0],
                                    "response": query_response,
                                    "userText": temtext,
                                    "title": t_list[1],
                                    "cat1": t_list[2],
                                    "cat2": t_list[3],
                                    "cat3": t_list[4],
                                    "cat4": t_list[5],
                                    "video_path": video_path,
                                    "project_name": t_list[8],
                                    "ParameterTitle": "",
                                    "action": "",
                                    "orignalText": "",
                                    "typetext": typetext,
                                    "mainIssue": mainIssue,
                                    "emailFlag": emailFlag
                                }
                        lastFlag = True
                        data1 = json.dumps(json_data, sort_keys=True, indent=4 * ' ')
                        print("json data = ", data1)
                        data = data1
                        data2 = json.dumps(json_data, ensure_ascii=False)
                        dbInsertion(temtext, data2, "answered", username,userType, userID, "-1", mainIssue, category, "-1")
                        resp = flask.Response(encrypt(data))
                        #resp = flask.Response(data)

                        return resp
                    if len(t_list) == 1:
                        if idx == 0:
                            resp = title
                            lastFlag = True
                if lastFlag:
                    print("Answer = ", data1)
                else:
                    print("in else...")
                    if str(head).lower == "hr":
                        typetext = "HR"
                        category = "HR"
                    elif str(head).lower() == "admin":
                        typetext = "Administration"
                        category = "Admin"
                    else:
                        typetext = "Operations"
                        category = "Operations"

                    json_data = {
                        "message": head,
                        "ParameterTitle": "ListView",
                        "typetext": typetext,
                        "action": json_array,
                        "mainIssue": mainIssue
                    }
                data1 = json.dumps(json_data, sort_keys=True, indent=4 * ' ')
                print("json data = ", data1)
                data = data1
                data2 = json.dumps(json_data, ensure_ascii=False)
                dbInsertion(temtext, data2, "answered", username,userType, userID, "-1", mainIssue, category, "-1")
                resp = flask.Response(encrypt(data))
                #resp = flask.Response(data)

               #logger.info(f'{userID} [get] Response:' + str(json_data))
                return resp

        else:
            print("bot data==", bot_data)
            json_array = []

            if language_flag:
                bot_data = translate_text(bot_data, language)
            sim = {
                    "title": str(bot_data),
                    "desc": str(bot_data),
                    "buttontext": "",
                    "imagepath": "",
                    "redirectlink": "", "topright": "", "bottomtight": "",
                    "action": "", "message": "",
                "ParameterTitle": ""
                }
            json_array.append(sim)

            json_data = {
                    "message": areyoulookingfor,
                    "ParameterTitle": "ListView",
                    "action": json_array,
                    "resolve": "",
                    "rating": "no",
                    "mainIssue": mainIssue
                }
            data1 = json.dumps(json_data, sort_keys=True, indent=4 * ' ')
            print("json data == ", data1)
            data = json.dumps(json_data, ensure_ascii=False)
            dbInsertion(temtext, data, "query", username,userType, userID, "-1", mainIssue, "--", "-1")
            resp = flask.Response(encrypt(data1))
            #resp = flask.Response(data)

           #logger.info(f'{userID} [get] Response:' + str(json_data))
            return resp

    elif flag == False:
        if bot_confidence > 0.50 or fuzzymatch > 60:
            equalMatch = False
            usertextsplit = usertext.split(" ")
            print("usertextsplit", usertextsplit)
            Matchtextsplit = matchText.split(" ")
            #Matchtextsplit = usertextsplit
            print("Matchtextsplit:", Matchtextsplit)
            print(len(Matchtextsplit))
            json_array = []
            fuzzydata = ["reminder", "leaves", "notification", "leave", "reminders", "paternity","comp","sat","code","need","income","salary","tax","attendance","ESIC",
                         "UAN","PARS","mouse","tab","desktop","internet","gmail","outlook","sim"]
            temp = False
            for text in Matchtextsplit:
                #print("text",text)
                for match in fuzzydata:
                    #print("text== ", text, "match== ", match)
                    if text.lower() == match.lower() and text.lower() != "" and match.lower() != "":
                            #print("in if")
                            temp = True
                            equalMatch = True
                            print(equalMatch)
                            tabdata = match.lower()
                            print("data:-", tabdata)
                            break
                    else:
                        equalMatch= False
                if temp:
                    break


            if equalMatch:
                if thirdvar.lower() == "hr":
                    typetext = "hr"
                    category = "HR"
                elif thirdvar.lower() == "admin":
                    typetext = "admin"
                    category = "Admin"
                else:
                    typetext = ""
                    category = "Technology"

                print("data:-", tabdata)


                query = create_query("SELECT title FROM operations WHERE lower(title) LIKE '%" + tabdata + "%' or '" + tabdata + "%' or '%" + tabdata + "' ")
                tagsdata = list(query)
                print("Tagsdata:", tagsdata)

                if len(tagsdata)>0:
                    for t in tagsdata:
                        d = str(t).replace("(", "").replace(",", "").replace(")", "").replace("'", "")
                        #print(d , ",")
                        if language_flag:
                           d= translate_text(d,language)
                        sim1 = {
                                "desc": d,
                                "title": d, "buttontext": "", "id": "",
                                "imagepath": "",
                                "redirectlink": "", "topright": "", "bottomtight": "",
                                "action": "", "message": "",
                                "ParameterTitle": ""}
                        json_array.append(sim1)



                        json_data = {
                            "message": areyoulookingfor,
                            "ParameterTitle": "ListView",
                            "action": json_array,
                            "resolve": "",
                            "rating": "no",
                            "typetext": thirdvar,
                            "mainIssue": mainIssue
                        }

                else:
                    json_data = {
                        "error": imsorry,
                        "resolve": "",
                        "rating": "err",
                        "ParameterTitle": "",
                        "action": "",
                        "cat1": "",
                        "cat2": "",
                        "cat3": "",
                        "cat4": "",
                        "emailFlag": "",
                        "mainIssue": mainIssue,
                        "message": imsorry,
                        "operation_id": "",
                        "orignalText": "",
                        "project_name": "Service Request",
                        "response": imsorry,
                        "title": temtext,
                        "typetext": "",
                        "userText": temtext,
                        "video_path": ""
                    }
                data1 = json.dumps(json_data, sort_keys=True, indent=4 * ' ')
                print("json data ==",data1)
                data = data1
                data2 = json.dumps(json_data, ensure_ascii=False)
                dbInsertion(temtext, data2, "query", username,userType, userID, platform, "-1", mainIssue, "")
                resp = flask.Response(encrypt(data))
                #resp = flask.Response(data)
                resp.headers['Access-Control-Allow-Origin'] = '*'
               #logger.info(f'{userID} [get] Response:' + str(json_data))
                return resp
            elif equalMatch == False:
                json_data = {
                    "error": imsorry,
                    "resolve": "",
                    "rating": "err",
                    "ParameterTitle": "",
                    "action": "",
                    "cat1": "",
                    "cat2": "",
                    "cat3": "",
                    "cat4": "",
                    "emailFlag": "",
                    "mainIssue": mainIssue,
                    "message": imsorry,
                    "operation_id": "",
                    "orignalText": "",
                    "project_name": "Service Request",
                    "response": imsorry,
                    "title": temtext,
                    "typetext": "",
                    "userText": temtext,
                    "video_path": ""
                }

                # print(json_data)
                data1 = json.dumps(json_data, sort_keys=True, indent=4 * ' ')
                data = json.dumps(json_data, ensure_ascii=False)
                print("json data = ", data1)
                dbInsertion(temtext,imsorry, "unanswered",
                            username, userType,
                            userID,
                            "-1", mainIssue, "--", "-1")

                resp = flask.Response(encrypt(data1))
                #resp = flask.Response(data)

               #logger.info(f'{userID} [get] Response:' + str(json_data))
                return resp

        else:
            json_data = {
                "error": imsorry,
                "resolve": "",
                "rating": "err",
                "ParameterTitle": "",
                "action": "",
                "cat1": "",
                "cat2": "",
                "cat3": "",
                "cat4": "",
                "emailFlag": "",
                "mainIssue": mainIssue,
                "message": imsorry,
                "operation_id": "",
                "orignalText": "",
                "project_name": "Service Request",
                "response":imsorry,
                "title": temtext,
                "typetext": "",
                "userText": temtext,
                "video_path": ""
            }

            # print(json_data)
            data1 = json.dumps(json_data, sort_keys=True, indent=4 * ' ')
            print("json data = ", data1)
            dbInsertion(temtext, imsorry, "unanswered", username, userType,
                        userID,
                        "-1", mainIssue, "--", "-1")
            data = json.dumps(json_data, ensure_ascii=False)
            resp = flask.Response(encrypt(data1))
            #resp = flask.Response(data)

           #logger.info(f'{userID} [get] Response:' + str(json_data))
            return resp

    else:
        json_data = {
            "error": imsorry,
            "resolve": "",
            "rating": "err",
            "ParameterTitle": "",
            "action": "",
            "cat1": "",
            "cat2": "",
            "cat3": "",
            "cat4": "",
            "emailFlag": "",
            "mainIssue": mainIssue,
            "message":imsorry,
            "operation_id": "",
            "orignalText": "",
            "project_name": "Service Request",
            "response": imsorry,
            "title": temtext,
            "typetext": "",
            "userText": temtext,
            "video_path": ""
        }

        # print(json_data)
        data1 = json.dumps(json_data, sort_keys=True, indent=4 * ' ')
        print("json data = ", data1)
        dbInsertion(temtext, imsorry, "unanswered", username, userType, userID,
                    "-1", mainIssue, "--", "-1")
        data = json.dumps(json_data, ensure_ascii=False)
        resp = flask.Response(encrypt(data1))
        #resp = flask.Response(data)

       #logger.info(f'{userID} [get] Response:' + str(json_data))
        return resp
    #
    # except Exception as e:
    #     logger.error(f'{userID} [get] Excepyion occured' ,exc_info=True)
    #     json_data = {
    #         "error": "We are sorry that we could not resolve your issue. Would you like to send a mail to the Help Desk Team?",
    #         "resolve": "",
    #         "rating": "no", "mainIssue": mainIssue
    #     }
    #
    #     # print(json_data)
    #     data1 = json.dumps(json_data, sort_keys=True, indent=4 * ' ')
    #     data = data1
    #     # print(data)
    #     data2 = json.dumps(json_data, ensure_ascii=False)
    #     dbInsertion(temtext, "EXCEPTION OCCURED " + data2 + " " + str(e), "unanswered", username, userType, userID,
    #                 "-1", mainIssue, "--","-1")
    #     traceback.print_exc()
    #     # print("Exception occured ",e)
    #     resp = flask.Response(encrypt(data))
    #     #resp = flask.Response(data)
    #
    #     resp.headers['Access-Control-Allow-Origin'] = '*'
    #    #logger.info(f'{userID} [get] Response:' + str(json_data))
    #     return resp  # translations[0].tbankoperation16ext)


def dbInsertion(usertext, response, flag, username, userType, userID, feedback, mainIssue, category, emailSent):
    try:
        print("db flag==",flag)
        usertext = str(usertext).replace("'", "").replace("\\", "")
        response = response.replace('src=\\"',"src=\'\'").replace('src = \\"',"src=\'\'").replace('.jpg\\"',".jpg\'\'")
        print("res==",response)
        currenttime = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        resptime = (datetime.now()+timedelta(seconds=3)).strftime("%Y-%m-%d %H:%M:%S")
        print(currenttime, "== ",resptime)
        requestFlag = False
        respFlag = False
        if usertext != "":
            print("in req")
            requestFlag = True
            historyFlag = "request"
            insertHistory(currenttime,usertext,historyFlag,username,userID)

        if response != "":
            print("in resp")
            respFlag = True
            historyFlag = "response"
            insertHistory(resptime, response, historyFlag, username, userID)


        #usertext = str(usertext).replace("'", "").replace("\\", "")
        print("flag=>",flag)
        if flag.lower() == "unanswered":
            unanswered_query = "insert into unanswered_queries" \
                               "(query,asked_on,username,userType,userid,category)" \
                               "values('" + str(usertext) + "','" + currenttime + "','" + str(username) + "','" + str(userType) + "','" + str(
                userID) + "','" + str(mainIssue) + "')"
            print("unanswered query = ", unanswered_query)
            insertquery(unanswered_query)
            inserted_data = create_query("SELECT * FROM `unanswered_queries` where `username` = '" + str(
                username) + "' order by `asked_on` desc LIMIT 1")
            print("####@@",inserted_data)


        else:
            #response = response.replace('\'', '\\"')

            answered_query = "insert into answered_queries" \
                             "(query,asked_on,username,userType,query_answer,userID,feedback,category,email_sent)" \
                             "values('" + str(usertext) + "','" + currenttime + "','" + str(username) + "','" + str(userType) + "','" + str(
                response) + "','" + str(userID) + "','" + str(feedback) + "','" + str(category) + "','" + str(
                emailSent) + "')"
            print("answered query = ", answered_query)
            insertquery(answered_query)
            inserted_data = create_query("SELECT * FROM `answered_queries` where `username` = '" + str(
                username) + "' order by `asked_on` desc LIMIT 1 ")
            print("====",inserted_data)

    except Exception as e:
        print("Exception occur ", e)


@app.route('/getFinalResponse', methods=["POST", "GET"])
# def get_final_response():
#     user_data1 = request.get_data()
#     user_data = decrypt(user_data1)
#     print(" === ",user_data1)
#     user_text = json.loads(user_data)
#     print("response userdata ==== ", user_text)
#     usertext = user_text.get('usertext')
#     userID = user_text.get('userID')
#     username = user_text.get('userName')
#     operation_id = user_text.get('operation_id')
#     response = user_text.get('response')
#     userResponse = user_text.get('userResponse')
#
#     query_id = ""
#
#     if userResponse.lower() == "no":
#         try:
#             get_ans_query = "SELECT query_id FROM `answered_queries` where `username` = '" + username + "' and `feedback` = '-1' order by `asked_on` desc LIMIT 1 "
#             uns = create_query(get_ans_query)
#             print("uns= ", uns)
#             query_id = uns[0][0]
#             print("query id = ", query_id)
#             if len(uns) > 0:
#                 answered_query = "UPDATE answered_queries SET `feedback`='" + userResponse + "' where query_id = '" + str(
#                     query_id) + "' and `feedback`='-1'"
#                 insertquery(answered_query)
#                 #print(answered_query)
#         except Exception as e:
#             print("Exception occur ", e)
#
#         resp = flask.Response(encrypt(
#             "We are sorry that we could not resolve your issue. Would you like to send a mail to the Help Desk Team"))
#
#         return resp
#
#     if userResponse.lower() == "yes":
#         try:
#             get_ans_query = "SELECT query_id FROM `answered_queries` where `username` = '" + username + "' and `feedback` = '-1' order by `asked_on` desc LIMIT 1 "
#             uns = create_query(get_ans_query)
#             query_id = uns[0][0]
#             print("query id ", query_id)
#             if len(uns) > 0:
#                 answered_query = "UPDATE answered_queries SET `feedback`='" + userResponse + "' where query_id = '" + str(
#                     query_id) + "' and `feedback`='-1'"
#                 insertquery(answered_query)
#                 print(answered_query)
#         except Exception as e:
#             print("Exception occur ", e)
#         resp = flask.Response(encrypt("Thank you!"))
#         #resp = flask.Response("Thank you!")
#
#         return resp
#
#     if userResponse.lower() == "" or userResponse.lower() == None:
#         try:
#             get_ans_query = "SELECT query_id FROM `answered_queries` where `username` = '" + username + "' and `feedback` = '-1' order by `asked_on` desc LIMIT 1 "
#             uns = create_query(get_ans_query)
#             query_id = uns[0][0]
#             print("query id ", query_id)
#             if len(uns) > 0:
#                 answered_query = "UPDATE answered_queries SET `feedback`='--',tabFeedBack='no' where query_id = '" + str(
#                     query_id) + "' and `feedback`='-1'"
#                 insertquery(answered_query)
#                 print(answered_query)
#         except Exception as e:
#             print("Exception occur ", e)
#         resp = flask.Response(encrypt(
#             "We are sorry that we could not resolve your issue. Would you like to send a mail to the Help Desk Team"))
#         # resp = flask.Response(
#         #     "We are sorry that we could not resolve your issue. Would you like to send a mail to the Help Desk Team")
#         return resp
def get_bot_response1111():
    try:
        print("get Final Response")
       # resp = ""

        message1 = request.get_data()
        message2 = decrypt(message1)
        objectrecived = json.loads(message2)
        # print(objectrecived)
        platform = objectrecived.get('platform')
        userID = objectrecived.get('userID')
        userName = objectrecived.get('userName')
        userID = objectrecived.get('userID')
        operation_id = objectrecived.get('operation_id')
        title = objectrecived.get('title')
        userText = objectrecived.get('userText')
        message = objectrecived.get('message')
        response = objectrecived.get('response')
        description = objectrecived.get('description')
        cat1 = objectrecived.get('cat1')
        cat2 = objectrecived.get('cat2')
        cat3 = objectrecived.get('cat3')
        cat4 = objectrecived.get('cat4')

        project_name = objectrecived.get('project_name')
        userResponse = objectrecived.get('userResponse')
        orignalText = objectrecived.get('title')

        # location = objectrecived.get('location')
        message = str(message).replace("'", "").replace("#|#", "<br>")
        # print(userResponse)
        # print("userid", userID)
        # print("Useresponse:",userResponse)
        queryid = ''
     ##################################
        user_zone = create_query("select `zone` from `mastertable` where `userID` = " + str(userID))[0][0]
        print('zone--- ', user_zone)

        #update in 17-02-2020
        # Remove ##C## and ##form##
        if message.find("##C##") != -1:
            message = message.strip("##C##")
        elif message.find("##form##"):
            message = message.strip("##form##")
     #######################################
        desc = "User Query : " + str(orignalText) + "<br><br>Bot Response : " + str(
            message) + "<br><br>Issue Description : " + str(description)

        # desc = "<br><br>Bot Response : " + str(
        #     message) + "<br><br>Issue Description : " + str(
        #     description)

        currenttime = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        logger.info(f'{userID} [getFinalResponse] Request:' + str(objectrecived))
        if userResponse.lower() == 'no':  # if users issue did not resolved
            try:
                getAnswered_query = "SELECT query_id FROM `answered_queries` where `username`='" + userName + "' and `Feedback`='-1' order by`asked_on` desc LIMIT 1 "
                uns = create_query(getAnswered_query)
                # print(uns[0][0])
                queryid = uns[0][0]
                # print("queryid " + str(queryid))
                if len(uns) > 0:
                    answered_query = "update answered_queries set `Feedback`='" + userResponse + "' where `query_id`=" + str(
                        queryid) + " and `Feedback`='-1'"
                    # print(answered_query)
                    uns = insertquery(answered_query)

            except Exception as e:
                logger.error(f'{userID} [getFinalResponse] Exception occurred', exc_info=True)

                # print("Exception Occured " + e)
            resp = flask.Response(encrypt(
                "We are sorry that we could not resolve your issue. Would you like to raise a ticket to the Help Desk Team?"))
            resp.headers['Access-Control-Allow-Origin'] = '*'

            return resp
        if userResponse.lower() == 'yes':
            try:
                getAnswered_query = "SELECT query_id FROM `answered_queries` where `username`='" + userName + "' and `Feedback`='-1' order by`asked_on` desc LIMIT 1 "
                uns = create_query(getAnswered_query)
                # print(uns[0][0])
                queryid = uns[0][0]
                # print("queryid " + str(queryid))
                if len(uns) > 0:
                    answered_query = "update answered_queries set `Feedback`='" + userResponse + "' where `query_id`=" + str(
                        queryid) + " and `Feedback`='-1'"
                    # print(answered_query)
                    uns = insertquery(answered_query)

            except Exception as e:
                logger.error(f'{userID} [getFinalResponse] Exception occurred', exc_info=True)

                print("Exception Occured " + e)

        if userResponse.lower() == '' or userResponse.lower() is None:
            try:
                getAnswered_query = "SELECT query_id FROM `answered_queries` where `username`='" + userName + "' and `Feedback`='-1' order by`asked_on` desc LIMIT 1 "
                uns = create_query(getAnswered_query)

                queryid = uns[0][0]
                # print("queryid " + str(queryid))
                if len(uns) > 0:
                    answered_query = "update answered_queries set `Feedback`='--',tabfeedback='no' where `query_id`=" + str(
                        queryid) + " and `Feedback`='-1'"
                    # print(answered_query)
                    uns = insertquery(answered_query)

            except Exception as e:
                logger.error(f'{userID} [getFinalResponse] Exception occurred', exc_info=True)

                # print("Exception Occured " + e)
            resp = flask.Response(encrypt(
                "We are sorry that we could not resolve your issue. Would you like to raise a ticket to the Help Desk Team?"))
            resp.headers['Access-Control-Allow-Origin'] = '*'

            return resp

        random_id = randint(10000000, 999999999999)
        # print(random_id)
        url = 'https://mgenius.in/ITSMTool/Service/Create'
        headers = {"Accept": "application/json",
                   "Content-Type": "application/json",
                   "int-log-id": "qwertyasdfg",
                   "key": "2fb29d27-51a9-4074-82f5-45db3f450d24",
                   "token": "7560a221-28b3-4343-8848-2388fe788d51",
                   "Cache-Control": "no-cache"}
        sourceName = ""
        if cat2 == "Domain Configuration":
            sourceName = "Chat Bot"
        else:
            sourceName = "Chat Bot"

        if cat4 == "" or cat4 == 'null' or cat4 == "NULL" or cat4 == None:
            cat4 = ""
        # else:
        #     derivedfield = "derivedField1"


        data = {
            "requestType": "CREATE_TICKET",
            "integrationLogId": random_id,
            "ticket": {
                "project": {
                    "projectName": project_name
                },
                "service": {
                    "name": cat1
                },
                "category": {
                    "name": cat2
                },
                "subCategory": {
                    "name": cat3
                },
                "derivedfield": {
                    "name": cat4
                },

                "probDescription": desc,
                "title": title,
                "submittedBy": {
                    "userName": userID,
                    # "userName": "mob_nikhil_l"
                    "Zone": user_zone
                },
                # "location": {
                #     "name": "Default"
                # },
                "department": {
                    "name": "Default"
                },
                "source": {
                    "name": sourceName
                },
                "additionalParams": {
                    "updated": False
                }
            }
        }

        data = json.dumps(data)
        response = requests.post(url, data=data, headers=headers, verify=False)
        # response = {
        #      "requestType": "CREATE_TICKET",
        #      "integrationLogId": "958104188316",
        #      "iteration": 0,
        #      "problemId": 54209,
        #      "requestNumber": "INC-010174"
        # }
        response = json.loads(response.text)
        # print("Respond:",+response)
        logger.info(f'{userID} [getFinalResponse] Response:' + str(response))
        if response.get("code"):
            # print("error")

            resp = flask.Response(encrypt(response.get("message")))
            resp.headers['Access-Control-Allow-Origin'] = '*'

            return resp
        else:
            Ticket_id_ = response.get("requestNumber")

            random_id = randint(10000000, 999999999999)
            # print(random_id)
        if userResponse.lower() == 'yes':  # if users issue resolved

            url = 'https://mgenius.in/ITSMTool/Service/update'
            headers = {"Accept": "application/json",
                       "Content-Type": "application/json",
                       "int-log-id": "qwertyasdfg",
                       "key": "2fb29d27-51a9-4074-82f5-45db3f450d24",
                       "token": "7560a221-28b3-4343-8848-2388fe788d51",
                       "Cache-Control": "no-cache"}
            data = {

                "requestType": "UPDATE_TICKET",

                "integrationLogId": random_id,

                "ticket": {

                    "requestId": Ticket_id_,

                    "project": {

                        "projectName": project_name

                    },

                    "currentState": {

                        "stateName": "Closed"

                    },

                    "additionalParams": {

                        "updated": True,

                        "attribute1": {

                            "updated": True,

                            "data": "",

                        }

                    },

                    "ticketStateDTO": {

                        "comment": "",
                        "user": userID,
                        #   "user": "mob_nikhil_l"

                    }

                }

            }
            data = json.dumps(data)
            logger.info(f'{userID} [getFinalResponse] SapphireUpdate:' + str(data))
            response = requests.post(url, data=data, headers=headers, verify=False)
            # response ={
            #      "requestType": "UPDATE_TICKET",
            #      "integrationLogId": "5421545144542",
            #      "iteration": 0,
            #      "problemId": 54209,
            #      "requestNumber": "INC-010174"
            # }
            response = json.loads(response.text)
            logger.info(f'{userID} [getFinalResponse] SapphireUpdateResponse:' + str(response))
            if response.get("code"):
                # print("error")
                resp = flask.Response(encrypt(response.get("message")))
                Ticket_id_ = response.get("message")
                resp.headers['Access-Control-Allow-Origin'] = '*'
            else:
                resp = flask.Response(encrypt(
                    "Thank you, We have created Ticket for your issue.<br><b><center>Ticket ID&nbsp;<font size='5px' color='#174c82'>" + Ticket_id_ + "</font></center>"))

                # resp = flask.Response(encrypt(" <br><b><center>Ticket ID&nbsp;<font size='5px' color='#174c82'>"+Ticket_id_+"</font></center>"))
                resp.headers['Access-Control-Allow-Origin'] = '*'

        try:

            # print("queryid " + str(queryid))
            if userResponse.lower() == '' or userResponse.lower() is None:
                if len(uns) > 0:
                    answered_query = "update answered_queries set `Feedback`='--',tabfeedback='no', Ticket_id='" + Ticket_id_ + "' where `query_id`=" + str(
                        queryid) + ""
                    # print(answered_query)
                    uns = insertquery(answered_query)
                resp = flask.Response(encrypt(
                    "We are sorry that we could not resolve your issue. Would you like to raise a ticket to the Help Desk Team?"))

                resp.headers['Access-Control-Allow-Origin'] = '*'
            else:
                if len(uns) > 0:
                    answered_query = "update answered_queries set `Feedback`='" + userResponse + "', Ticket_id='" + Ticket_id_ + "' where `query_id`=" + str(
                        queryid) + ""
                    # print(answered_query)
                    uns = insertquery(answered_query)
            return resp
        except Exception as e:
            logger.error(f'{userID} [getFinalResponse] Exception occurred', exc_info=True)
            resp = flask.Response(encrypt(
                "We are sorry that we could not resolve your issue. Would you like to raise a ticket to the Help Desk Team?"))

            resp.headers['Access-Control-Allow-Origin'] = '*'
            # print("Exception Occured " + e)
        return resp
    except Exception as e:
        logger.error(f'{userID} [getFinalResponse] Exception occurred', exc_info=True)
        traceback.print_exc()
        resp = flask.Response(encrypt(
            "Currently service not available"))
        resp.headers['Access-Control-Allow-Origin'] = '*'
        return resp

@app.route("/getTicStatus", methods=["POST", "GET"])
def get_bot_response_tic():
    try:
        message1 = request.get_data()
        message2 = decrypt(message1)
        objectrecived = json.loads(message2)
        userName = objectrecived.get('userName')
        Ticket = objectrecived.get('ticket_id')
        Ticket = Ticket.upper()
        logger.info(f'{userName} [getTicStatus] Request:' + str(objectrecived))
        # if hasNumbers(Ticket):
        #     tempText = re.search(r'\d+', Ticket).group()
        #     Ticket =(tempText)
        #
        #     Ticket="INC-"+str(Ticket)
        # else:
        #     resp = flask.Response(encrypt("Please enter valid Ticket Id"))
        #     resp.headers['Access-Control-Allow-Origin'] = '*'
        #     return resp

        if Ticket[:3] == "INC":
            url = 'https://mgenius.in/ITSMTool/Service/GetTicketDetailsByID/' + Ticket
        elif Ticket[:3] == "SR-":
            url = 'https://mgenius.in/ITSMTool/Service/GetTicketDetailsByID/' + Ticket
        else:
            resp = flask.Response(encrypt("Please enter valid Ticket Id"))
            resp.headers['Access-Control-Allow-Origin'] = '*'
            logger.info(f'{userName} [getTicStatus]  Response: Please enter valid Ticket Id')

            return resp

        headers = {"Accept": "application/json",
                   "Content-Type": "application/json",
                   "int-log-id": "qwertyasdfg",
                   "key": "2fb29d27-51a9-4074-82f5-45db3f450d24",
                   "token": "7560a221-28b3-4343-8848-2388fe788d51",
                   "Cache-Control": "no-cache"}

        response = requests.get(url, headers=headers, verify=False)

        response = json.loads(response.text)
        logger.info(f'{userName} [getTicStatus]  MgeniusResponse:' + str(response))
        if response.get("code"):
            resp = flask.Response(encrypt(response.get("message")))
            resp.headers['Access-Control-Allow-Origin'] = '*'
            logger.info(f'{userName} [getTicStatus]  Response:' + str(response.get("message")))
            return resp

        else:
            # print("success")
            Status = response.get("ticket").get("currentState").get("stateName")
            resp = flask.Response(encrypt(
                "Status of Ticket ID " + Ticket + "<br><b><center><font size='4px' color='#174c82'>" + Status + "</font></center>"))
            resp.headers['Access-Control-Allow-Origin'] = '*'
            logger.info(
                f'{userName} [getTicStatus]  Response:Status of Ticket ID '+Ticket+'<br><b><center><font size="4px" color="#174c82">'+Status+'</font></center>')
            return resp
    except:
        logger.error(f'{userName} [getTicStatus] Exception occurred', exc_info=True)
        resp = flask.Response(encrypt(
            "Currently service not available"))
        resp.headers['Access-Control-Allow-Origin'] = '*'
        logger.info(f'{userName} [getTicStatus]  Response: Currently service not available')
        return resp

@app.route('/getIssueTicket',methods=["POST","GET"])
def get_issue_ticket():
    try:
        filestoragearray = []
        # posted_file = request.files['descAttachment']
        posted_file1 = request.files.getlist('descAttachmentOne', None)
        if posted_file1:
            filestoragearray.append(posted_file1)

        posted_file2 = request.files.getlist('descAttachmentTwo', None)
        if posted_file2:
            filestoragearray.append(posted_file2)

        posted_file3 = request.files.getlist('descAttachmentThree', None)
        if posted_file3:
            filestoragearray.append(posted_file3)
        #
        # new_Zonal_file1 = request.files.getlist('ZonalHeadAttachmentOne', None)
        # if new_Zonal_file1:
        #     filestoragearray.append(new_Zonal_file1)
        #
        # new_error_file1 = request.files.getlist('ErrSSAttachmentOne', None)
        # if new_error_file1:
        #     filestoragearray.append(new_error_file1)
        #
        # new_error_file2 = request.files.getlist('ErrSSAttachmentTwo', None)
        # if new_error_file2:
        #     filestoragearray.append(new_error_file2)

        totalfile = []

        for filedata in filestoragearray:
            for file in filedata:
                file.save(os.path.join(app.config['UPLOAD_FOLDER'], file.filename))
                file_name = file.filename
                totalfile.append(file_name)

        print('totalfiles ----> ',totalfile)


        bodycontent = request.form.to_dict()
        print("Bodycontent: ", bodycontent)
        if len(bodycontent) > 0:
            objectrecived = json.loads(decrypt(bodycontent['requestData']))
        else:
            message1 = request.get_data()
            message2 = decrypt(message1)
            objectrecived = json.loads(message2)

        print(objectrecived)
        resolve = objectrecived.get('resolve')
        userID = objectrecived.get('userID')
        userName = objectrecived.get('userName')
        # FinalResponse = objectrecived.get('finalResponse')
        userID = objectrecived.get('userID')
        operation_id = objectrecived.get('operation_id')
        title = objectrecived.get('title')
        userText = objectrecived.get('userText')
        message = objectrecived.get('message')
        response = objectrecived.get('response')
        description = objectrecived.get('description')
        cat1 = objectrecived.get('cat1')
        cat2 = objectrecived.get('cat2')
        cat3 = objectrecived.get('cat3')
        cat4 = objectrecived.get('cat4')
        print('cat4--- ',cat4)
        project_name = objectrecived.get('project_name')
        userResponse = objectrecived.get('userResponse')
        orignalText = objectrecived.get('title')
        chatHistory = objectrecived.get('chatHistory')
        print("chatHistory :--------- ", chatHistory)
        mainIssue = objectrecived.get('mainIssue')
        print("MessageIssueTicket:", message)





        currenttime = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        logger.info(f'{userID} [getIssueTicket] Request:' + str(objectrecived))
        random_id = randint(10000000, 999999999999)
        # print(random_id)




        if cat4 == "" or cat4 == 'null' or cat4 == "NULL" or cat4 == None:
            cat4 = ""
        # else:
        #     derivedfield = "derivedField1"

        user_zone = create_query("select `zone` from `mastertable` where `userID` = "+str(userID))[0][0]
        print('zone--- ',user_zone)

        sourceName = ""
        if cat2 == "Domain Configuration":
            sourceName = "Chat Bot"
        else:
            sourceName = "Chat Bot"

        desc = "User Query : " + str(orignalText) + "<br><br>Bot Response : " + str(
            message) + "<br><br>Issue Description : " + str(
            description)

        # desc = "<br><br>Bot Response : " + str(
        #     message) + "<br><br>Issue Description : " + str(
        #     description)

        if userResponse.lower() == 'yes':
            url = 'https://mgenius.in/ITSMTool/Service/Create'
            headers = {"Accept": "application/json",
                       "Content-Type": "application/json",
                       "int-log-id": "qwertyasdfg",
                       "key": "2fb29d27-51a9-4074-82f5-45db3f450d24",
                       "token": "7560a221-28b3-4343-8848-2388fe788d51",
                       "Cache-Control": "no-cache"}

            data = {
                "requestType": "CREATE_TICKET",
                "integrationLogId": random_id,
                "ticket": {
                    "project": {
                        "projectName": project_name
                    },
                    "service": {
                        "name": cat1
                    },
                    "category": {
                        "name": cat2
                    },
                    "subCategory": {
                        "name": cat3
                    },
                    "derivedfield": {
                        "name": cat4
                    },
                    "probDescription": desc,
                    "title": title,
                    "submittedBy": {
                        "userName": userID,
                        # "userName": "mob_nikhil_l"
                        "Zone":user_zone
                    },
                    # "location": {
                    #     "name": "Default"
                    # },
                    "department": {
                        "name": "Default"
                    },
                    "source": {
                        "name": sourceName
                    },
                    "chatHistory": chatHistory,
                    "additionalParams": {
                        "updated": False
                    }
                }
            }
            data = json.dumps(data)
            print(data)
            logger.info(f'{userID} [getIssueTicket]  MgeniusRequest:' + str(data))
            response = requests.post(url, data=data, headers=headers, verify=False)
            print(response)
            response = json.loads(response.text)
            print('res text---->',response)
            # response ={
            #     "requestType": "CREATE_TICKET",
            #     "integrationLogId": "958104188316",
            #     "iteration": 0,
            #     "problemId": 54209,
            #     "requestNumber": "INC-010174"
            # }
            logger.info(f'{userID} [getIssueTicket]  MgeniusResponse:' + str(response))

            Ticket_id_ = ''
            if response.get("code"):
                # print("error")
                resp = flask.Response(encrypt(response.get("message")))
                Ticket_id_ = response.get("message")
                print(Ticket_id_)
                resp.headers['Access-Control-Allow-Origin'] = '*'
            else:
                Ticket_id_ = response.get("requestNumber")
                print(Ticket_id_)

                for filenameattach in totalfile:
                    filearray = []
                    print('files--->', filenameattach)
                    filepath = 'temp/' + filenameattach

                    openfile = open(filepath, 'rb')
                    filedata = ('file', openfile)
                    filearray.append(filedata)

                    print("Filearray", filearray)

                    url = "https://mgenius.in/ITSMTool/Service/upload"
                    payload = {'requestNo': Ticket_id_,
                               'userName': userID,
                               'project': project_name}
                    files = filearray
                    headers = {
                        'int-log-id': 'qwertyasdfg',
                        'key': '2fb29d27-51a9-4074-82f5-45db3f450d24',
                        'token': '7560a221-28b3-4343-8848-2388fe788d51'
                    }
                    response = requests.request("POST", url, headers=headers, data=payload, verify=False, files=files)
                    print('resp txt---->', response.text)
                    openfile.close()
                    os.remove(os.path.join(app.config['UPLOAD_FOLDER'], filenameattach))


                resp = flask.Response(encrypt(
                    "Thank you, We have created Ticket for your issue.<br><b><center>Ticket ID&nbsp;<font size='5px' color='#174c82'>" + Ticket_id_ + "</font></center>"))
                resp.headers['Access-Control-Allow-Origin'] = '*'
                logger.info(
                    f'{userID} [getIssueTicket] Response:Thank you, We have created Ticket for your issue.<br><b><center>Ticket ID&nbsp;<font size="5px" color="#174c82">"'+Ticket_id_+'"</font></center>')

            print("Length of Ticket ID:", len(Ticket_id_))
            if len(Ticket_id_) < 20:
                if resolve.lower() == 'unanswered':
                    try:
                        getAnswered_query = "SELECT query_id FROM `unanswered_queries` where `username`='" + userName + "' order by`asked_on` desc LIMIT 1 "
                        uns = create_query(getAnswered_query)
                        print(uns[0][0])
                        queryid = uns[0][0]
                        print("queryid " + str(queryid))
                        if len(uns) > 0:
                            answered_query = "update unanswered_queries set `Ticket_id`='" + Ticket_id_ + "' where `query_id`=" + str(
                                queryid) + ""
                            print(answered_query)
                            uns = insertquery(answered_query)

                    except Exception as e:
                        logger.error(f'{userID} [getFinalResponse] Exception occurred', exc_info=True)
                        print("Exception Occured " + e)
                else:
                    try:
                        getAnswered_query = "SELECT query_id FROM `answered_queries` where `username`='" + userName + "' order by`asked_on` desc LIMIT 1 "
                        uns = create_query(getAnswered_query)
                        print(uns[0][0])
                        queryid = uns[0][0]
                        print("queryid " + str(queryid))
                        if len(uns) > 0:
                            answered_query = "update answered_queries set `Ticket_id`='" + Ticket_id_ + "' where `query_id`=" + str(
                                queryid) + ""
                            print(answered_query)
                            uns = insertquery(answered_query)

                    except Exception as e:
                        logger.error(f'{userID} [getFinalResponse] Exception occurred', exc_info=True)
                        print("Exception Occured " , e)
            return resp

        # return "Thank you, We have created Ticket for your issue.Your Ticket Id is: 10004"
        elif userResponse.lower() == 'no':  # if users issue did not resolves
            resp = flask.Response(encrypt("Thank you"))
            resp.headers['Access-Control-Allow-Origin'] = '*'
            return resp
            # return "Thank you"
    except Exception as e:
        logger.error(f'{userID} [getIssueTicket] Exception occurred', exc_info=True)
        traceback.print_exc()
        resp = flask.Response(encrypt(
            "Currently service not available"))
        resp.headers['Access-Control-Allow-Origin'] = '*'
        return resp


@app.route('/send_email', methods=["POST", "GET"])
def send_email():
    message = request.get_data()
    usermsg1 = decrypt(message)
    usermsg = json.loads(usermsg1)
    #usermsg = json.loads(message)
    username = usermsg.get('userName')
    userID = usermsg.get('userID')
    title = usermsg.get('title')  # user query
    userEmail = usermsg.get('userEmail')  # mobitrail.technology@gmail.com
    desc = usermsg.get('desc')
    userResponse = usermsg.get('userResponse')  # yes/no to send email
    response = usermsg.get('response')  # bot response

    print("send email data == ", usermsg)
   #logger.info(f'{userID} [get] Email Request:' + str(usermsg))

    if userResponse == "yes":
        if title in ["loss of pay","Loss of pay","Loss Of Pay","loss pay","Loss pay","Loss Pay"] :
            print("if of email")
            msg = Message(subject="Query about {} ".format(title), sender=userEmail,
                      recipients=['vedanti@mobitrail.com'])

            msg.body = "The employee Vikas Kedia (E10001) has a below-mentioned concern w.r.t his Loss of Pay.\n\n" \
                       "{0}\n\n" \
                       "Request you to please check and provide the appropiate resolution for the same. \n\n" \
                       "Regards \n\n" \
                       "SuperE \n" \
                       "(Experian Serive BOT)".format(desc)

        else:
            print("else of email")
            msg = Message(subject="Query about {} ".format(title), sender=userEmail,
                          recipients=['vedanti@mobitrail.com'])
            msg.body = "Dear Admin, \n\n" \
                       "User {0} is looking for the resolution for the below mentioned query. \n" \
                       "Query:- {1} \n" \
                       "BOT Response:- {2} \n" \
                       "Query Description:- {3} \n\n" \
                       "Request you to please check and provide the appropiate resolution for the same. \n\n" \
                       "Regards \n\n" \
                       "SuperE \n" \
                       "(Experian Serive BOT)".format(userID, title, response, desc)

     #   mail.send(msg)
        get_email_query = "SELECT `query_id` from `answered_queries` WHERE `username` = '" + username + "' AND `tabFeedBack` = '--' ORDER BY `asked_on` desc LIMIT 1 "
        uns = create_query(get_email_query)
        query_id = uns[0][0]
        if len(uns) > 0:
            answered_query = "UPDATE answered_queries SET email_sent = '" + userResponse + "'WHERE `query_id` = '" + str(
                query_id) + "'"
            insertquery(answered_query)
            print("email response ==== ", answered_query)
        json_data = {
            "message": "Email has been sent successfully!"
        }
        data = json.dumps(json_data)
        print("json data == ", data)
        resp = flask.Response(encrypt(data))
        #resp = flask.Response(data)

        return resp
    else:
        get_email_query = "SELECT `query_id` from `answered_queries` WHERE `username` = '" + username + "' AND `tabFeedBack` = '--' ORDER BY `asked_on` desc LIMIT 1 "
        uns = create_query(get_email_query)
        query_id = uns[0][0]
        if len(uns) > 0:
            answered_query = "UPDATE answered_queries SET email_sent = '" + userResponse + "'WHERE `query_id` = '" + str(
                query_id) + "'"
            insertquery(answered_query)
            print("email response ==== ", answered_query)
        json_data = {
            "message": "Thank you!"
        }
        data = json.dumps(json_data)
        print("json data == ", data)
        resp = flask.Response(encrypt(data))
        #resp = flask.Response(data)

        return resp

@app.route('/Rating',methods=["POST","GET"])
def get_feedback_rating():
    userdata1 = request.get_data()
    userdata = decrypt(userdata1)
    usertext = json.loads(userdata)
    print("rating data ==== ",usertext)
    username = usertext.get('userName')
    userID = usertext.get('userID')
    rating = usertext.get('rating')
    UserRespValue = usertext.get('issuevalue')
    RatingDesIssue = usertext.get('RatingDesIssue')
    mainIssue = usertext.get('mainIssue')
    query_id =""


   #logger.info(f'{userID} [Rating] Request:'+str(usertext))

    if RatingDesIssue == "" or RatingDesIssue == None:
        RatingDesIssue='-'
    RatingDesIssue = str(RatingDesIssue).replace("'","").replace("\\","")

    try:
        if str(UserRespValue).lower() == "yes":
            get_ans_query = "SELECT `query_id` FROM `answered_queries` WHERE `username` = '" + username + "' and `userID` = '" + userID + "' order by `asked_on` desc LIMIT 1"
            ans = create_query(get_ans_query)
            print(ans)
            query_id = ans[0][0]
            if len(ans) > 0:
                answered_query = "UPDATE `answered_queries` SET rating ='" + rating + "' , rating_feedback ='" + RatingDesIssue + "' WHERE query_id = '" + str(query_id) + "' and `feedback` = 'yes' "
                print(answered_query)
                insertquery(answered_query)

        elif str(UserRespValue).lower() == "no":
            get_ans_query = "SELECT `query_id` FROM `answered_queries` WHERE `username` = '" + username + "' and `userID` = '" + userID + "' and `feedback` = 'no' order by `asked_on` desc LIMIT 1"
            ans = create_query(get_ans_query)
            query_id = ans[0][0]
            if len(ans) > 0:
                answered_query = "UPDATE `answered_queries` SET `rating` ='" + rating + "' , `rating_feedback` ='" + RatingDesIssue + "' WHERE query_id = '" + str(query_id) +"'"
                print(answered_query)
                insertquery(answered_query)

        elif str(UserRespValue).lower() == "" or str(UserRespValue).lower() == None:
            get_ans_query = "SELECT `query_id` FROM `answered_queries` WHERE `username` = '" + username + "' and `userID` = '" + userID + "' order by `asked_on` desc LIMIT 1"
            ans = create_query(get_ans_query)
            query_id = ans[0][0]
            if len(ans) > 0:
                answered_query = "UPDATE `answered_queries` SET `rating` ='" + rating + "' , `rating_feedback` ='" + RatingDesIssue + "' WHERE query_id = '" + str(query_id) + "'"
                print(answered_query)
                insertquery(answered_query)

        else:
            get_ans_query = "SELECT `query_id` FROM `unanswered_queries` WHERE `username` = '" + username + "' and `userID` = '" + userID + "' order by `asked_on` desc LIMIT 1"
            ans = create_query(get_ans_query)
            query_id = ans[0][0]
            if len(ans) > 0:
                answered_query = "UPDATE `answered_queries` SET `rating` ='" + rating + "' , `rating_feedback` ='" + RatingDesIssue + "' WHERE query_id = '" + str(query_id) + "'"
                print(answered_query)
                insertquery(answered_query)
        resp = flask.Response(encrypt("Thank you for your feedback!"))
        #resp = flask.Response("Thank you for your feedback!")

       #logger.info(f'{userID} [Rating] Response: Thank you for your feedback' )
        return resp

    except Exception as e:
        print("Exception occured " +str(e))
        resp = flask.Response(encrypt("Thank you for your feedback!"))
        #resp = flask.Response("Thank you for your feedback!")

        return resp

jumpwords = set(parser.parserinfo.JUMP)
keywords = set(kw.lower() for kw in itertools.chain(
    parser.parserinfo.UTCZONE,
    parser.parserinfo.PERTAIN,
    (x for s in parser.parserinfo.WEEKDAYS for x in s),
    (x for s in parser.parserinfo.MONTHS for x in s),
    (x for s in parser.parserinfo.HMS for x in s),
    (x for s in parser.parserinfo.AMPM for x in s),
))

def parse_multiple(s):
    #print("parse str ===> ",s)
    def is_valid_kw(s):
        try:  # is it a number?
            float(s)
            return True
        except ValueError:
            return s.lower() in keywords

    def _split(s):
        kw_found = False
        tokens = parser._timelex.split(s)
        for i in xrange(len(tokens)):
            if tokens[i] in jumpwords:
                continue
            if not kw_found and is_valid_kw(tokens[i]):
                kw_found = True
                start = i
            elif kw_found and not is_valid_kw(tokens[i]):
                kw_found = False
                yield "".join(tokens[start:i])
        # handle date at end of input str
        if kw_found:
            yield "".join(tokens[start:])

    return [parser.parse(x) for x in _split(s)]

@app.route('/start1', methods=["POST", "GET"])
def start():
    while True:
        schedule.run_pending()

@app.route("/getrecommendation",methods= ["POST","GET"])
def get_recommendation_list():
    message1 = request.get_data()
    json_array = []

    query_data = create_query("select TitleRecommend from operations")
    tagsdata = list(query_data)
    json_array = []

    for t_list in tagsdata:
        recommend_list = t_list[0]
        if "Please enter the below details to raise a ticket" in recommend_list:
            pass
        else:
            json_array.append(recommend_list)
    print(json_array)
    resp = flask.Response(encrypt(str(json_array)))
    resp.headers['Access-Control-Allow-Origin'] = '*'
    return resp

def gettaglanguage(language):
    a={
        "gu":["ટેકનોલોજી","માનવ સંસાધન","વહીવટ"],
        "hi": ["प्रौद्योगिकी", "मानव संसाधन", "शासन प्रबंध"],
        "ml": ["സാങ്കേതികവിദ്യ", "മാനവ വിഭവശേഷി", "ഭരണകൂടം"],
        "mr": ["तंत्रज्ञान", "मानव संसाधन", "प्रशासन"],
        "ta": ["தொழில்நுட்பம்", "மனித வளம்", "நிர்வாகம்"],
        "te": ["సాంకేతికం", "మానవ వనరుల", "అడ్మినిస్ట్రేషన్"],
        "ur": ["ٹیکنالوجی", "انسانی وسائل", "انتظامیہ"],
        "pa": ["ਤਕਨਾਲੋਜੀ", "ਮਾਨਵ ਸੰਸਾਧਨ", "ਪ੍ਰਸ਼ਾਸਨ"],
    }
    taglist = a.get(language)
    return taglist

@app.route('/gettags_list', methods=["POST", "GET"])
def get_tag_list():

    userdata1 = request.get_data()
    print(userdata1)
    userdata = decrypt(userdata1)
    usertext = json.loads(userdata)
    print("user=========== ", usertext)
    userID = usertext.get('userID')
    user_token = usertext.get('userToken')
    username = usertext.get('userName')
    language = usertext.get('language')
    print("language========",language)
    print("user_token========", user_token)
    language_flag = False
    if language == "gu" or language == "hi" or language == "ml" or language == "mr" or language == "ta" or language == "te"  or language == "ur" or language == "pa":
        language_flag = True

    try:
        if user_token != "None" and user_token != "" and user_token != "null" and user_token != None:
            q = "select * from `notify_list` where `user_token` = '"+ user_token +"' "
            output = create_query(q)
            print(output)
            if len(output) == 0:
                query = "insert into `notify_list`(user_token,user_name,userID) values('" + str(user_token) + "','" + str(username) + "','" + str(userID) + "') "
                output = insertquery(query)
                print("token == ", output)

            print("tt==>",output)
        currentdate = datetime.now().strftime("%Y-%m-%d")
        print("++",currentdate)

        # for notification count
        query = "select * from notify  order by notification_id desc"
        output = create_query(query)
        tag_list = list(output)
        notification_count = len(tag_list)
        print("count",notification_count)
        print(tag_list)

            # to display todays reminder
        rem_query = "select * from reminder_detail where date = '" + str(currentdate) + "' and emp_id = '" + str(userID) + "' "
        output = create_query(rem_query)
        tags = list(output)
        rem_count = len(tags)

        survey_query = "select survey_id,title from survey where NOT EXISTS(select survey_id from survey_submit_details " \
                "where survey.survey_id = survey_submit_details.survey_id and survey_submit_details.emp_id = '" + userID + "')"
        survey_data = create_query(survey_query)
        survey_count = len(list(survey_data))
        print("++++++++++++++++++++++++++++++++++++++",language_flag)
        if rem_count > 0:
            if survey_count > 0:
                if language_flag:
                    tags_data = gettaglanguage(language)
                else:
                    tags_data = ["Technology", "Human Resource", "Administration","My Ticket Status"]
                json_array = []
                for x in tags_data:

                    sim = {
                        "title": x,
                        "desc": x
                    }
                    json_array.append(sim)
                json_data = {
                    "message": "",
                    "parameterTitle": "Listview",
                    "parameterType" : "reminder##rem##",
                    "notification_count": notification_count,
                    "suvey_status": "survey pending",
                    "action": json_array
                }
            else:
                if language_flag:
                    tags_data = gettaglanguage(language)
                else:
                    tags_data = ["Human Resource","My Ticket Status","My Documents"]
                json_array = []
                for x in tags_data:

                    sim = {
                        "title": x,
                        "desc": x
                    }
                    json_array.append(sim)
                json_data = {
                    "message": "",
                    "parameterTitle": "Listview",
                    "parameterType": "",
                    "notification_count": notification_count,
                    "suvey_status": "survey completed",
                    "action": json_array
                }
        else:
            if survey_count > 0:

                if language_flag:
                    tags_data = gettaglanguage(language)
                else:
                    tags_data = ["Technology", "Human Resource", "Administration","Show Ticket Status"]
                json_array = []
                for x in tags_data:

                    sim = {
                        "title": x,
                        "desc": x
                    }
                    json_array.append(sim)
                json_data = {
                    "message": "",
                    "parameterTitle": "Listview",
                    "parameterType": "reminder##rem##",
                    "notification_count": notification_count,
                    "suvey_status": "survey pending",
                    "action": json_array
                }
            else:
                if language_flag:
                    tags_data = gettaglanguage(language)
                else:
                    tags_data = ["Technology", "Human Resource", "Administration","Show Ticket Status"]
                json_array = []
                for x in tags_data:

                    sim = {
                        "title": x,
                        "desc": x
                    }
                    json_array.append(sim)
                json_data = {
                    "message": "",
                    "parameterTitle": "Listview",
                    "parameterType": "",
                    "notification_count": notification_count,
                    "suvey_status": "survey completed",
                    "action": json_array
                }


        data = json.dumps(json_data, sort_keys=True, indent=4 * ' ')
        print("json data == ", data)
        resp = flask.Response(encrypt(data))
        #resp = flask.Response(data)

        resp.headers['Access-Control-Allow-Origin'] = '*'
        return resp

    except Exception as e:
        logger.error(f'{userID} [insertLeave] Exception occurred', exc_info=True)

        print("Exception occured ", e)
        traceback.print_exc()
        return "somthing went wrong"

@app.route("/reopenClosedTicket",methods=["POST","GET"])
def reopen_closed_ticket():
    try:
        filestoragearray = []
        # posted_file = request.files['descAttachment']
        posted_file1 = request.files.getlist('descAttachmentOne', None)
        if posted_file1:
            filestoragearray.append(posted_file1)

        posted_file2 = request.files.getlist('descAttachmentTwo', None)
        if posted_file2:
            filestoragearray.append(posted_file2)

        posted_file3 = request.files.getlist('descAttachmentThree', None)
        if posted_file3:
            filestoragearray.append(posted_file3)

        totalfile = []

        for filedata in filestoragearray:
            for file in filedata:
                file.save(os.path.join(app.config['UPLOAD_FOLDER'], file.filename))
                file_name = file.filename
                totalfile.append(file_name)

        print('totalfiles ----> ', totalfile)

        bodycontent = request.form.to_dict()
        print("Bodycontent: ", bodycontent)
        if len(bodycontent) > 0:
            objectrecived = json.loads(decrypt(bodycontent['requestData']))
        else:
            message1 = request.get_data()
            message2 = decrypt(message1)
            objectrecived = json.loads(message2)

        print('obj---> ', objectrecived)


        userID = objectrecived.get('userID')
        ticket_id = objectrecived.get('ticket_id')
        description = objectrecived.get('description')

        json_data = {
            "message": "<b>"+ ticket_id + "</b> has been <b> Reopened </b>",
            "ParameterTitle": "",
            "action": "",
            "resolve": "",
            "rating": "no",
            "title": "",
            "mainIssue": "Technology",
            "response": "<b>"+ ticket_id + "</b> has been <b> Reopened </b>"
        }

        data1 = json.dumps(json_data, sort_keys=True, indent=4 * ' ')
        data = data1
        data2 = json.dumps(json_data)
        print("reopen tic api ---->", data2)
        #dbInsertion(temtext, data2, "query", username, userType, userID, "-1", mainIssue, "Technology", "-1")
        resp = flask.Response(encrypt(str(data)))
        resp.headers['Access-Control-Allow-Origin'] = '*'
        logger.info(f'{userID} [reopenClosedTicket] Response:' + str(json_data))
        return resp



    except Exception as e:
        logger.error(f'{userID} [reopenClosedTicket] Exception occurred', exc_info=True)
        traceback.print_exc()
        resp = flask.Response(encrypt(
            "Unable to reopen ticket"))
        resp.headers['Access-Control-Allow-Origin'] = '*'
        return resp



# schedule.every(2).minutes.do(get_tag_list)
# while True:
#     schedule.run_pending()
def translate_text(text,target='en'):
    """
    Target must be an ISO 639-1 language code.
    https://cloud.google.com/translate/docs/languages
    """
    print("Intranslation",text,target)
    translate_client = translate.Client()
    result = translate_client.translate(
        text,
        target_language=target)

    # print(u'Text: {}'.format(result['input']))
    # print(u'Translation: {}'.format()
    # print(u'Detected source language: {}'.format(
    #     result['detectedSourceLanguage']))
    return result['translatedText']

# def detect_lang(text):
#     """
#     Target must be an ISO 639-1 language code.
#     https://cloud.google.com/translate/docs/languages
#     """
#     print("in detect",text)
#     # translate_client = translate.Client()
#     #result = translate_client.detect_language(text)
#
#
#     return result['language']

def hasNumbers(inputString):
    return any(char.isdigit() for char in inputString)

# schedule.every(2).minutes.do(get_tag_list)
# while True:
#     schedule.run_pending()

def myFunc(e):
   return e['problemId']


if __name__ == "__main__":
    # app.run(host='192.168.0.159',port=6003, threaded=True)
    schedule.every().day.at("11:00").do(daily_notify)
    schedule.every(10).minutes.do(remind_notify)
    app.run(host='0.0.0.0', port=6004, threaded=True)

    # app.run(host='0.0.0.0', port=6004, threaded=True)