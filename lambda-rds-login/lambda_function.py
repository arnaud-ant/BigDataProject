import json
import pymysql

"""
{
  "login": "admin",
  "password": "admin"
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

    login = event["login"]
    password = event["password"]

    with conn.cursor() as cur:
        cur.execute("SELECT * FROM user WHERE login='" + login + "'")
        user = cur.fetchone()
        
        if(user):
            if (user[2] == password):
                res = {"statusCode": 200, "body": json.dumps(user)}
            else :
                res = {"statusCode": 401, "body": json.dumps("Invalid password")}
        else :
            res = {"statusCode": 401, "body": json.dumps("Invalid login")}
    conn.commit()
    conn.close()

    return res
