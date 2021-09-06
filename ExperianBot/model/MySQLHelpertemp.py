
import pyodbc as mssql


#
# def create_query(query):
#     conn = mssql.connect("Driver={SQL Server};"
#                         "Server=78.140.143.46,1232;"
#                         "Database=ipruamcmssql;"
#                         "uid=sa;pwd=SOz@Rg5BmbD*qYiCrgB;"
#                         "Trusted_Connection = yes;")
#
#     cursor = conn.cursor()
#     cursor.execute(query)
#     data = cursor.fetchall()
#
#     print("Number of Rows Returned "+str(len(data)))
#     conn.close()
#     return data
# def insertquery(query):
#     conn = mssql.connect("Driver={SQL Server};"
#                          "Server=78.140.143.46,1232;"
#                          "Database=ipruamcmssql;"
#                          "uid=sa;pwd=SOz@Rg5BmbD*qYiCrgB;"
#                          "Trusted_Connection = yes;")
#
#
#     cursor = conn.cursor()
#     cursor.execute(query)
#     conn.commit()
#     cursor.close()
#     conn.close()
#     return "successfully added"
#
def create_query(query):
    print("CreateQuery")
    conn = mssql.connect("Driver={SQL Server};"
                        "Server=202.66.172.133,1232;"
                        "Database=EXPBOT;"
                        "uid=sa;pwd=SOz@Rg5BmbD*qYiCrgB;"
                        "Trusted_Connection = yes;")

    cursor = conn.cursor()
    # print("<<<<==========================================QUERY==========================================>>>>")
    # print(query)
    cursor.execute(query)
    # print("<<<<==========================================QUERY==========================================>>>>")
    data = cursor.fetchall()
    # print("==========data=============>>>>"+str(data))
    print("Number of Rows Returned "+str(len(data)))
    conn.close()
    data=tuple(data)
    return data

def insertquery(query):
    conn = mssql.connect("Driver={SQL Server};"
                         "Server=202.66.172.133,1232;"
                         "Database=EXPBOT;"
                         "uid=sa;pwd=SOz@Rg5BmbD*qYiCrgB;"
                         "Trusted_Connection = yes;")
    cursor = conn.cursor()
    cursor.execute(query)
    conn.commit()
    cursor.close()
    conn.close()
    return "successfully added"

# s = create_query("select location_name from taj_location")
# print(list(s))
# res = list(s)
# res1 = []
# for i in res:
#     res1.append(i[0])
#
# print(res1)