
import MySQLdb as sql


production = False

if production:
    DATABASE_IP ="localhost"
    DATABASE_USERNAME = "botuser"
    DATABASE_PASSWORD = "Botuser@2020"
    DATABASE_NAME = "ExperianBot"

else:
    #DATABASE_IP = "103.90.33.118"
    DATABASE_IP = "202.66.172.133"
    DATABASE_USERNAME = "sa"
    DATABASE_PASSWORD = "Botuser@2020"
    DATABASE_NAME = "EXPBOT"
    # DATABASE_IP = "78.140.143.46"
    # DATABASE_USERNAME = "botuser"
    # DATABASE_PASSWORD = "Botuser@2020"
    #DATABASE_NAME = "indiancoins"


def insertquery(query):
    try:
        db = sql.connect(DATABASE_IP, DATABASE_USERNAME, DATABASE_PASSWORD, DATABASE_NAME, charset='utf8',
                         init_command='SET NAMES UTF8')
        cursor = db.cursor()
        cursor.execute(query)
        db.commit()
        cursor.close()
        db.close()

        return "successfully added"
    except Exception as e:
        print("ex==",e)
        return "Insertion error"

def create_query(query):
    # try:
        db = sql.connect(DATABASE_IP, DATABASE_USERNAME, DATABASE_PASSWORD, DATABASE_NAME, charset='utf8',
                     init_command='SET NAMES UTF8')
        #print("=="+db)
        cursor = db.cursor()
        cursor.execute(query)
        data = cursor.fetchall()

        print(data)
        print("Number of Rows Returned "+str(len(data)))
        cursor.close()
        db.close()
        return data
    # except:
    #     d= ()
    #     return d

# print(create_query("select location_name from taj_location"))

#query = "SELECT  SCH_GROUP_CODE , SCH_GROUP_NAME , SCH_CODE , SCH_NAME , LAUNCH_DATE , SCHEME_TYPE , SCHEME_OPTION , BROK_SCH_TYPE , NFO_FROM_DATE , NFO_TO_DATE , MCR_CATEGORY , SID_DOC , KIM_DOC , DIV_FREQUENCY , SCHEME_SUB_OPTION , Fund_Manager , MFUND_SCH_GROUP  FROM  nfo"
#
