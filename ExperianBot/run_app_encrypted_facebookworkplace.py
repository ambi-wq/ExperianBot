#Python libraries that we need to import for our bot
import os
import random
import sys
import traceback
from datetime import datetime
from logging.handlers import TimedRotatingFileHandler
from random import randint
from autocorrect import spell
from chatterbot.parsing import regex
from flask import Flask, request, json
from fuzzywuzzy import fuzz
from nltk import word_tokenize, re
from pymessenger.bot import Bot
from chatterbot import ChatBot
import requests
from urllib.parse import urlparse
from pathlib import Path
from chatterbot.trainers import ChatterBotCorpusTrainer
from model.MySQLHelper import insertquery, create_query
import logging.handlers

logger = logging.getLogger("Rotating Log")
logger.setLevel(logging.INFO)
handler = TimedRotatingFileHandler('log//bot.log',
                                   when="midnight",
                                   interval=1,
                                   backupCount=10)
# create console handler and set level to debug
handler = logging.FileHandler('log//bot.log'.format(datetime.now()))

# create formatter
formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
# add formatter to ch
handler.setFormatter(formatter)
# add ch to logger
logger.addHandler(handler)


app = Flask(__name__)

# Access token for Ask panda for IIFL (mgenius)
#ACCESS_TOKEN = 'DQVJzMWY1V2ZAnUHkxc0FpeUtXaVE4OXRvd0lLa2NtNkhuYXRHVWh5OGZA0c3gxT0s2dXVtWnZAkQzU3cGdxR2JlbzUxRk9mY3BOVFpuQWlMZAk9Gb2xXaHRJdWp1R0JvVUZA4ZAXBNN3BuLXNQdW9KRnJreFQwejVBUlVxV2dPSXE2YTh6eVNILVR2UnJ6TkY4NW96dXpGNE5Ya1RtSWwyY29EdGRNZA1I4enU1RG15Vi1lRXpjdzhnTngtNzVFN09jSXdHbGN3cWJn'
# Access token for Mobitrail Ask panda
ACCESS_TOKEN = 'DQVJ0VkZAhQnpZAVEFKeWxoOXlrNjJtdWtHYV92TWQ1dE9fQzZABd0ZAKUGxGbk9UZA3BUaGtDNkdLQUpsV0hGaFlpdEd6djlMVTBRZAldkT2lpSkRrNFdNS2tJaWd0dTAtNWlCUzE1ZAHdBcVotbXgyZA1JqcVk4clFrMm9HMGw1RHFTRHNfMXBuUXdVMTcwSTFYcG81eUZAoUnNwV1o0cUhMZAUFNamo3MEdvMkpwV1dfRS1WWW1XQmRfSjA2ZAWJFZA25PYTJSMEY5VW5n'
VERIFY_TOKEN = 'c88dca673c2190ceaed3c7652a946baf'
#VERIFY_TOKEN = 'EUWKPmK3cdEUWKPmK3cd'
auth = {
                'access_token': ACCESS_TOKEN
            }
bot = Bot(ACCESS_TOKEN)

UPLOAD_FOLDER = 'Temp'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

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

english_bot = ChatBot("Chatterbot", storage_adapter="chatterbot.storage.MongoDatabaseAdapter", database = "IIFLBOT_facebookWorkplace")
english_bot.set_trainer(ChatterBotCorpusTrainer)
# corpus file C:\Users\pushpak\AppData\Local\Continuum\anaconda3\Lib\site-packages\chatterbot_corpus\data
english_bot.train("chatterbot.corpus.system")
english_bot.read_only = True
requiredset = ["need mouse", "required mouse", "mouse need", "mouse required", "need keyboard", "required keyboard",
               "require keyboard",
               "keyboard need", "keyboard required", "keyboard require", "mouse require", "get mouse", "get keyboard",
               "find keyboard", "find mouse"]
arr = ["crm", "iifl", "zoho", "Weightage","nbfc","otp","gmail","GMAIL","onekey","Lenovo","lenovo"]


#We will receive messages that Facebook sends our bot at this endpoint
# @app.route("/", methods=['GET', 'POST'])
# def receive_message():
#     if request.method == 'GET':
#         """Before allowing people to message your bot, Facebook has implemented a verify token
#         that confirms all requests that your bot receives came from Facebook."""
#         token_sent = request.args.get("hub.verify_token")
#         return verify_fb_token(token_sent)
#     #if the request was not get, it must be POST and we can just proceed with sending a message back to user
#     else:
#         # get whatever message a user sent the bot
#        output = request.get_json()
#        print(output)
#        for event in output['entry']:
#           messaging = event['messaging']
#           for message in messaging:
#             if message.get('message'):
#                 #Facebook Messenger ID for user so we know where to send response back to
#
#                 recipient_id = message['sender']['id']
#                 print("_________________")
#                 print(recipient_id)
#                 print("_________________")
#                 if message['message'].get('text'):
#
#                     response_sent_text = "Hello, Click on the below option to continue the chat with AskPanda"
#                     # send_image_mess(recipient_id, "a")
#                     send_message(recipient_id, response_sent_text)
#                 #if user sends us a GIF, photo,video, or any other non-text item
#                 if message['message'].get('attachments'):
#                     response_sent_nontext = get_message()
#                     response_sent_text = "Hello,Talk to Ask Panda with the link below:"
#                     send_message(recipient_id, response_sent_text)
#     return "Message Processed"

tmp = []
post_data = {}
@app.route("/group", methods=['GET', 'POST'])
def receive_message1():
    if request.method == 'GET':
        """Before allowing people to message your bot, Facebook has implemented a verify token
        that confirms all requests that your bot receives came from Facebook."""
        token_sent = request.args.get("hub.verify_token")
        return verify_fb_token(token_sent)
    # if the request was not get, it must be POST and we can just proceed with sending a message back to user
    else:
        # get whatever message a user sent the bot
        print("-------------------------------")
        usertext = ""
        flag = ""
        parent_id = ""
        groupobj = request.get_json()
        print(groupobj)

        if groupobj not in tmp:

            tmp.append(groupobj)

            groupobj = groupobj['entry'][0]
            #print(groupobj)
            grpid = groupobj['id']
            #print("group id:", grpid)
            #
            grp_changes = groupobj['changes'][0]
            #print("from :",grp_changes)

            grp_value = grp_changes['value']
            #print(grp_value)
            msg = grp_value['message']
            print("msg :", msg)
            message_len = len(msg)

            verb =  grp_value['verb']
            print("Verb-------",verb)

            if verb == "add":

                uname = grp_value['from']
                userID = uname['id']
                userName = uname['name']
                print("Username",userName,"\n\n\n")

                if userName == "Mobitrail Ask Panda":
                    return "Success"
                else:

                    # comment_id = grp_value['comment_id']
                    # print("------comment_id------------------:", comment_id)
                    post_id = grp_value['post_id']
                    print("post_id :", post_id)

                    _temp_post_id = post_id

                    _from = grp_value['from']
                    _userid = _from['id']
                    _username = _from['name']
                    file_url = ""
                    parent_message = ""

                    try:
                        parent = grp_value['parent']
                        parent_id = parent['id']
                        post_id = parent_id
                        parent_message = parent['message']
                    except KeyError:
                        print("Keyerror")
                        pass

                    try:
                        attach = grp_value['attachments']
                        attach_type = attach['type']
                        if attach_type == 'file_upload':
                            file_title = attach['title']
                            file_url = attach['url']
                        elif attach_type == 'photo':
                            media = attach['media']
                            image = media['image']
                            file_url = image['src']
                        else:
                            pass
                    except KeyError:
                        print("URLKeyerror")
                        pass

                    temtext = msg
                    platform = "Facebook Workplace"

                    flag = ""

                    if "INC" in msg.upper():
                        get_tic_status (userName,msg,post_id)
                        return "Success"
                    elif "SR" in msg.upper():
                        get_tic_status(userName,msg,post_id)
                        return "Success"

                    if msg == "1" or msg == "2" or msg == "3" or msg == "4" or msg == "5":
                        Rating(userName,userID,msg,post_id)
                        return "Success"


                    if msg.lower() == "yes":
                        print("Yes")

                        if parent_message == "Kindly raise a new ticket(Yes / No)?":
                            print("Kindly raise a new ticket:= Yes")
                            grpurl = "https://graph.workplace.com/" + post_id + "/comments"
                            y = {
                                'message': "Can you please elaborate the issue/ request you wanted to report"
                            }
                            print("----------------+---------------============++++payload:", y)
                            response = requests.post(
                                grpurl,
                                params=auth,
                                json=y
                            )
                            print("-------------------Response:-", response)
                            return "Success"

                        # print(post_data)
                        if str(_temp_post_id) in post_data.keys():
                            print("_______________________________________")
                            print(post_data[str(_temp_post_id)])


                            ticket_res_data = post_data[str(_temp_post_id)]
                            print(ticket_res_data)
                            print(type(ticket_res_data))

                            grpurl = "https://graph.facebook.com/"+ post_id +"/comments?summary=1&filter=toplevel&access_token="+ str(ACCESS_TOKEN)
                            response = requests.get(
                                grpurl,
                                params=auth
                            )
                            # print(response)
                            # print(response.text)

                            response_data = json.loads(response.text)
                            # print(response_data)
                            # print(type(response_data))
                            resp_arr = response_data['data']
                            print("----------resparr-------",resp_arr)

                            count = 0
                            for h in reversed(resp_arr):
                                count += 1
                                if count < 3 :
                                    if h['message'] == 'We are sorry that we could not resolve your issue. Would you like to raise a ticket to the technical team (Yes / No)?':
                                        flag = "final_Ticket_creation"
                                        break
                                    elif h['message'] == "Kindly raise a new ticket(Yes / No)?":
                                        flag = "final_Ticket_creation"
                                        break
                                    else:
                                        flag = "Issue_Resolved"
                                        pass

                            if flag == "Issue_Resolved":
                                print("Is the Issued Resolved:-Yes")
                                user_response = "Yes"
                                return_ticket_res = Create_Update_ticket(ticket_res_data,userID,userName,user_response,post_id)
                                return "Success"
                            else:
                                print("GetIssueTicket called")

                                grpurl = "https://graph.workplace.com/" + post_id + "/comments"
                                y = {
                                    'message': "Can you please elaborate the issue/ request you wanted to report"
                                }
                                print("----------------+---------------============++++payload:", y)
                                response = requests.post(
                                    grpurl,
                                    params=auth,
                                    json=y
                                )
                                print("-------------------Response:-", response)
                                return "Success"

                        else:
                            grpurl = "https://graph.workplace.com/" + post_id + "/comments"
                            print(grpurl)
                            payload = {
                                'message': "I am sorry, we could not find a solution for your reported issue. Would you like to raise a ticket to the technical team?"
                            }
                            response = requests.post(
                                grpurl,
                                params=auth,
                                json=payload
                            )
                            dbInsertion(temtext, payload, "unanswered", userName, userID, platform, "-1", "--")
                            logger.info(f'{userID} [get] Response:' + str(payload))
                            return "Fail"

                    elif msg.lower() == "no":
                        if parent_message == "Kindly raise a new ticket(Yes / No)?":
                            grpurl = "https://graph.workplace.com/" + post_id + "/comments"
                            print(grpurl)
                            y = {
                                'message': "Thank You"
                            }
                            print("----------------+8++++++++++000000000000000000000000000000007++++payload:", y)
                            response = requests.post(
                                grpurl,
                                params=auth,
                                json=y
                            )
                            print("-------------------Response:-", response)

                            grpurl1 = "https://graph.workplace.com/" + post_id + "/comments"
                            print(grpurl)
                            x1 = {
                                'message': "Please Rate a Services provided(1 / 2 / 3 / 4 / 5)"
                            }

                            print("----------------+8++++++++++000000000000000000000000000000007++++payload:", x1)
                            response = requests.post(
                                grpurl1,
                                params=auth,
                                json=x1
                            )


                            return "Success"

                        if str(_temp_post_id) in post_data.keys():
                            print("_______________________________________")
                            print(post_data[str(_temp_post_id)])


                            ticket_res_data = post_data[str(_temp_post_id)]
                            print(ticket_res_data)
                            print(type(ticket_res_data))

                            grpurl = "https://graph.facebook.com/"+ post_id +"/comments?summary=1&filter=toplevel&access_token="+ str(ACCESS_TOKEN)
                            response = requests.get(
                                grpurl,
                                params=auth
                            )

                            response_data = json.loads(response.text)

                            resp_arr = response_data['data']
                            print("----------resparr-------",resp_arr)

                            count = 0
                            for h in reversed(resp_arr):
                                count += 1
                                if count < 3:
                                    if h['message'] == 'We are sorry that we could not resolve your issue. Would you like to raise a ticket to the technical team (Yes / No)?':
                                        flag = "final_Ticket_creation"
                                        break
                                    elif h['message'] == "Kindly raise a new ticket(Yes / No)?":
                                        flag = "final_Ticket_creation"
                                        break
                                    else:
                                        flag = "Issue_Resolved"
                                        pass

                            if flag == "Issue_Resolved":
                                print("Is the issue Resolved:-  No")
                                userResponse = "No"
                                try:
                                    getAnswered_query = "SELECT query_id FROM `answered_queries` where `user_name`='" + userName + "' and `Feedback`='-1' order by`asked_on` desc LIMIT 1 "
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

                                grpurl = "https://graph.workplace.com/" + post_id + "/comments"
                                print(grpurl)
                                x = {
                                        'message': "We are sorry that we could not resolve your issue. Would you like to raise a ticket to the technical team (Yes / No)?"
                                }
                                print("----------------+8++++++++++000000000000000000000000000000007++++payload:", x)
                                response = requests.post(
                                    grpurl,
                                    params=auth,
                                    json=x
                                )
                                print("-------------------Response:-",response)
                                return "Success"

                            else:
                                grpurl = "https://graph.workplace.com/" + post_id + "/comments"
                                print(grpurl)
                                y = {
                                    'message': "Thank You"
                                }
                                print("----------------+8++++++++++000000000000000000000000000000007++++payload:", y)
                                response = requests.post(
                                    grpurl,
                                    params=auth,
                                    json=y
                                )
                                print("-------------------Response:-", response)

                                grpurl1 = "https://graph.workplace.com/" + post_id + "/comments"
                                print(grpurl)
                                x1 = {
                                    'message': "Please Rate a Services provided(1 / 2 / 3 / 4 / 5)",
                                }

                                print("----------------+8++++++++++000000000000000000000000000000007++++payload:", x1)
                                response = requests.post(
                                    grpurl1,
                                    params=auth,
                                    json=x1
                                )

                                return "Success"

                    else:
                        print("In else")

                        grpurl = "https://graph.facebook.com/" + post_id + "/comments?summary=1&filter=toplevel&access_token=" + str(
                            ACCESS_TOKEN)
                        response1 = requests.get(
                            grpurl,
                            params=auth
                        )

                        response_data1 = json.loads(response1.text)

                        resp_arr_1 = response_data1['data']
                        print("----------resparr-------", resp_arr_1)

                        c = 0
                        for h in reversed(resp_arr_1):
                            c += 1
                            if c < 3:
                                if h['message'] == 'Can you please elaborate the issue/ request you wanted to report':
                                    description = str(msg)
                                    # call getIssueTicket for ticket creation
                                    if str(_temp_post_id) in post_data.keys():
                                        print("++++++++++______________+++++++++++++++___________")
                                        print(post_data[str(_temp_post_id)])

                                        ticket_res_data_desc = post_data[str(_temp_post_id)]
                                        print(ticket_res_data_desc)

                                        user_response = "Yes"
                                        getIssueticket(ticket_res_data_desc,userID,userName,user_response,post_id,description,file_url)
                                        return "Success"

                                elif h['message'] == 'Please Rate a Services provided(1 / 2 / 3 / 4 / 5)':
                                    rating = str(msg)
                                    Rating(userName,userID,rating,post_id)
                                    return "Success"
                                else:
                                    pass

                        word_tokens = word_tokenize(msg.lower())
                        filtered_sentence = [w for w in word_tokens if not w in stop_words]
                        filtered_sentence = []
                        for w in word_tokens:
                            if w not in arr:
                                w = spell(w.lower())
                            if (w.lower() not in stop_words):
                                filtered_sentence.append(w)

                        usertext = " ".join(filtered_sentence)
                        print("=", usertext)

                        data = english_bot.get_response(usertext)
                        confidencebot = data.confidence  # english_bot.get_response(usertext).confidence
                        data = str(data)
                        print("data=== ", data)
                        flag = False
                        thirdvar = ""

                        if "|" in data:  # to separate word by space and compare each single word of input to each single word of yml file
                            Matchtext = data.split("|")[1];
                            sp = data.split("|")
                            if len(sp) > 2:
                                thirdvar = data.split("|")[2]
                            usertextsplit = usertext.split(" ")
                            Matchtextsplit = Matchtext.split(" ")
                            usertext = ""
                            for text in usertextsplit:
                                for match in Matchtextsplit:
                                    # print("fuzzy ",text.lower().strip(), "match", match.lower().strip()," = ", fuzz.ratio(text.lower().strip(),Matchtext.lower().strip()))
                                    if (fuzz.ratio(text.lower().strip(), Matchtext.lower().strip()) > 50):
                                        if text.lower() != "issue" and text.lower() != "problem" and text.lower() != "" and Matchtext.lower() != "":
                                            if text not in usertext:
                                                usertext += " " + text
                                            if (fuzz.ratio(text.lower().strip(), Matchtext.lower().strip())) == 100:
                                                flag = True
                                                break
                            fuzzymatch = fuzz.ratio(usertext.lower(), Matchtext.lower())
                            # print("Matchtext ", Matchtext)
                            # print("fuzzymatch = ", fuzzymatch)
                            if (confidencebot >= 0.80):
                                flag = True
                            elif (fuzzymatch) >= 80:
                                flag = True

                            data = data.split("|")[0]
                            print("New:", data)

                        elif "**" in data:
                            if (confidencebot >= 0.80):
                                flag = True
                        else:
                            if (confidencebot >= 0.80):
                                flag = True

                        regex = re.compile('[@_!#$%^*<>\|}{~:]')

                        if flag :
                            print("data______________________"+data)

                            if data[0:7] == "select ":
                                lastflag = False
                                query = data
                                # print("Query:",query)
                                output = create_query(query)
                                # print("output:",output)
                                tags_data = list(output)
                                # print("tags_data:",tags_data)
                                json_array = []
                                typetext = ""
                                newtags_data = []
                                # print("Length_tags_data",len(tags_data))
                                if len(tags_data) == 1:
                                    for t in tags_data:
                                        # print("ttttttttttttt"+str(t))
                                        for idx, title in enumerate(t):
                                            if len(t) == 2:
                                                head = t[1]
                                                if idx == 0:
                                                    # print("idx[0]", t[0])
                                                    d = t[0]
                                                    if ";" in d:
                                                        tag = d.split(";")
                                                        taglength = len(tag)
                                                        # print("Tag:", tag)
                                                        for t in tag:
                                                            if (regex.search(t) != None):
                                                                if "#" in t:
                                                                    tab = t.split("#")
                                                                    t5 = tab[1] + "#"
                                                                    tab1 = tab.remove(tab[1])
                                                                    newtab = tab.insert(1, t5)
                                                                    tabdata = tuple(tab)
                                                                    newtags_data.append(tabdata)
                                                                elif "$" in t:
                                                                    tab = t.split("$")
                                                                    t6 = tab[1] + "$"
                                                                    tab1 = tab.remove(tab[1])
                                                                    newtab = tab.insert(1, t6)
                                                                    tabdata = tuple(tab)
                                                                    newtags_data.append(tabdata)
                                                                elif "@" in t:
                                                                    tab = t.split("@")
                                                                    t7 = tab[1] + "@"
                                                                    tab1 = tab.remove(tab[1])
                                                                    newtab = tab.insert(1, t7)
                                                                    tabdata = tuple(tab)
                                                                    newtags_data.append(tabdata)
                                                                elif "*" in t:
                                                                    tab = t.split("*")
                                                                    t9 = tab[1] + "*"
                                                                    tab1 = tab.remove(tab[1])
                                                                    newtab = tab.insert(1, t9)
                                                                    tabdata = tuple(tab)
                                                                    newtags_data.append(tabdata)
                                                                elif "|" in t:
                                                                    tab = t.split("|")
                                                                    tabdata = tuple(tab)
                                                                    newtags_data.append(tabdata)
                                                                else:
                                                                    newtags_data.append(t)

                                                        for i in newtags_data:
                                                            # print("newtags_tttttt", i)
                                                            sim1 = {
                                                                "desc": i[0]
                                                            }
                                                            json_array.append(sim1)
                                                    elif ";" not in d:
                                                        if (regex.search(d) != None):
                                                            if "#" in d:
                                                                tab = d.split("#")
                                                                t5 = tab[1] + "#"
                                                                tab1 = tab.remove(tab[1])
                                                                newtab = tab.insert(1, t5)
                                                                tabdata = tuple(tab)
                                                                newtags_data.append(tabdata)
                                                            elif "$" in d:
                                                                tab = d.split("$")
                                                                t6 = tab[1] + "$"
                                                                tab1 = tab.remove(tab[1])
                                                                newtab = tab.insert(1, t6)
                                                                tabdata = tuple(tab)
                                                                newtags_data.append(tabdata)
                                                            elif "@" in d:
                                                                tab = d.split("@")
                                                                t7 = tab[1] + "@"
                                                                tab1 = tab.remove(tab[1])
                                                                newtab = tab.insert(1, t7)
                                                                tabdata = tuple(tab)
                                                                newtags_data.append(tabdata)
                                                            elif "*" in d:
                                                                tab = d.split("*")
                                                                t7 = tab[1] + "*"
                                                                tab1 = tab.remove(tab[1])
                                                                newtab = tab.insert(1, t7)
                                                                tabdata = tuple(tab)
                                                                newtags_data.append(tabdata)
                                                            elif "|" in d:
                                                                tab = d.split("|")
                                                                tabdata = tuple(tab)
                                                                newtags_data.append(tabdata)
                                                            else:
                                                                newtags_data.append(t)
                                                        # else:
                                                        #     sim1 = {
                                                        #         "desc": title,
                                                        #         "title": title, "buttontext": "",
                                                        #         "imagepath": "",
                                                        #         "redirectlink": "", "topright": "", "bottomtight": "",
                                                        #         "action": "", "message": "",
                                                        #         "ParameterTitle": ""}
                                                        #     json_array.append(sim1)
                                                        #
                                                        for i in newtags_data:
                                                            # print("newtags_tttttt", i)
                                                            sim1 = {
                                                                "desc": i[0]
                                                                }
                                                            json_array.append(sim1)

                                                if idx == 1:
                                                    head = title
                                            if len(t) == 12:
                                                if "hr" in str(t[3]).lower():
                                                    typetext = "hr"
                                                    category = "HR"
                                                elif "admin" in str(t[3]).lower():
                                                    typetext = "admin"
                                                    category = "Admin"
                                                elif "cctv" in str(t[3]).lower():
                                                    typetext = "admin"
                                                    category = "Admin"
                                                else:
                                                    typetext = ""
                                                    category = "Technology"
                                                l = len(t)
                                                queryResponse = str(t[6]).replace("##LINK##", image_path_BAseURL)
                                                video_path = t[7]
                                                if video_path is None:
                                                    video_path = ""
                                                else:
                                                    video_path = video_path_BaseURL + video_path
                                                    queryResponse = queryResponse + "\n" + video_path

                                                    # print("video_path",video_path)

                                                vendor = ["Zicom", "Securens", "Modern", "Soteria", "SIS Prosegur"]
                                                cat1 = t[2]
                                                cat3 = t[4]
                                                if "##cctvform##" in queryResponse:
                                                    json_data = {
                                                        # "message": queryResponse,
                                                        # "operation_id": t[0],
                                                        # "userText": usertext,
                                                        "title": "Please enter the below details to raise a ticket",
                                                        "cat1": t[2],
                                                        "cat2": t[3],
                                                        "cat3": t[4],
                                                        "cat4": t[5],
                                                        "response": queryResponse,
                                                        "video_path": video_path,
                                                        "project_name": t[8],
                                                        # "ParameterTitle": "",
                                                        # "action": "",
                                                        "orignalText": msg,
                                                        # "typetext": typetext,
                                                        "vendor": vendor,
                                                        "priority": t[9],
                                                        "urgency": t[10],
                                                        "impact": t[11]
                                                    }
                                                elif "Voice" in cat1 or "One Login SMS Not received" in cat3:
                                                    json_data = {
                                                        "error": "Kindly raise  a new ticket",
                                                        "resolve": "",
                                                        "rating": "err",
                                                        "Keyadmin": "True",
                                                        "cat1": t[2],
                                                        "cat2": t[3],
                                                        "cat3": t[4],
                                                        "cat4": t[5],
                                                        "project_name": t[8],
                                                        "priority": t[9],
                                                        "urgency": t[10],
                                                        "impact": t[11],
                                                        "mainIssue": "Technology"
                                                    }
                                                else:
                                                    json_data = {
                                                        # "message": queryResponse,
                                                        # "operation_id": t[0],
                                                        # "userText": usertext,
                                                        "title": t[1],
                                                        "cat1": t[2],
                                                        "cat2": t[3],
                                                        "cat3": t[4],
                                                        "cat4": t[5],
                                                        "response": queryResponse,
                                                        "video_path": video_path,
                                                        "project_name": t[8],
                                                        # "ParameterTitle": "",
                                                        # "action": "",
                                                        "orignalText": msg,
                                                        # "typetext": typetext,
                                                        "priority": t[9],
                                                        "urgency": t[10],
                                                        "impact": t[11]
                                                    }
                                                lastflag = True

                                            if len(t) == 1:
                                                l = len(t)
                                                if idx == 0:
                                                    res = title
                                                lastflag = True

                                    if lastflag:
                                        print("answer1 " + str(json_data))

                                        data1 = json.dumps(json_data, sort_keys=True, indent=4 * ' ')
                                        data = data1
                                        data2 = json.dumps(json_data)

                                        final_response = json_data['response']
                                        print("Final Response-------:", final_response)

                                        if "##C##" in final_response :
                                            final_response = final_response.strip("##C##")
                                            grpurl = "https://graph.workplace.com/" + post_id + "/comments"
                                            print(grpurl)
                                            payload = {
                                                'message': final_response,
                                                # 'attachment_url':"https://askpanda.iifl.in/ServiceBot/iiflvideos/Google/183_Google_Google_DATA_STUDIO.mp4"
                                            }
                                            print("----------------______________________________________++++payload:",
                                                  payload)
                                            response = requests.post(
                                                grpurl,
                                                params=auth,
                                                json=payload
                                            )
                                            print("++++++++++++++++++++++++++++++++Response", response)
                                            dbInsertion(temtext, data2, "query", userName, userID, platform, "-1",category)
                                            logger.info(f'{userID} [get] Response:' + str(json_data))

                                            user_response = "Yes"
                                            Create_Update_ticket(json_data, userID, userName, user_response,post_id)
                                            return "Success"
                                        else:

                                            post_d = {_temp_post_id : json_data}

                                            if str(_temp_post_id) in post_data.keys():
                                                post_data.pop(_temp_post_id)
                                                post_data.update(post_d)
                                            else:
                                                post_data.update(post_d)


                                            if "<br>" in final_response :
                                                final_response1 = final_response.replace('<br>','\n')
                                                final_response = final_response1

                                            if "#|#" in final_response :
                                                e = final_response.split("#|#")
                                                e.append("Is the Issue resolved (Yes / No)?")


                                                grpurl = "https://graph.workplace.com/" + post_id + "/comments"

                                                for i in e:
                                                    image_path = ""
                                                    if "<img" in i:
                                                        image_path = re.search("(?P<url>https?://[^\s>']+)", str(i)).group("url").strip('"')
                                                        print(image_path)

                                                        #image_path = IMG_URL.strip('"')
                                                        text_res = i.split("<img")[0]
                                                        print(text_res)
                                                    else:
                                                        text_res = i

                                                    if len(image_path) > 0:
                                                        payload = {
                                                            'message': str(text_res),
                                                            'attachment_url': image_path
                                                        }
                                                    else:
                                                        payload = {
                                                            'message': str(text_res)
                                                        }

                                                    print("----------------+8++++++++++88++8+8+8888888888888777++++payload11111:", payload)
                                                    response = requests.post(
                                                        grpurl,
                                                        params=auth,
                                                        json=payload
                                                    )
                                                    print("++++++++++++++++++++++++++++++++Response", response)

                                                dbInsertion(temtext, data2, "query", userName, userID, platform, "-1", category)
                                                logger.info(f'{userID} [get] Response:' + str(json_data))
                                                return "Success"

                                            else:
                                                grpurl = "https://graph.workplace.com/" + post_id + "/comments"
                                                print(grpurl)
                                                payload = {
                                                     'message': final_response,
                                                     #'attachment_url':"https://askpanda.iifl.in/ServiceBot/iiflvideos/Google/183_Google_Google_DATA_STUDIO.mp4"
                                                }
                                                print("----------------______________________________________++++payload:",payload)
                                                response = requests.post(
                                                    grpurl,
                                                    params=auth,
                                                    json=payload
                                                )
                                                print("++++++++++++++++++++++++++++++++Response",response)
                                                dbInsertion(temtext, data2, "query", userName, userID, platform, "-1", category)
                                                logger.info(f'{userID} [get] Response:' + str(json_data))

                                                payload_issue = {
                                                    'message': "Is the Issue resolved (Yes / No)?"
                                                }

                                                response = requests.post(
                                                    grpurl,
                                                    params=auth,
                                                    json=payload_issue
                                                )

                                                return "Success"

                                    else:
                                        print("Head:",head)
                                        if "|" in head:
                                            cat = head.split("|")
                                            head = cat[0]
                                            if "hr" in cat[1]:
                                                category = "HR"
                                            elif "admin" in cat[1]:
                                                category = "Admin"
                                            else:
                                                category = "Technology"

                                        print("-------------2",json_array)
                                        print("-------------head",head)

                                        if "|" in head:
                                            cat = head.split("|")
                                            head = cat[0]

                                        data_arr = "Can you please further elaborate the Nature of the Issue:"
                                        count = 0
                                        for i in json_array:
                                            if data_arr != "":
                                                count += 1
                                                if count == 1:
                                                    data_arr = data_arr + '\n\n' + str(count)+"."+str(i['desc'])
                                                else:
                                                    data_arr = data_arr +' '+'\n'+' '+ str(count)+"."+ str(i['desc'])
                                        print(data_arr)

                                        grpurl = "https://graph.workplace.com/"+post_id+"/comments"
                                        print(grpurl)
                                        payload = {

                                            'message': data_arr
                                        }
                                        response = requests.post(
                                            grpurl,
                                            params=auth,
                                            json=payload
                                        )
                                        dbInsertion(temtext, payload, "query", userName, userID, platform, "-1", category)
                                        logger.info(f'{userID} [get] Response:' + str(payload))
                                        return "Success"

                                else:
                                    for t in tags_data:
                                        # print("ttttttttttttt"+str(t))
                                        for idx, title in enumerate(t):
                                            # print(len(t))
                                            if len(t) == 2:
                                                head = t[1]
                                                d = t[0]
                                                tabdata = ()
                                                if idx == 0:
                                                    if (regex.search(d) != None):
                                                        if "#" in d:
                                                            tab = d.split("#")
                                                            t5 = tab[1] + "#"
                                                            tab1 = tab.remove(tab[1])
                                                            newtab = tab.insert(1, t5)
                                                            tabdata = tuple(tab)
                                                        elif "$" in d:
                                                            tab = d.split("$")
                                                            t6 = tab[1] + "$"
                                                            tab1 = tab.remove(tab[1])
                                                            newtab = tab.insert(1, t6)
                                                            tabdata = tuple(tab)
                                                        elif "*" in d:
                                                            tab = d.split("*")
                                                            t5 = tab[1] + "*"
                                                            tab1 = tab.remove(tab[1])
                                                            newtab = tab.insert(1, t5)
                                                            tabdata = tuple(tab)
                                                        elif "@" in d:
                                                            tab = d.split("@")
                                                            t7 = tab[1] + "@"
                                                            tab1 = tab.remove(tab[1])
                                                            newtab = tab.insert(1, t7)
                                                            tabdata = tuple(tab)
                                                        elif "|" in d:
                                                            tab = d.split("|")
                                                            tabdata = tuple(tab)
                                                        # print(tabdata)
                                                        sim1 = {
                                                            "desc": tabdata[0],
                                                            }
                                                        json_array.append(sim1)

                                                    else:
                                                        tabdata = d
                                                        sim1 = {
                                                            "desc": d,
                                                            }
                                                        json_array.append(sim1)

                                    #####################   Category related logic ##########################
                                    print(head)
                                    if "|" in head:
                                        cat = head.split("|")
                                        head = cat[0]
                                        if "hr" in cat[1]:
                                            category = "HR"
                                        elif "admin" in cat[1]:
                                            category = "Admin"
                                        else:
                                            category = "Technology"

                                    # mainIssue = category
                                    # print("MainIssue:", mainIssue)

                                    print("-------------3", json_array)
                                    data_arr = "Can you please further elaborate the Nature of the Issue:"
                                    count = 0
                                    for i in json_array:
                                        if data_arr != "":
                                            count += 1
                                            if count == 1:
                                                data_arr = data_arr + '\n\n' + str(count) + "." + str(i['desc'])
                                            else:
                                                data_arr = data_arr + ' ' + '\n' + ' ' + str(count) + "." + str(i['desc'])
                                    print(data_arr)

                                    grpurl = "https://graph.workplace.com/" + post_id + "/comments"
                                    print(grpurl)
                                    payload = {

                                        'message': data_arr
                                    }
                                    response = requests.post(
                                        grpurl,
                                        params=auth,
                                        json=payload
                                    )
                                    dbInsertion(temtext, payload, "query", userName, userID, platform, "-1", category)
                                    logger.info(f'{userID} [get] Response:' + str(payload))
                                    return "Success"

                            elif "Admin_default" in data:  # in case we want to send manualy ticket message and Keyadmin is a key to store the data in answered table

                                json_data = {
                                    "title": "Kindly raise a new ticket",
                                    "resolve": "",
                                    "rating": "err",
                                    "Keyadmin": "True",
                                    "cat1": "Administration",
                                    "cat2": "Admin",
                                    "cat3": "Admin related work",
                                    "cat4": "",
                                    "project_name": "Service Request",
                                    "response":"",
                                    "orignalText": temtext,
                                    "priority": "default" ,
                                    "urgency": "default" ,
                                    "impact": "default"
                                }

                                post_d = {_temp_post_id: json_data}

                                if str(_temp_post_id) in post_data.keys():
                                    post_data.pop(_temp_post_id)
                                    post_data.update(post_d)
                                else:
                                    post_data.update(post_d)

                                grpurl = "https://graph.workplace.com/" + post_id + "/comments"
                                print(grpurl)
                                payload = {

                                    'message': "Kindly raise a new ticket(Yes / No)?"
                                }
                                response = requests.post(
                                    grpurl,
                                    params=auth,
                                    json=payload
                                )
                                dbInsertion(temtext, payload, "query", userName, userID, platform, "-1", "Admin")
                                logger.info(f'{userID} [get] Response:' + str(payload))
                                return "Success"


                            elif "showtickets" in data:
                                print("==========================Data==========",data)
                                grpurl = "https://graph.workplace.com/" + post_id + "/comments"
                                print(grpurl)
                                payload = {

                                    'message': "Please enter Ticket ID (INC-/ SR-)"
                                }
                                response = requests.post(
                                    grpurl,
                                    params=auth,
                                    json=payload
                                )

                                dbInsertion(temtext, payload, "query", userName, userID, platform, "-1", "Ticket Status")
                                logger.info(f'{userID} [get] Response:' + str(payload))
                                return "Success"

                            elif "tickets" in data:
                                print("==========================Data==========",data)
                                grpurl = "https://graph.workplace.com/" + post_id + "/comments"
                                print(grpurl)
                                payload = {

                                    'message': "Please enter Ticket ID (INC-/ SR-)"
                                }
                                response = requests.post(
                                    grpurl,
                                    params=auth,
                                    json=payload
                                )

                                dbInsertion(temtext, payload, "query", userName, userID, platform, "-1", "Ticket Status")
                                logger.info(f'{userID} [get] Response:' + str(payload))
                                return "Success"

                            else:
                                grpurl = "https://graph.workplace.com/" + post_id + "/comments"
                                print(grpurl)
                                payload = {
                                    'message': "I am sorry, we could not find a solution for your reported issue. Would you like to raise a ticket to the technical team?"
                                }
                                response = requests.post(
                                    grpurl,
                                    params=auth,
                                    json=payload
                                )
                                dbInsertion(temtext, payload, "unanswered", userName, userID, platform, "-1", "--")
                                logger.info(f'{userID} [get] Response:' + str(payload))

                                return "Success"

                        elif flag == False:
                            equalMatch = False
                            usertextsplit = temtext.split(" ")
                            # print("false data== ",data)
                            Matchtextsplit = Matchtext.split(" ")
                            print("usertextsplit= ", usertextsplit, "\n Matchtextsplit=", Matchtextsplit)
                            for text in usertextsplit:
                                for match in Matchtextsplit:
                                    # print("fuzzy== ",text, "match== ", match)
                                    if text.lower() == match.lower() and text.lower() != "" and match.lower() != "":
                                        equalMatch = True
                            # print("equalMatch ",equalMatch)
                            if equalMatch:
                                if "hr" in thirdvar.lower():
                                    typetext = "hr"
                                    category = "HR"
                                elif "admin" in thirdvar.lower():
                                    typetext = "admin"
                                    category = "Admin"
                                else:
                                    typetext = ""
                                    category = "Technology"

                                json_array1 = []
                                sim1 = {
                                    "desc": Matchtext
                                }
                                json_array1.append(sim1)

                                data_arr = "Are you looking for ?"

                                count = 0
                                for i in json_array1:
                                    if data_arr != "":
                                        count += 1
                                        if count == 1:
                                            data_arr = data_arr + '\n\n' + str(count) + "." + str(i['desc'])
                                        else:
                                            data_arr = data_arr + ' ' + '\n' + ' ' + str(count) + "." + str(i['desc'])
                                print(data_arr)

                                grpurl = "https://graph.workplace.com/" + post_id + "/comments"
                                print(grpurl)
                                payload = {

                                    'message': data_arr
                                }
                                response = requests.post(
                                    grpurl,
                                    params=auth,
                                    json=payload
                                )
                                dbInsertion(temtext, payload, "query", userName, userID, platform, "-1", category)
                                logger.info(f'{userID} [get] Response:' + str(payload))
                                return "Success"

                            elif "help" in str(temtext).lower():
                                # json_data = {
                                #     "error": "Sure, can you please enter the issue your are facing.",
                                #     # "cat1": "Application Services",
                                #     # "cat2": "Applications",
                                #     # "cat3": "Trader Terminal",
                                #     # "project_name": "Incident Management"
                                # }
                                grpurl = "https://graph.workplace.com/" + post_id + "/comments"
                                print(grpurl)
                                payload = {
                                    'message': "Sure, can you please enter the issue your are facing."
                                }
                                response = requests.post(
                                    grpurl,
                                    params=auth,
                                    json=payload
                                )
                                dbInsertion(temtext, payload, "query", userName, userID, platform, "-1", "Greeting")
                                logger.info(f'{userID} [get] Response:' + str(payload))
                                return "Success"


                            elif str(temtext).lower() in ["how are you", "how are you?", "how r you?", "how r you", "how r u",
                                                          "how r u?",
                                                          "hows u?"]:  # greeting for How are you
                                # json_data = {
                                #     "error": "Fine",
                                #     "cat1": "Application Services",
                                #     "cat2": "Applications",
                                #     "cat3": "Trader Terminal",
                                #     "project_name": "Incident Management",
                                # }

                                grpurl = "https://graph.workplace.com/" + post_id + "/comments"
                                print(grpurl)
                                payload = {
                                    'message': "Fine"
                                }
                                response = requests.post(
                                    grpurl,
                                    params=auth,
                                    json=payload
                                )
                                dbInsertion(temtext, payload, "query", userName, userID, platform, "-1", "Greeting")
                                logger.info(f'{userID} [get] Response:' + str(payload))
                                return "Success"

                            else:
                                # json_data = {
                                #     "error": "I am sorry, we could not find a solution for your reported issue. Would you like to raise a ticket to the technical team?",
                                #     "resolve": "",
                                #     "rating": "err",
                                #     "cat1": "Application Services",
                                #     "cat2": "Applications",
                                #     "cat3": "Trader Terminal",
                                #     "project_name": "Incident Management",
                                # }
                                grpurl = "https://graph.workplace.com/" + post_id + "/comments"
                                print(grpurl)
                                payload = {
                                    'message': "I am sorry, we could not find a solution for your reported issue. Would you like to raise a ticket to the technical team?"
                                }
                                response = requests.post(
                                    grpurl,
                                    params=auth,
                                    json=payload
                                )
                                dbInsertion(temtext, payload, "unanswered", userName, userID, platform, "-1", "--")
                                logger.info(f'{userID} [get] Response:' + str(payload))
                                return "Success"

                        print("message")
                return "Message Processed"
            else:
                return "Success"
        else:
            return "Success"

def get_tic_status(userName,Ticket,post_id):
    try:
        objectrecived = {'userName':userName,'Ticket id':Ticket,'post_id':post_id}
        Ticket = Ticket.upper()
        logger.info(f'{userName} [getTicStatus] Request:' + str(objectrecived))

        if Ticket[:3] == "INC":
            url = 'https://techconnect.iifl.in/SapphireIMS/api/ticket/get/' + Ticket + '/requestId/Incident Management/projectName'
        elif Ticket[:3] == "SR-":
            url = 'https://techconnect.iifl.in/SapphireIMS/api/ticket/get/' + Ticket + '/requestId/Service Request/projectName'
        else:
            grpurl = "https://graph.workplace.com/" + post_id + "/comments"
            print(grpurl)
            payload = {
                'message': "Please enter valid Ticket Id"
            }
            response = requests.post(
                grpurl,
                params=auth,
                json=payload
            )
            logger.info(f'{userName} [getTicStatus]  Response: Please enter valid Ticket Id')

            return "Success"

        headers = {"Accept": "application/json",
                   "Content-Type": "application/json",
                   "int-log-id": "qwertyasdfg",
                   "key": "2fb29d27-51a9-4074-82f5-45db3f450d24",
                   "token": "7560a221-28b3-4343-8848-2388fe788d51",
                   "Cache-Control": "no-cache"}

        response = requests.get(url, headers=headers, verify=False)

        response = json.loads(response.text)
        logger.info(f'{userName} [getTicStatus]  SapphireResponse:' + str(response))
        if response.get("code"):
            e = response.get("message")

            grpurl = "https://graph.workplace.com/" + post_id + "/comments"
            print(grpurl)
            payload = {
                'message': e
            }
            response = requests.post(
                grpurl,
                params=auth,
                json=payload
            )

            logger.info(f'{userName} [getTicStatus]  Response:' + str(response.get("message")))

            grpurl1 = "https://graph.workplace.com/" + post_id + "/comments"
            print(grpurl)
            x1 = {
                'message': "Please Rate a Services provided(1 / 2 / 3 / 4 / 5)",
            }

            print("----------------+8++++++++++000000000000000000000000000000007++++payload:", x1)
            response = requests.post(
                grpurl1,
                params=auth,
                json=x1
            )

            return "Success"
        else:
            # print("success")
            Status = response.get("ticket").get("currentState").get("stateName")
            grpurl = "https://graph.workplace.com/" + post_id + "/comments"
            print(grpurl)
            payload = {
                'message': "Ticket ID :-\t" + Ticket +"\n Status:-\t "+ Status
            }
            response = requests.post(
                grpurl,
                params=auth,
                json=payload
            )

            logger.info(
                f'{userName} [getTicStatus]  Response:Status of Ticket ID "+Ticket+"\n"+ Status')

            grpurl1 = "https://graph.workplace.com/" + post_id + "/comments"
            print(grpurl)
            x1 = {
                'message': "Please Rate a Services provided(1 / 2 / 3 / 4 / 5)",
            }

            print("----------------+8++++++++++000000000000000000000000000000007++++payload:", x1)
            response = requests.post(
                grpurl1,
                params=auth,
                json=x1
            )

            return "Success"
    except:
        logger.error(f'{userName} [getFinalResponse] Exception occurred', exc_info=True)
        traceback.print_exc()
        grpurl = "https://graph.workplace.com/" + post_id + "/comments"
        print(grpurl)
        x = {
            'message': "Currently service not available",
        }

        print("----------------+8++++++++++000000000000000000000000000000007++++payload:", x)
        response = requests.post(
            grpurl,
            params=auth,
            json=x
        )
        print("-------------------Response:-", response)

        grpurl1 = "https://graph.workplace.com/" + post_id + "/comments"
        print(grpurl)
        x1 = {
            'message': "Please Rate a Services provided(1 / 2 / 3 / 4 / 5)",
        }

        print("----------------+8++++++++++000000000000000000000000000000007++++payload:", x1)
        response = requests.post(
            grpurl1,
            params=auth,
            json=x1
        )

        return "Success"


def dbInsertion(usertext, response, flag, userName, userID, platform, feedback, category):
    try:
        currenttime = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        usertext = str(usertext).replace("'", "").replace("\\", "")


        if flag.lower() == "unanswered":

            unanswered_query = "insert into unanswered_queries" \
                               "(query,asked_on,user_name,userid,platform,category) " \
                               "values ('" + str(usertext) + "','" + currenttime + "','" + str(userName) + "','" + str(
                userID) + "','" + str(platform) + "','" + category + "')"
            # print("unanswered_query ", unanswered_query)
            uns = insertquery(unanswered_query)
        else:
            response = response.replace('\'', '\\"')

            # print("response"+response)
            answered_query = "insert into answered_queries" \
                             "(query,asked_on,user_name,query_answer,Feedback,userid,platform,category) values " \
                             "(" \
                             "'" + str(usertext) + "','" + currenttime + "','" + str(userName) + "','" + str(
                response) + "','" + str(feedback) + "','" + str(userID) + "','" + str(
                platform) + "','" + category + "')"
            # print("answered_query ", answered_query)
            uns = insertquery(answered_query)

    except Exception as e:
        logger.error(f'{userID} [dbInsertion] Exception occurred', exc_info=True)

        print("Exception occured ", e)
        traceback.print_exc()
        # print("### cannot insert into database ###")

def getIssueticket(ticketdata,userID,userName,userResponse,post_id,description,file_url):
    print("[[[[[[[[[[[[[[[[[[[[[[[[_________________________________}}}}}}}}}}}}}}}}}}}}}}}}")
    try:
        title = ticketdata['title']
        cat1 = ticketdata['cat1']
        cat2 = ticketdata['cat2']
        cat3 = ticketdata['cat3']
        cat4 = ticketdata['cat4']
        botresponse = ticketdata['response']
        if botresponse == "":
            botresponse = None

        project_name = ticketdata['project_name']
        orignalText = ticketdata['orignalText']
        priority = ticketdata['priority']
        urgency = ticketdata['urgency']
        impact = ticketdata['impact']

        platform = "Facebook Workplace"

        #userID = "mob_nikhil_l"
        _filename = ""

        if file_url != "":
            folder = userID
            path = os.path.join('Temp/', folder)
            os.mkdir(path)
            a = urlparse(file_url)
            _filename = Path(a.path).name
            print("Filename",_filename)
            r = requests.get(file_url, allow_redirects=True)
            with open(os.path.join('Temp/'+ folder, _filename), 'wb') as f:
                f.write(r.content)

        filearray = []

        if priority == None or priority == "default":
            priority = "P3"
        else:
            priority = priority

        if urgency == None or urgency == "default":
            urgency = "Low"
        else:
            urgency = urgency

        if impact == None or impact == "default":
            impact = "Low"
        else:
            impact = impact

        if cat2.lower() == 'admin' and cat3 == 'Trader Terminal':
            cat1 = "Administration"
            cat2 = "Admin"
            cat3 = "Admin related work"
            cat4 = ""
            project_name = "Service Request"

        currenttime = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        logger.info(f'{userName} [getIssueTicket] Request:' + str(ticketdata))
        random_id = randint(10000000, 999999999999)

        desc = "User Query : " + str(orignalText) + "<br><br>Bot Response : " + str(
            botresponse) + "<br><br>Issue Description : " + str(
            description)

        if "Service Request" in project_name:
            priority = "P4"

        if userResponse.lower() == 'yes':
            url = 'https://techconnect.iifl.in/SapphireIMS/api/ticket/create'
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

            if not cat4:
                cat4 == ""

            if cat4 == "" or cat4 == "NULL":
                derivedfield = "DerivedField1"
            else:
                derivedfield = "derivedField1"

            if "Top-Up Issue" in cat4:
                derivedfield = "DerivedField1"


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
                        derivedfield: {
                            "name": cat4
                        },
                        "priority": {
                            "name": priority
                        },
                        "urgency": {
                            "name": urgency
                        },
                        "impact": {
                            "name": impact
                        },
                        "probDescription": desc,
                        "title": orignalText,
                        "submittedBy": {
                            "userName": userName,
                            # "userName": "mob_nikhil_l"
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
            print(data)
            logger.info(f'{userName} [getIssueTicket]  SapphireRequest:' + str(data))
            response = requests.post(url, data=data, headers=headers, verify=False)
            print(response)
            response = json.loads(response.text)
            # response ={
            #      "requestType": "CREATE_TICKET",
            #      "integrationLogId": "5421545144542",
            #      "iteration": 0,
            #      "problemId": 54209,
            #      "requestNumber": "INC-010174"
            # }
            logger.info(f'{userName} [getIssueTicket]  SapphireResponse:' + str(response))

            if response.get("code"):
                ticket_fail_resp = response.get("message")

                grpurl = "https://graph.workplace.com/" + post_id + "/comments"
                print(grpurl)
                x = {
                    'message': str(ticket_fail_resp),
                    # 'attachment':"https://askpanda.iifl.in/ServiceBot/iiflvideos/Google/183_Google_Google_DATA_STUDIO.mp4"
                }

                print("----------------+8++++++++++000000000000000000000000000000007++++payload:", x)
                response = requests.post(
                    grpurl,
                    params=auth,
                    json=x
                )
                print("-------------------Response:-", response)

                grpurl1 = "https://graph.workplace.com/" + post_id + "/comments"
                print(grpurl)
                x1 = {
                    'message': "Please Rate a Services provided(1 / 2 / 3 / 4 / 5)",
                }

                print("----------------+8++++++++++000000000000000000000000000000007++++payload:", x1)
                response = requests.post(
                    grpurl1,
                    params=auth,
                    json=x1
                )

                return "Success"
            else:
                Ticket_id_ = response.get("requestNumber")
                print(Ticket_id_)

                if _filename != "":
                    filepath = 'Temp/'+ userID +"/"+_filename

                    openfile = open(filepath, 'rb')
                    filedata = ('file', openfile)
                    filearray.append(filedata)

                    url = "https://techconnect.iifl.in/SapphireIMS/api/ticket/upload"

                    payload = {'requestNo': Ticket_id_,
                               'project': project_name}
                    files = filearray
                    headers = {
                        'int-log-id': 'qwertyasdfg',
                        'key': '2fb29d27-51a9-4074-82f5-45db3f450d24',
                        'token': '7560a221-28b3-4343-8848-2388fe788d51'
                    }
                    response = requests.request("POST", url, headers=headers, data=payload, verify=False, files=files)
                    print(response.text)
                    openfile.close()
                    os.remove(os.path.join("Temp/"+userID, _filename))
                    path = os.path.join("Temp/", userID)
                    os.rmdir(path)

                ticket_success_resp = "Thank you, We have created Ticket for your issue.\n       Ticket ID :-" + " " + Ticket_id_
                grpurl = "https://graph.workplace.com/" + post_id + "/comments"
                print(grpurl)
                x = {
                    'message': str(ticket_success_resp),
                    # 'attachment':"https://askpanda.iifl.in/ServiceBot/iiflvideos/Google/183_Google_Google_DATA_STUDIO.mp4"
                }

                print("----------------+8++++++++++000000000000000000000000000000007++++payload:", x)
                response = requests.post(
                    grpurl,
                    params=auth,
                    json=x
                )
                print("-------------------Response:-", response)
                try:
                    getAnswered_query = "SELECT query_id FROM `answered_queries` where `user_name`='" + userName + "' order by`asked_on` desc LIMIT 1 "
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
                    logger.error(f'{userName} [getFinalResponse] Exception occurred', exc_info=True)
                    print("Exception Occured " + e)


                grpurl1 = "https://graph.workplace.com/" + post_id + "/comments"
                print(grpurl)
                x1 = {
                    'message': "Please Rate a Services provided(1 / 2 / 3 / 4 / 5)",
                }
                print("----------------+8++++++++++000000000000000000000000000000007++++payload:", x1)
                response = requests.post(
                    grpurl1,
                    params=auth,
                    json=x1
                )

                return "Success"

    except Exception as e:
        logger.error(f'{userName} [getFinalResponse] Exception occurred', exc_info=True)
        traceback.print_exc()
        grpurl = "https://graph.workplace.com/" + post_id + "/comments"
        print(grpurl)
        x = {
            'message': "Currently service not available",
            # 'attachment':"https://askpanda.iifl.in/ServiceBot/iiflvideos/Google/183_Google_Google_DATA_STUDIO.mp4"
        }

        print("----------------+8++++++++++000000000000000000000000000000007++++payload:", x)
        response = requests.post(
            grpurl,
            params=auth,
            json=x
        )
        print("-------------------Response:-", response)
        return "Success"

def Create_Update_ticket(ticketdata,userID,userName,userResponse,post_id):
    print("=========================================================================")
    # userid is defined "mob_nikhil_l"
    try:
        title = ticketdata['title']
        cat1 = ticketdata['cat1']
        cat2 = ticketdata['cat2']
        cat3 = ticketdata['cat3']
        cat4 = ticketdata['cat4']
        botresponse = ticketdata['response']
        project_name = ticketdata['project_name']
        orignalText = ticketdata['orignalText']
        priority = ticketdata['priority']
        urgency = ticketdata['urgency']
        impact = ticketdata['impact']

        platform = "Facebook Workplace"

        #userID = "mob_nikhil_l"

        if "##C##" in botresponse:
            botresponse = botresponse.strip("##C##")

        if priority == None or priority == "default":
            priority = "P3"
        else:
            priority = priority

        if urgency == None or urgency == "default":
            urgency = "Low"
        else:
            urgency = urgency

        if impact == None or impact == "default":
            impact = "Low"
        else:
            impact = impact

        desc = "User Query : " + str(orignalText) + "<br><br>Bot Response : " + str(botresponse)
        currenttime = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        logger.info(f'{userName} [getFinalResponse] Request:' + str(ticketdata))

        try:
            getAnswered_query = "SELECT query_id FROM `answered_queries` where `user_name`='" + userName + "' and `Feedback`='-1' order by`asked_on` desc LIMIT 1 "
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
            logger.error(f'{userName} [getFinalResponse] Exception occurred', exc_info=True)

            print("Exception Occured " + e)

        random_id = randint(10000000, 999999999999)
        # print(random_id)
        url = 'https://techconnect.iifl.in/SapphireIMS/api/ticket/create'
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

        if cat4 == "" or cat4 is None:
            derivedfield = "DerivedField1"
        else:
            derivedfield = "derivedField1"

        if "Service Request" in project_name:
            priority = "P4"

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
                derivedfield: {
                    "name": cat4
                },
                "priority": {
                    "name": priority
                },
                "urgency": {
                    "name": urgency
                },
                "impact": {
                    "name": impact
                },
                "probDescription": desc,
                "title": orignalText,
                "submittedBy": {
                    "userName": userName,
                    # "userName": "mob_nikhil_l"
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
        print("json data:::::::::::",data)
        supphireresponse = requests.post(url, data=data, headers=headers, verify=False)
        # print(supphireresponse)
        print(supphireresponse.text)
        # newresponse = {
        #      "requestType": "CREATE_TICKET",
        #      "integrationLogId": "958104188316",
        #      "iteration": 0,
        #      "problemId": 54209,
        #      "requestNumber": "INC-010174"
        # }
        newresponse = json.loads(supphireresponse.text)
        print("Respond:",newresponse)
        logger.info(f'{userName} [getFinalResponse] Response:' + str(newresponse))
        if newresponse.get("code"):
            # print("error")
            ticket_fail_resp = newresponse.get("message")
            grpurl = "https://graph.workplace.com/" + post_id + "/comments"
            print(grpurl)
            x = {
                'message': str(ticket_fail_resp),
                # 'attachment':"https://askpanda.iifl.in/ServiceBot/iiflvideos/Google/183_Google_Google_DATA_STUDIO.mp4"
            }

            print("----------------+8++++++++++000000000000000000000000000000007++++payload:", x)
            response = requests.post(
                grpurl,
                params=auth,
                json=x
            )
            print("-------------------Response:-", response)

            grpurl = "https://graph.workplace.com/" + post_id + "/comments"
            print(grpurl)
            x = {
                'message': "Please Rate a Services provided(1 / 2 / 3 / 4 / 5)",
                # 'attachment':"https://askpanda.iifl.in/ServiceBot/iiflvideos/Google/183_Google_Google_DATA_STUDIO.mp4"
            }

            print("----------------+8++++++++++000000000000000000000000000000007++++payload:", x)
            response = requests.post(
                grpurl,
                params=auth,
                json=x
            )

            return "Success"
        else:
            Ticket_id_ = newresponse.get("requestNumber")
            random_id = randint(10000000, 999999999999)
            if userResponse.lower() == 'yes':  # if users issue resolved

                url = 'https://techconnect.iifl.in/SapphireIMS/api/ticket/update'
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
                            "user": userName,
                            #   "user": "mob_nikhil_l"

                        }

                    }

                }
                data = json.dumps(data)
                logger.info(f'{userName} [getFinalResponse] SapphireUpdate:' + str(data))
                response = requests.post(url, data=data, headers=headers, verify=False)
                response = json.loads(response.text)
                # response = {
                #     "requestType": "UPDATE_TICKET",
                #     "integrationLogId": "958104188316",
                #     "iteration": 0,
                #     "problemId": 54209,
                #     "requestNumber": "INC-010174"
                # }

                logger.info(f'{userName} [getFinalResponse] SapphireUpdateResponse:' + str(response))
                if response.get("code"):
                    # print("error")
                    ticket_fail_resp1 = response.get("message")
                    grpurl = "https://graph.workplace.com/" + post_id + "/comments"
                    print(grpurl)
                    x = {
                        'message': str(ticket_fail_resp1),
                        # 'attachment':"https://askpanda.iifl.in/ServiceBot/iiflvideos/Google/183_Google_Google_DATA_STUDIO.mp4"
                    }

                    print("----------------+8++++++++++000000000000000000000000000000007++++payload:", x)
                    response = requests.post(
                        grpurl,
                        params=auth,
                        json=x
                    )
                    print("-------------------Response:-", response)
                    return "Success"

                else:
                    if cat2.upper() == "HR":
                        ticket_success_resp = "Thank You!"
                    else:
                        ticket_success_resp = "Thank you, We have created Ticket for your issue.\n       Ticket ID :-" +" "+Ticket_id_


                    grpurl = "https://graph.workplace.com/" + post_id + "/comments"
                    print(grpurl)
                    x = {
                        'message': str(ticket_success_resp),
                        # 'attachment':"https://askpanda.iifl.in/ServiceBot/iiflvideos/Google/183_Google_Google_DATA_STUDIO.mp4"
                    }

                    print("----------------+8++++++++++000000000000000000000000000000007++++payload:", x)
                    response = requests.post(
                        grpurl,
                        params=auth,
                        json=x
                    )
                    print("-------------------Response:-", response)

            if len(uns) > 0:
                answered_query = "update answered_queries set `Feedback`='" + userResponse + "', Ticket_id='" + Ticket_id_ + "' where `query_id`=" + str(
                    queryid) + ""
                # print(answered_query)
                uns = insertquery(answered_query)

            grpurl = "https://graph.workplace.com/" + post_id + "/comments"
            print(grpurl)
            x = {
                'message': "Please Rate a Services provided(1 / 2 / 3 / 4 / 5)",
                # 'attachment':"https://askpanda.iifl.in/ServiceBot/iiflvideos/Google/183_Google_Google_DATA_STUDIO.mp4"
            }

            print("----------------+8++++++++++000000000000000000000000000000007++++payload:", x)
            response = requests.post(
                grpurl,
                params=auth,
                json=x
            )

            return "Success"

    except Exception as e:
        logger.error(f'{userID} [getFinalResponse] Exception occurred', exc_info=True)
        traceback.print_exc()
        grpurl = "https://graph.workplace.com/" + post_id + "/comments"
        print(grpurl)
        x = {
            'message': "Currently service not available",
            # 'attachment':"https://askpanda.iifl.in/ServiceBot/iiflvideos/Google/183_Google_Google_DATA_STUDIO.mp4"
        }

        print("----------------+8++++++++++000000000000000000000000000000007++++payload:", x)
        response = requests.post(
            grpurl,
            params=auth,
            json=x
        )
        print("-------------------Response:-", response)
        return "Success"

def Rating(userName,userID,rating,post_id):
    try:
        issuevalue = "yes"
        RatingDesIssue = ""

        rating_arr = {"1":"Worst","2":"Poor","3":"Average","4":"Good","5":"Excellent"}

        if rating in rating_arr.keys():
            RatingDesIssue = rating_arr[rating]

        if str(issuevalue).lower() == "yes":
            getAnswered_query = "SELECT query_id FROM `answered_queries` where `user_name`='" + userName + "' and userid='" + userID + "' order by `asked_on` desc LIMIT 1 "
            # print("getAnswered_query " + str(getAnswered_query))
            uns = create_query(getAnswered_query)
            queryid = uns[0][0]
            # print("queryid " + str(queryid))
            if len(uns) > 0:
                answered_query = "update answered_queries set `rating`=" + str(rating) + ", rating_feedback='" + str(
                    RatingDesIssue) + "' where `query_id`='" + str(queryid) + "' "
                # print(answered_query)
                uns = insertquery(answered_query)

        grpurl = "https://graph.workplace.com/" + post_id + "/comments"
        print(grpurl)
        x = {
            'message': "Thank you for your feedback",
        }
        print("----------------+8++++++++++000000000000000000000000000000007++++payload:", x)
        response = requests.post(
            grpurl,
            params=auth,
            json=x
        )

        return "Success"
        # resp = flask.Response(encrypt("Thank you for your feedback"))
        # resp.headers['Access-Control-Allow-Origin'] = '*'
        # logger.info(f'{userID} [Rating] Response:Thank you for your feedback')
        # return resp
    except Exception as e:
        print("Exception Occured " + str(e))
        grpurl = "https://graph.workplace.com/" + post_id + "/comments"
        print(grpurl)
        x = {
            'message': "Thank you for your feedback",
        }
        print("----------------+8++++++++++000000000000000000000000000000007++++payload:", x)
        response = requests.post(
        grpurl,
        params=auth,
        json=x
        )

        return "Success"


def verify_fb_token(token_sent):
    #take token sent by facebook and verify it matches the verify token you sent
    #if they match, allow the request, else return an error
    if token_sent == VERIFY_TOKEN:
        return request.args.get("hub.challenge")
    return 'Invalid verification token'


#chooses a random message to send to the user
def get_message():
    sample_responses = ["You are stunning!", "We're proud of you.", "Keep on being you!", "We're greatful to know you :)"]
    # return selected item to the user
    return random.choice(sample_responses)

#uses PyMessenger to send response to user
def send_message(recipient_id, response):
    #sends user the text message provided via input response parameter
    print("in msg")

    bot.get_user_info(recipient_id,['name','email','department','primary_phone','organization'])
    bot.send_text_message(recipient_id, response)
    return "success"

def send_image_mess(recipient_id, image_path):
    #sends user the text message provided via input response parameter
    print("in image")
    bot.send_image_url( recipient_id, "https://askpanda.iifl.in/ServiceBot/iiflimages/mouse/7.jpg")
    return "success"

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=6006, threaded=True)