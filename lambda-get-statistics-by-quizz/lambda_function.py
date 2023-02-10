import json
import pymysql

"""
{
  "id": 1
}
"""

rds_host  = "database-big-data.c5bwz5okbrmn.us-east-1.rds.amazonaws.com"
db_username = "admin"
db_password = "aqwzsx1234"
db_name = "BigDataDB"

def lambda_handler(event, context):
    
    try:
        conn = pymysql.connect(host=rds_host, user=db_username, password=db_password, database=db_name)
    except pymysql.MySQLError as e:
        return {"statusCode": 500, "body": json.dumps(e.__str__())}

    id = event["id"]

    with conn.cursor() as cur:
        cur.execute("SELECT * FROM statistics WHERE quizz_id=" + id.__str__())
        stats = cur.fetchall()
        
        if (stats.__len__() == 0):
            res = {"statusCode": 401, "body": json.dumps("No statistics for this quizz")}
        else:
            res = {"statusCode": 200, "body": json.dumps(stats)}
    conn.commit()
    conn.close()

    return res
