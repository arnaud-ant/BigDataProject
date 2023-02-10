import json
import pymysql

"""
{
  "user_id": 1,
  "quizz_id": 1,
  "date": "2023-02-08",
  "score": 8
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

    user_id = event["user_id"]
    quizz_id = event["quizz_id"]
    date = event["date"]
    score = event["score"]

    with conn.cursor() as cur:
        res = cur.execute("INSERT INTO statistics (user_id, quizz_id, date, score) VALUES (" + user_id.__str__() + "," + quizz_id.__str__() + ",'" + date + "'," + score.__str__() + ")")
        if (res == 1):
            res = {"statusCode": 201, "body": json.dumps(event)}
        else:
            res = {"statusCode": 500, "body": json.dumps("Cannot add the statistic")}
    conn.commit()
    conn.close()
    
    return res