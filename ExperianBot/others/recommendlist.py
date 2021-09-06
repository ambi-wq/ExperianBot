import csv
from model.MySQLHelper import insertquery, create_query

with open('RecommendationListSuperEBot.csv', newline='') as f:
    reader = csv.reader(f)


    data = [row[0] for row in reader]

print(data)
print(len(data))
ids = create_query("select sub_id from sub_type where sub_id >= '1' ")
print(ids)
ids = list(ids)
print(len(ids))
for (a, b) in zip(ids, data):
    print(a[0])
    insertquery('UPDATE sub_type SET `Sub_Type` = "'+b+'" WHERE sub_id = '+str(a[0])+'')


# for i in range(1,109):
#     print(i)