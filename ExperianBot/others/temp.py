import random
from ExperianBot.model.MySQLHelpertemp import create_query,insertquery
from googletrans import Translator
from textblob import TextBlob

# a = ['Discounts', 'Employee Assistance Program', 'Exit', 'Generic', 'Joining', 'Leaves & Attendance', 'Recruitment & Selection', 'Reward and Recognition', 'Statutory Compliances', 'Work Related Benefits', 'World of Privileges']
# try:
#     for i in range(43, 5751):
#         randomnum = random.randint(0, 10)
#         query = "update answered_queries set category='" + a[randomnum] + "' where query_id = " + str(i) +";"
#         insertquery(query)
# except Exception as e:
#     print(e)

# translator = Translator()

# issue_id = 5
# s = "Taj Swagat Start Time"


# query = "UPDATE operations_MyTaj SET hint_mr = N'ताज स्वगत प्रारंभ वेळ' WHERE issue_id = '"+str(issue_id)+"';"
# insertquery(query)


for i in range(91,101):
    print(i)
    query1 = "SELECT response FROM operations_MyTaj WHERE issue_id = '"+str(i)+"' AND Location_id = 'LOCATION1';"
    res = create_query(query1)

    s = str(res[0][0])
    print("s",s)
    blob = TextBlob(s)
    # print(blob.translate(to='hi'))
    hindi = blob.translate(to='hi')
    print(hindi)
    #hindi = ""
    gujrati = blob.translate(to='gu')
    print(gujrati)
    #gujrati = ""
    ml = blob.translate(to='ml')
    #ml = ""
    marathi = blob.translate(to='mr')
    #marathi = ""

    pa = blob.translate(to='pa')
    print(pa)
    #pa = ""
    ta = blob.translate(to='ta')
    #ta = ""
    te = blob.translate(to='te')
    #te = ""
    ur = blob.translate(to='ur')
    #ur = ""

    query = "UPDATE operations_MyTaj SET hi = N'"+str(hindi)+"',gu= N'"+str(gujrati)+"' ,ml = N'"+str(ml)+"', mr = N'"+str(marathi)+"',pa= N'"+str(pa)+"', ta= N'"+str(ta)+"', te = N'"+str(te)+"', ur= N'"+str(ur)+"' WHERE issue_id = '"+str(i)+"' AND Location_id = 'LOCATION1';"
    insertquery(query)
