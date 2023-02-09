import json
import tempfile
import boto3
from LambdaModelTest import make_prediction
from LambdaModelTrain import split_wavs

s3_client = boto3.client("s3")
audio_bucket = "big-data-audio-file"
model_bucket = "big-data-model"
model_name = "conv2d_divider6_dropout0.5_epoch50.h5"

def test_handler(event, context):
    print("===== TEST MODEL =====")

    audio_file = event["audio_file"]
    print("Audio file name: " + audio_file)

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

            res = make_prediction(audio_temp.name, model_temp.name)
            print("Result: " + res)

            return {"statusCode": 200, "body": json.dumps(res)}

def train_handler(event, context):
    print("===== TRAIN MODEL =====")

    audio_file = event["audio_file"]
    print("Audio file name: " + audio_file)

    label = event["label"]
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
