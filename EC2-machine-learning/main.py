import json
import tempfile
import boto3
from LambdaModelTest import make_prediction
from LambdaModelTrain import split_wavs

from fastapi import FastAPI, HTTPException
import uvicorn

app = FastAPI()

aws_access_key_id = "ASIARQRVCA2Q2NJJUDV2"
aws_secret_access_key = "fbfXIYAeCyrwsQOa8OSP20lyPJoCpQ7F69NfIsh4"
aws_session_token = "FwoGZXIvYXdzEB8aDJc4wKZUUu2Bw0ggTSK9AeZcYY772wQAukgYXOg4XLsD2ZdibWNvWv5bncrPsanlIPxKeS2OYRLUH8eSapdcFH1eBxaocgwuYbkbQgGJb5HkkDxMpdVP1E26Ylo44YCFkyOJ1k"

s3_client = boto3.client("s3", aws_access_key_id=aws_access_key_id, aws_secret_access_key=aws_secret_access_key, aws_session_token=aws_session_token)
audio_bucket = "big-data-audio-file"
model_bucket = "big-data-model"
model_name = "conv2d_divider6_dropout0.5_epoch50.h5"

@app.get("/")
async def root():
    print("Hello world")
    return "hello-world"

@app.get("/test")
async def test_handler(file: str):
    print("===== TEST MODEL =====")

    audio_file = file
    print("Audio file name: " + audio_file)

    # Get the audio file
    for key in s3_client.list_objects(Bucket=audio_bucket)['Contents']:
        print(key['Key'])
    response = s3_client.get_object(Bucket=audio_bucket, Key=audio_file)
    audio_content = response['Body'].read()

    # Get the model 
    response = s3_client.get_object(Bucket=model_bucket, Key=model_name)
    model_content = response['Body'].read()

    with tempfile.NamedTemporaryFile(suffix='.wav', delete=True) as audio_temp:
        audio_temp.write(audio_content)
        print("Audio Temp File: " + audio_temp.name)

        with tempfile.NamedTemporaryFile(suffix='.h5', delete=True) as model_temp:
            model_temp.write(model_content)
            print("Model Temp File: " + model_temp.name)

            res = make_prediction(audio_temp.name, model_temp.name)
            print("Result: " + res)

            s3_client.delete_object(Bucket=audio_bucket, Key=audio_file)
            return res

@app.get("/train")
async def train_handler(file: str, label: str):
    print("===== TRAIN MODEL =====")

    audio_file = file
    print("Audio file name: " + audio_file)

    label = label
    print("Label: " + label)

    # Get the audio file
    response = s3_client.get_object(Bucket=audio_bucket, Key=audio_file)
    audio_content = response['Body'].read()

    # Get the model
    response = s3_client.get_object(Bucket=model_bucket, Key=model_name)
    model_content = response['Body'].read()

    with tempfile.NamedTemporaryFile(suffix='.wav', delete=True) as audio_temp:
        audio_temp.write(audio_content)
        print("Audio Temp File: " + audio_temp.name)

        with tempfile.NamedTemporaryFile(suffix='.h5', delete=True) as model_temp:
            model_temp.write(model_content)
            print("Model Temp File: " + model_temp.name)

            res = split_wavs(audio_temp.name, model_temp.name, label)
            print("Result: " + res)

            if(res):
                return {"statusCode": 200, "body": json.dumps(res)}
            else :
                return {"statusCode": 400, "body": json.dumps(res)}

if __name__ == "__main__":
    config = uvicorn.Config("main:app", reload=True, port=8000, log_level="info", host="0.0.0.0")
    server = uvicorn.Server(config)
    server.run()