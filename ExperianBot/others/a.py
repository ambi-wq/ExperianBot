
import re
import unicodedata
import requests
from textblob import TextBlob
# query_response = "You can apply future dated leave through the For any other questions on the Leave policy click here:<br>   http://econnect.fullertonindia.local/jonction/spaces/files/default/?spaceID=3&spaceName=policies&directoryID=118#"

def Find(string):
    # findall() has been used
    # with valid conditions for urls in string
    regex = r"(?i)\b((?:https?://|www\d{0,3}[.]|[a-z0-9.\-]+[.][a-z]{2,4}/)(?:[^\s()<>]+|\(([^\s()<>]+|(\([^\s()<>]+\)))*\))+(?:\(([^\s()<>]+|(\([^\s()<>]+\)))*\)|[^\s`!()\[\]{};:'\".,<>?«»“”‘’]))"
    url = re.findall(regex, string)
    return [x[0] for x in url]

from model.MySQLHelper import insertquery, create_query

query = "select operation_id,title,response from operations_temp where operation_id =236 order by operation_id desc"
response = create_query(query)
print(response)
language= ["gu","hi","ml","mr","pa","ta","te","ur"]
for res in response:
    # print(a)
    for lan in language:
        print("___________________________________________________________________")
        print(res)
        print("___________________________________________________________________")
        query_response = str(res[2])
        print(query_response)
        print(query_response)
        appen=""
        if "##C##" in query_response:
            query_response = query_response.replace("##C##","")
            appen="##C##"
        if "##form##" in query_response:
            query_response= query_response.replace("##form##","")
            appen = "##form##"
        if "http" in query_response or "www"in query_response:
            a = Find(query_response)
            print(a)
            for count,link in enumerate(a):
                print("link = ",link)
                print(count)
                print("before",query_response)
                query_response = query_response.replace(str(link), "#######")
                print("replaced",query_response)


        print(language)
        hi_blob1 = TextBlob(query_response)
        query_response = hi_blob1.translate(to=lan)
        query_response = str(query_response)+appen
        query_response = query_response.replace("'","")
        if "#######" in query_response:
            for count,link in enumerate(a):
                query_response = query_response.replace("#######", link)
                print("replaced2", query_response)
        query = "UPDATE `operations_temp` SET `"+lan+"` = '"+query_response+"' WHERE `operations_temp`.`operation_id` = '"+str(res[0])+"';"
        inserttransa= insertquery(query)
        print(query_response)