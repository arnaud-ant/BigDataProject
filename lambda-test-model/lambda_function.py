import json
import requests

"""
{
  "key": "fichier.wav"
}
"""

def lambda_handler(event, context):
    
    audio_file = event["key"]
    print("Audio file name: " + audio_file)
    response = requests.get("http://ec2-54-145-225-156.compute-1.amazonaws.com:8000/test/?file="+ audio_file + "")
    print(response.content)
    
    return {
        'statusCode': 200,
        'body': response.content
    }
