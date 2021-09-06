#Python libraries that we need to import for our bot

from __future__ import print_function
from flask import Flask, request, redirect,render_template,url_for
import json
import flask
from langdetect import detect
from chatterbot import ChatBot
from chatterbot.trainers import ChatterBotCorpusTrainer
import ssl
from model.MySQLHelper import insertquery, create_query
from flask_cors import CORS

from autocorrect import spell
import itertools
from dateutil import parser
from nltk import word_tokenize

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
from translate import Translator
from datetime import datetime, timedelta
from pyfcm import FCMNotification
import os.path
import pickle
from datetime import  timezone
import datefinder

import schedule
from dateparser.search import search_dates
from random import randint
import requests
#import schedule

app = Flask(__name__)


logger = logging.getLogger("Rotating Log")
logger.setLevel(logging.INFO)
handler = TimedRotatingFileHandler('log//bot.log', when='midnight', interval=1, backupCount=10)
# create console handler and set leve to debug
handler = logging.FileHandler('log//bot.log'.format(datetime.now()))
# create formatter
formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
handler.setFormatter(formatter)
logger.addHandler(handler)

video_path_BaseURL="https://mgenius.in/mobitrail/DemoBot/Video"
#image_path_BAseURL="http://mgenius.in/IIFLBotHtml/iiflimages/"
image_path_BAseURL = "https://askpanda.iifl.in/ServiceBot/iiflimages/"
scopes = ['https://www.googleapis.com/auth/calendar']
BasePathAttachment = "https://8162aae4defc.ngrok.io/static/notifications_attachments/"
BasePathDocumnets = "https://8162aae4defc.ngrok.io/static/document_files/"


image_path_BAseURL = "https://askpanda.iifl.in/ServiceBot/iiflimages/"
video_path_BaseURL = "https://askpanda.iifl.in/ServiceBot/iiflvideos/"
garbage_list = ["kindly", "Actually", "dear", "are", "employee", "about", "above", "across", "after", "afterwards",
                "help", "Dear", "asap", "solve",
                "again", "against", "all", "almost", "alone", "along", "already", "also", "although", "always",
                "among", "amongst", "amoungst", "amount", "an ", "and", "another", "any", "anyhow", "anyone",
                "anything",
                "anyway", "anywhere", "are", "around", "as", "at", "back", "be", "became", "because", "become",
                "becomes", "becoming", "been", "before", "beforehand", "behind", "being", "below", "beside", "besides",
                "between", "beyond", "bill", "both", "bottom", "but", "by", "call", "can", "co",
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
                "no", "nobody", "none", "noone", "nor", "nothing", "now", "nowhere", "of", "off", "often", "on",
                "once", "one", "only", "onto", "or", "other", "others", "otherwise", "our", "ours", "ourselves", "out",
                "over", "own", "part", "per", "perhaps", "please", "put", "rather", "re", "same", "see", "seem",
                "seemed", "seeming", "seems", "serious", "several", "she", "should", "show", "side", "since", "sincere",
                "six", "sixty", "so", "some", "somehow", "someone", "something", "sometime", "sometimes", "somewhere",
                "still", "such", "ten", "than", "that", "the", "their", "them", "themselves", "then",
                "thence", "there", "thereafter", "thereby", "therefore", "therein", "thereupon", "these", "they",
                "thickv", "thin", "third", "this", "those", "though", "three", "through", "throughout", "thru", "thus",
                "to", "together", "too", "top", "toward", "towards", "twelve", "twenty", "two", "un", "under", "until",
                "up", "upon", "us", "very", "via", "was", "we", "well", "were", "what", "whatever", "when", "whence",
                "whenever", "where", "whereafter", "whereas", "whereby", "wherein", "whereupon", "wherever", "whether",
                "which", "while", "whither", "who", "whoever", "whole", "whom", "whose", "why", "will", "with",
                "within", "without", "would", "yet", "you", "your", "yours", "yourself", "yourselves", "the", "facing",
                "Assist"
    , "resolve", "Resolve", "resolv", "resolved", "pls", "please", "resolution", "looking", "look", "solution", "issue",
                "issues", "issu"
    , "isue", "problem", "problm", "prblm", "assist", "asist", "assit", "Problem", "Issue", "Issues", "Problems",
                "problems", "u", "U", "resolving"
    , "working", "work", "hey", "error", "eror", "unable", "properly", "proper", "properer", "plss", "want", "let",
                "Tell", "tell"]
stopwordsss = ['i', 'me', 'my', 'myself', 'we', 'our', 'ours', 'ourselves', 'you', "you're", "you've", "you'll",
               "you'd", 'your', 'yours', 'yourself', 'yourselves', 'he', 'him', 'his', 'himself', 'she', "she's", 'her',
               'hers', 'herself', 'it', "it's", 'its', 'itself', 'they', 'them', 'their', 'theirs', 'themselves',
               'what', 'which', 'who', 'whom', 'this', 'that', "that'll", 'these', 'those', 'am', 'is', 'are', 'was',
               'were', 'be', 'been', 'being', 'have', 'has', 'had', 'having', 'do', 'does', 'did', 'doing', 'an', 'the',
               'and', 'but', 'if', 'or', 'because', 'as', 'until', 'while', 'of', 'at', 'by', 'for', 'with', 'about',
               'against', 'between', 'into', 'through', 'during', 'before', 'after', 'above', 'below', 'to', 'from',
               'up', 'down', 'in', 'out', 'on', 'off', 'over', 'under', 'again', 'further', 'then', 'once', 'here',
               'there', 'when', 'where', 'why', 'how', 'all', 'any', 'both', 'each', 'few', 'more', 'most', 'other',
               'some', 'such', 'no', 'nor', 'not', 'only', 'own', 'same', 'so', 'than', 'too', 'very', 's', 't', 'can',
               'will', 'just', 'don', "don't", 'should', "should've", 'now', 'd', 'll', 'm', 'o', 're', 've', 'y',
               'ain', 'aren', "aren't", 'couldn', "couldn't", 'didn', "didn't", 'doesn', "doesn't", 'hadn', "hadn't",
               'hasn', "hasn't", 'haven', "haven't", 'isn', "isn't", 'ma', 'mightn', "mightn't", 'mustn', "mustn't",
               'needn', "needn't", 'shan', "shan't", 'shouldn', "shouldn't", 'wasn', "wasn't", 'weren', "weren't",
               'won', "won't", 'wouldn', "wouldn't"]
stop_words = set(garbage_list)
stop_words.update(stopwordsss)

english_bot = ChatBot("Chatterbot", storage_adapter="chatterbot.storage.MongoDatabaseAdapter")
english_bot.set_trainer(ChatterBotCorpusTrainer)
# corpus file C:\Users\pushpak\AppData\Local\Continuum\anaconda3\Lib\site-packages\chatterbot_corpus\data
english_bot.train("chatterbot.corpus.ExperianBot")
english_bot.read_only = True
requiredset = ["need mouse", "required mouse", "mouse need", "mouse required", "need keyboard", "required keyboard",
               "require keyboard",
               "keyboard need", "keyboard required", "keyboard require", "mouse require", "get mouse", "get keyboard",
               "find keyboard", "find mouse"]
arr = ["crm", "iifl", "zoho", "Weightage","nbfc","otp","gmail","GMAIL","onekey","Lenovo","lenovo"]


obj = []
serviceurl = "https://hooks.slack.com/services/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"
# serviceurl = "https://hooks.slack.com/services/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"

@app.route("/msg", methods=['GET', 'POST'])
def receive_message():
    print("in msg")
    req = request.get_json()
    if 'challenge' in req:
        req1 = req['challenge']
        return req1
    if req not in obj:
        abc = req['event']
        print(abc)
        msg=abc['text']
        user = abc['user']


        usertext = msg
        print("user query = ", usertext)
        username = "Pushpak"
        userID = "1003"
        temtext = msg  # storing original text value
        platform = "Slack"
        locationId = "Mumbai"
        userType = "Type"


        if 'subtype' in abc:
            return "True"
        else:
            print(req)
            # res = {"text": "HI"}
            # print(res)
            # a = requests.post(serviceurl, data=json.dumps(res), headers={"Content-type": "application/json"})
            # print(a)
            # return "hello"
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

            try:
                meetingFlag = False
                callFlag = False

                if "meeting" in usertext.lower():
                    meetingFlag = True
                elif "call" in usertext.lower():
                    callFlag = True
                rem_type = chkFlags(meetingFlag, callFlag)
                print("rem type==", rem_type)

                if usertext.lower() == "":

                    if "help" in str(temtext).lower():
                        json_data = {
                            "error": "Sure, can you please enter the issue your are facing.",
                            "operation_id": "",
                            "response": "Sure, can you please enter the issue your are facing.",
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
                            "emailFlag": ""

                        }
                        data = json.dumps(json_data)
                        print("json data = ", data)
                        dbInsertion(temtext, data, "answered", username, userType, userID, "-1", "Greetings","-1")

                        res = {"text": "Sure, can you please enter the issue your are facing."}
                        # print(res)
                        a = requests.post(serviceurl, data=json.dumps(res), headers={"Content-type": "application/json"})

                        logger.info(f'{userID} [get] Response:' + str(json_data))
                        return "hello"

                    # usertext is empty hence taking original text through temtext
                    elif str(temtext).lower() in ["how are you", "how are you?", "how r you?", "how r you", "how r u",
                                                  "how r u?",
                                                  "hows u?"]:

                        # print("elif loop")
                        json_data = {
                            "error": "I am fine",
                            "cat1": "Greetings",
                            "cat2": "",
                            "cat3": "",
                            "project_name": ""
                        }
                        data = json.dumps(json_data)
                        print("json data = ", data)
                        dbInsertion(temtext, data, "answered", username, userType, userID, "-1","Greetings",
                                    "-1")
                        res = {"text": "I am fine"}
                        # print(res)
                        a = requests.post(serviceurl, data=json.dumps(res),headers={"Content-type": "application/json"})

                        logger.info(f'{userID} [get] Response:' + str(json_data))
                        return "Hello"

                    elif str(temtext).lower() in ["who are you", "what is your name", "who r u?", "who are you?",
                                                  "who are u",
                                                  "whos this"]:
                        json_data = {
                            "error": "I am SuperE - Service BoT - the Company Service Bot :)",
                            "cat1": "Greetings",
                            "cat2": "",
                            "cat3": "",
                            "project_name": "",
                        }
                        data = json.dumps(json_data)
                        print("json data = ", data)
                        dbInsertion(temtext, data, "answered", username, userType, userID, "-1","Greetings",
                                    "-1")

                        res = {"text": "I am SuperE - Service BoT - the Company Service Bot :)"}
                        # print(res)
                        a = requests.post(serviceurl, data=json.dumps(res),headers={"Content-type": "application/json"})

                        logger.info(f'{userID} [get] Response:' + str(json_data))
                        return "Hello"

                    else:
                        json_data = {
                            "error": "I am sorry I could not resolve your issue.Would you like to send a mail to Help Desk Team? ",
                            "operation_id": "",
                            "response": "I am sorry I could not resolve your issue.Would you like to send a mail to Help Desk Team?",
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
                            "emailFlag": ""

                        }
                        # print("else",type(json_data))
                        data = json.dumps(json_data)
                        print("json data = ", data)
                        dbInsertion(temtext, data, "unanswered", username, userType, userID, "-1",
                                    "Greetings", "-1")
                        res = {"text": "I am sorry I could not resolve your issue.Would you like to send a mail to Help Desk Team? "}
                        # print(res)
                        a = requests.post(serviceurl, data=json.dumps(res),headers={"Content-type": "application/json"})

                        logger.info(f'{userID} [get] Response:' + str(json_data))
                        return "Hello"

                print("Origional Usertext ====> ", usertext)
                bot_resp = english_bot.get_response(usertext)
                # print(bot_resp)
                bot_confidence = bot_resp.confidence
                print("Confidence = ", bot_confidence)
                print("Response ====> ", bot_resp)
                bot_data = str(bot_resp)
                flag = False
                matchText = ""
                thirdvar = ""

                if '|' in bot_data:  # pipe separation
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
                    print("Response with sql query ==> ", bot_data)

                elif "Admin_default" in bot_data:
                    json_data = {
                        "message": "Kindly contact your Local HR Admin.",
                        "operation_id": "",
                        "response": "Kindly contact your Local HR Admin.",
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
                        "emailFlag": ""
                    }
                    data1 = json.dumps(json_data, sort_keys=True, indent=4 * ' ')
                    data = data1
                    data2 = json.dumps(json_data)
                    dbInsertion(temtext, data2, "answered", username, userType, userID, "-1", "--", "-1")
                    res = {
                        "text": "Kindly contact your Local HR Admin."}
                    # print(res)
                    a = requests.post(serviceurl, data=json.dumps(res), headers={"Content-type": "application/json"})

                    logger.info(f'{userID} [get] Response:' + str(json_data))
                    return "Hello"
                else:
                    if bot_confidence >= 0.80:
                        flag = True

                print("Usertext == ", usertext)
                print("flag == ", flag)
                print("bot confidence == ", bot_confidence)

                if flag:
                    if bot_data == "ERROR":
                        print("if error")
                        json_data = {
                            "error": "I am sorry, we could not find a solution for your reported issue. Would you like to send a mail to Help Desk Team?",
                            "cat1": "Application Services",
                            "cat2": "Applications",
                            "resolve": "",
                            "rating": "err",
                            "project_name": "MobitrailBot"
                        }
                        data1 = json.dumps(json_data, sort_keys=True, indent=4 * ' ')
                        print("json data = ", data1)
                        data = data1
                        data2 = json.dumps(json_data)
                        dbInsertion(temtext, data2, "answered", username, userType, userID, "-1","--", "-1")
                        res = {
                            "text": "I am sorry, we could not find a solution for your reported issue. Would you like to send a mail to Help Desk Team?"}
                        # print(res)
                        a = requests.post(serviceurl, data=json.dumps(res),
                                          headers={"Content-type": "application/json"})

                        logger.info(f'{userID} [get] Response:' + str(json_data))
                        return "Hello"

                    elif "select" in bot_data:  # if data has sql query
                        print("if select")
                        output = create_query(bot_data)
                        tag_list = list(output)
                        print("list == ", tag_list)
                        json_array = []
                        lastFlag = False
                        typetext = ""
                        category = ""
                        emailFlag = False
                        for t_list in tag_list:
                            print("in for loop")
                            for idx, title in enumerate(t_list):
                                print(idx, ",", title)
                                if len(t_list) == 2:
                                    print("length is 2")
                                    if idx == 0:
                                        arr = {
                                            "desc": title
                                        }
                                        json_array.append(arr)
                                        data1 = json.dumps(json_array)
                                        data = data1
                                        print("json data = ", data)
                                    if idx == 1:
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
                                                sim = {
                                                    "desc": id_op[0]
                                                    }
                                                json_array.append(sim)

                                            elif "$" in i:
                                                id_main_op = i.split("$")
                                                # print("id main op ", id_main_op)
                                                sim = {
                                                    "desc": id_main_op[0]
                                                    }
                                                json_array.append(sim)

                                            else:
                                                sim = {
                                                    "desc": i
                                                }
                                                json_array.append(sim)

                                        json_data = {
                                            "message": "I would be happy to tell you more. What would you like to know about " + str(
                                                t_list[7]),
                                            "action": json_array,
                                            "typetext": "HR",
                                            "ParameterTitle": "ListView",
                                            "mainIssue": "HR"
                                        }
                                        data1 = json.dumps(json_data, sort_keys=True, indent=4 * ' ')
                                        print("json data == ", data1)
                                        data = data1
                                        data2 = json.dumps(json_data)
                                        dbInsertion(temtext, data2, "answered", username, userType, userID, "-1","HR", "-1")

                                        data_arr = "I would be happy to tell you more. What would you like to know about " + str(
                                                t_list[7])
                                        count = 0
                                        for i in json_array:
                                            if data_arr != "":
                                                count += 1
                                                if count == 1:
                                                    data_arr = data_arr + '\n\n' + str(count) + "." + str(i['desc'])
                                                else:
                                                    data_arr = data_arr + ' ' + '\n' + ' ' + str(count) + "." + str(
                                                        i['desc'])
                                        print(data_arr)

                                        res = {"text": data_arr}
                                        # print(res)
                                        a = requests.post(serviceurl, data=json.dumps(res),
                                                          headers={"Content-type": "application/json"})

                                        logger.info(f'{userID} [get] Response:' + str(json_data))
                                        return "Hello"

                                if len(t_list) == 9:
                                    print("length is 9 ")
                                    if str(t_list[3]) == "HR":
                                        typetext = "HR"
                                        category = "HR"
                                    elif str(t_list[3]) == "Admin":
                                        typetext = "Administration"
                                        category = "Admin"
                                    else:
                                        typetext = "Technology"
                                        category = "Technology"

                                    query_response = str(t_list[6])
                                    regex = '([\w+-]+@[\w-]+\.[\w\.-]+)'
                                    email = re.search(regex, query_response)
                                    if email:
                                        emailFlag = True
                                    print("Email flag == ", emailFlag)

                                    video_path = t_list[7]
                                    if video_path == None or video_path == "":
                                        video_path = ""
                                    else:
                                        video_path = video_path_BaseURL + video_path
                                    query_response = query_response.replace("##LINK##", image_path_BAseURL)

                                    queryResponse = query_response.replace("##LINK##", image_path_BAseURL)

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
                                        "emailFlag": emailFlag
                                    }
                                    lastFlag = True
                                    data1 = json.dumps(json_data, sort_keys=True, indent=4 * ' ')
                                    print("json data = ", data1)
                                    data = data1
                                    data2 = json.dumps(json_data)
                                    dbInsertion(temtext, data2, "answered", username, userType, userID, "-1",category, "-1")
                                    res = {"text": query_response}
                                    # print(res)
                                    a = requests.post(serviceurl, data=json.dumps(res),
                                                      headers={"Content-type": "application/json"})

                                    return "Hello"

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
                                    "typetext": typetext,
                                }
                            data1 = json.dumps(json_data, sort_keys=True, indent=4 * ' ')
                            print("json data = ", data1)
                            data = data1
                            data2 = json.dumps(json_data)
                            dbInsertion(temtext, data2, "answered", username, userType, userID, "-1", category, "-1")

                            data_arr = "I would be happy to tell you more. What would you like to know about " + str(head)
                            count = 0
                            for i in json_array:
                                if data_arr != "":
                                    count += 1
                                    if count == 1:
                                        data_arr = data_arr + '\n\n' + str(count) + "." + str(i['desc'])
                                    else:
                                        data_arr = data_arr + ' ' + '\n' + ' ' + str(count) + "." + str(
                                            i['desc'])
                            print(data_arr)

                            res = {"text": data_arr}
                            # print(res)
                            a = requests.post(serviceurl, data=json.dumps(res),
                                              headers={"Content-type": "application/json"})

                            logger.info(f'{userID} [get] Response:' + str(json_data))
                            return "hello"

                    else:
                        json_data = {
                            "error": "We are sorry that we could not resolve your issue. Would you like to send a mail to the Help Desk Team?",
                            "resolve": "",
                            "rating": "no"
                        }

                        # print(json_data)
                        data1 = json.dumps(json_data, sort_keys=True, indent=4 * ' ')
                        data = data1
                        # print(data)
                        data2 = json.dumps(json_data)
                        # dbInsertion(temtext, "EXCEPTION OCCURED " + data2 + " " + str(e), "unanswered", username, userType,
                        #             userID,
                        #             "-1", mainIssue, "--", "-1")
                        traceback.print_exc()
                        # print("Exception occured ",e)

                        res = {
                            "text": "We are sorry that we could not resolve your issue. Would you like to send a mail to the Help Desk Team?"}
                        # print(res)
                        a = requests.post(serviceurl, data=json.dumps(res),
                                          headers={"Content-type": "application/json"})
                        logger.info(f'{userID} [get] Response:' + str(json_data))
                        return "Hello"  # translations[0].tbankoperation16ext)

            except Exception as e:
                logger.error(f'{userID} [get] Excepyion occured', exc_info=True)
                json_data = {
                    "error": "We are sorry that we could not resolve your issue. Would you like to send a mail to the Help Desk Team?",
                    "resolve": "",
                    "rating": "no"
                }

                # print(json_data)
                data1 = json.dumps(json_data, sort_keys=True, indent=4 * ' ')
                data = data1
                # print(data)
                data2 = json.dumps(json_data)
                # dbInsertion(temtext, "EXCEPTION OCCURED " + data2 + " " + str(e), "unanswered", username, userType,
                #             userID,
                #             "-1", mainIssue, "--", "-1")
                traceback.print_exc()
                # print("Exception occured ",e)

                res = {
                    "text": "We are sorry that we could not resolve your issue. Would you like to send a mail to the Help Desk Team?"}
                # print(res)
                a = requests.post(serviceurl, data=json.dumps(res), headers={"Content-type": "application/json"})
                logger.info(f'{userID} [get] Response:' + str(json_data))
                return "Hello"  # translations[0].tbankoperation16ext)

def chkFlags(meetingFlag, callFlag):
    if meetingFlag:
        type = "meeting"
    elif callFlag:
        type = "call"
    else:
        type = ""
    return type

def dbInsertion(usertext, response, flag, username, userType, userID, feedback,category, emailSent):
    print("db fun" + "-" * 50)
    print(usertext, response, flag, username, userType, userID, feedback,category, emailSent)
    try:
        print("db flag==", flag)
        usertext = str(usertext).replace("'", "").replace("\\", "")
        response = response.replace('src=\\"', "src=\'\'").replace('.jpg\\"', ".jpg\'\'").replace("'", "''")
        print("res==", response)
        currenttime = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        resptime = (datetime.now() + timedelta(seconds=3)).strftime("%Y-%m-%d %H:%M:%S")
        print(currenttime, "== ", resptime)
        requestFlag = False
        respFlag = False
        if usertext != "":
            print("in req")
            requestFlag = True
            historyFlag = "request"
            insertHistory(currenttime, usertext, historyFlag, username, userID)

        if response != "":
            print("in resp")
            respFlag = True
            historyFlag = "response"
            insertHistory(resptime, response, historyFlag, username, userID)

        # usertext = str(usertext).replace("'", "").replace("\\", "")
        print("flag=>", flag)
        if flag.lower() == "unanswered":
            unanswered_query = "insert into unanswered_queries" \
                               "(query,asked_on,username,userType,userid)" \
                               "values('" + str(usertext) + "','" + currenttime + "','" + str(username) + "','" + str(
                userType) + "','" + str(
                userID) + "')"
            print("unanswered query = ", unanswered_query)
            insertquery(unanswered_query)
            inserted_data = create_query("SELECT * FROM `unanswered_queries` where `username` = '" + str(
                username) + "' order by `asked_on` desc LIMIT 1")
            print("####@@", inserted_data)


        else:
            # response = response.replace('\'', '\\"')

            answered_query = "insert into answered_queries" \
                             "(query,asked_on,username,userType,query_answer,userID,feedback,category,email_sent)" \
                             "values('" + str(usertext) + "','" + currenttime + "','" + str(username) + "','" + str(
                userType) + "','" + str(
                response) + "','" + str(userID) + "','" + str(feedback) + "','" + str(category) + "','" + str(
                emailSent) + "')"
            print("answered query = ", answered_query)
            insertquery(answered_query)
            inserted_data = create_query("SELECT * FROM `answered_queries` where `username` = '" + str(
                username) + "' order by `asked_on` desc LIMIT 1 ")
            print("====", inserted_data)

    except Exception as e:
        print("Exception occur ", e)


def insertHistory(time, query, flag, username, userID):
    query = "insert into chat_history(asked_on,query,flag,username,userID)" \
            "values('" + str(time) + "','" + str(query) + "','" + flag + "','" + username + "','" + userID + "')"
    print("add==", insertquery(query))

@app.route("/group", methods=['GET', 'POST'])
def receive_message1():
    if request.method == 'GET':
      print("hi")
    else:
        # get whatever message a user sent the bot
        # groupobj = request.POST.get['payload']
        # print(groupobj)
        print(request.get_json())
        print(request.form)
        print("+++++++++++++++++")
        bodycontent = request.form
        # print(bodycontent)
        objectrecived = json.loads(bodycontent['payload'])

        user= objectrecived.get('user')
        token = objectrecived.get('token')
        channel = objectrecived.get('channel')
        response_url = objectrecived.get('response_url')
        actions = objectrecived.get('actions')
        respon = actions[0].get('text').get('text')
        print("user",user)
        print("token",token)
        print("channel",channel)
        print("response_url",response_url)
        print("respon",respon)
        if respon == "Yes":
            res= {"text":"Approved"}

        if respon == "No":
            res= {"text":"Rejected"}
        print(res)
        a = requests.post(serviceurl,data=json.dumps(res),headers={"Content-type":"application/json"})
        print(a)
        return "Approved"




if __name__ == "__main__":
    app.run()