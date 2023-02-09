import pandas as pd
import numpy as np
import librosa
from pydub import AudioSegment
import os
from sklearn.model_selection import train_test_split
import parameters
PATH=parameters.PATH
LANGUAGE=parameters.LANGUAGE
WORD_LIST=parameters.WORD_LIST
STORAGE_WAV_PATH=parameters.STORAGE_WAV_PATH
STORAGE_WAV_PATH_CLASSES=parameters.STORAGE_WAV_PATH_CLASSES


def Convert_MP3_to_WAV(input_path,output_path):
    sound = AudioSegment.from_mp3(input_path)
    sound.export(output_path, format="wav")
    return output_path


def Convert_All_files_to_WAV_Into_Classes_folder(path=PATH,language=LANGUAGE,labels=WORD_LIST,storage_wav_path=STORAGE_WAV_PATH_CLASSES):
    file_path_test=['/test.tsv']
    file_path=['/train.tsv']
    file_number=0
    for file in file_path:
        path_tsv=path+language+file

        validated_df=pd.read_csv(path_tsv, sep='\t',encoding='latin1')
        if not os.path.exists(storage_wav_path+language+"/"):
            os.makedirs(storage_wav_path+language+"/")
        #Keep only the words from word_list
        validated_df=validated_df[validated_df['sentence'].apply(lambda x: x in labels)]
        progression=0
        #iterate on all files
        for label in labels:
            if not os.path.exists(storage_wav_path+language+"/"+label+"/"):
                os.makedirs(storage_wav_path+language+"/"+label+"/")
            #iterate on all files
            for ind in validated_df.loc[validated_df["sentence"]==label].index:
                file_path=PATH+language+'/clips/'+validated_df['path'][ind]
                new_file_path=storage_wav_path+language+"/"+label+"/"+file_path.split('.mp3')[0].split('/clips/')[1]+'.wav'
                Convert_MP3_to_WAV(file_path,new_file_path)
                print(label,":",progression,"/",validated_df.index.max())
                progression=progression+1
                file_number=file_number+1
    print("Number of data: ",file_number)
    storage_wav_path=storage_wav_path+"_test"
    file_number=0
    for file in file_path:
        path_tsv=path+language+file

        validated_df=pd.read_csv(path_tsv, sep='\t',encoding='latin1')
        if not os.path.exists(storage_wav_path+language+"/"):
            os.makedirs(storage_wav_path+language+"/")
        #Keep only the words from word_list
        validated_df=validated_df[validated_df['sentence'].apply(lambda x: x in labels)]
        progression=0
        #iterate on all files
        for label in labels:
            if not os.path.exists(storage_wav_path+language+"/"+label+"/"):
                os.makedirs(storage_wav_path+language+"/"+label+"/")
            #iterate on all files
            for ind in validated_df.loc[validated_df["sentence"]==label].index:
                file_path=PATH+language+'/clips/'+validated_df['path'][ind]
                new_file_path=storage_wav_path+language+"/"+label+"/"+file_path.split('.mp3')[0].split('/clips/')[1]+'.wav'
                Convert_MP3_to_WAV(file_path,new_file_path)
                print(label,":",progression,"/",validated_df.index.max())
                progression=progression+1
                file_number=file_number+1
    print("Number of data test : ",file_number)


def main():
    Convert_All_files_to_WAV_Into_Classes_folder()