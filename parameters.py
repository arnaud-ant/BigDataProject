
#Preprocess.py
#Path of folder with raw data
PATH='./cv-corpus-7.0-singleword/'
#Language
LANGUAGE='fr'
#Labels that you wanna get (sentence column)
WORD_LIST=['un','deux','trois','quatre','oui','non']
#Folder to store selected wav files
STORAGE_WAV_PATH="./wav_files/"
#Folder to store wav files into classes folder

#Clean.py
#Directory where audio are stored in subdirectories (by classes)
SRC_ROOT="wav_files_classes/"+LANGUAGE+"/"
#Directory where all the resampled and splited files by delta time will be stored
DST_ROOT="clean"
#Time in second to sample the audio files
DELTA_TIME=1.0
#Sample rate to downsample audio files
SR=16000

#File to help set the threshold "common_voice_fr_21894154"
FN="common_voice_fr_23916420"
#Duration of the window in seconds
TIME_WINDOW=0.4


STORAGE_WAV_PATH_CLASSES="./wav_files_classes/"


#Train
#Type of model that we want they are stored in models.py
MODEL_TYPE="conv2d"
#Batch_size
BATCH_SIZE=16
#False if you wanna train it from scratch or True if you wanna keep the data you trained it on before
LOAD_MODEL=False

#Test/Prediction
#File name of the model that you wanna use to predict with
MODEL_FN='models/conv2d.h5'
#File name to write the predictions in
PRED_FN='predictions'
#Foloder with files to predict
PRED_DIR='enregistrements'

#Divider ratio to divide average of maxes to get thresholds must be an array of at least 1 element
DIVIDER=[6]
#Number of epoch must be an array
EPOCH=[50]#[10,20,30,40,50]
#Dropout must be an array 
DROPOUT=[0.5]#[0.1,0.3,0.5,0.7,0.9]
