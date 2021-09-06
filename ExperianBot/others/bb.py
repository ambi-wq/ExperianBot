from model.MySQLHelper import create_query,insertquery
import json
from datetime import datetime,timedelta
user = "0"

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
            "googleFlag": data[4],
            "outlookFlag": data[5],
            # "query": data[8],
            # "flag" : data[9],
            "message": "Please help me with the below mentioned details for your Reminder.##RemForm##",
            "response": "Please help me with the below mentioned details for your Reminder.##RemForm##",

        }
        json_array.append(sim)
    json_data = {"message": "Please help me with the below mentioned details for your Reminder.##RemForm##",
                 "ParameterTitle": "",
                 "ParameterType": "",
                 "action": json_array}
    data1 = json.dumps(json_data, sort_keys=True, indent=4 * ' ')
    data = data1
    data2 = json.dumps(json_data)
    print("json data ==> ", data)
    formdata = "UPDATE chat_history SET query = '" + data2 + "' where asked_on < '" + currenttime + "' order by id desc limit 1"
    query = insertquery(formdata)
    print(query)