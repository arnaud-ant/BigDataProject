
from clean import downsample_mono, envelope,get_threshold
from keras.models import load_model
from kapre.time_frequency import STFT, Magnitude, ApplyFilterbank, MagnitudeToDecibel
from sklearn.preprocessing import LabelEncoder
import numpy as np
from glob import glob
import argparse
import os
import pandas as pd
from tqdm import tqdm
import parameters

pred_fn=parameters.PRED_FN
src_dir=parameters.PRED_DIR
dt=parameters.DELTA_TIME
sr=parameters.SR

def make_prediction(divider,dropout,epoch):
    df=pd.DataFrame(['Actual class'])
    df=pd.concat([df,pd.DataFrame(['Prediction'])],axis=1)
    model_fn="models/conv2d_divider"+str(divider)+"_dropout"+str(dropout)+"_epoch"+str(epoch)+".h5"
    print(model_fn)
    model = load_model(model_fn,
        custom_objects={'STFT':STFT,
                        'Magnitude':Magnitude,
                        'ApplyFilterbank':ApplyFilterbank,
                        'MagnitudeToDecibel':MagnitudeToDecibel})
    wav_paths = glob('{}/**'.format(src_dir), recursive=True)
    wav_paths = sorted([x.replace(os.sep, '/') for x in wav_paths if '.wav' in x])
    classes = sorted(os.listdir(src_dir))
    labels = [os.path.split(x)[0].split('/')[-1] for x in wav_paths]
    le = LabelEncoder()
    y_true = le.fit_transform(labels)
    results = []

    for z, wav_fn in tqdm(enumerate(wav_paths), total=len(wav_paths)):
        rate, wav = downsample_mono(wav_fn, sr)
        threshold=get_threshold(wav,divider=divider)
        mask, env = envelope(wav, rate, threshold=threshold)
        clean_wav = wav[mask]
        step = int(sr*dt)
        batch = []

        for i in range(0, clean_wav.shape[0], step):
            sample = clean_wav[i:i+step]
            sample = sample.reshape(-1, 1)
            if sample.shape[0] < step:
                tmp = np.zeros(shape=(step, 1), dtype=np.float32)
                tmp[:sample.shape[0],:] = sample.flatten().reshape(-1, 1)
                sample = tmp
            batch.append(sample)
        X_batch = np.array(batch, dtype=np.float32)
        y_pred = model.predict(X_batch)
        y_mean = np.mean(y_pred, axis=0)
        y_pred = np.argmax(y_mean)
        real_class = os.path.dirname(wav_fn).split('/')[-1] 
        df_temp=pd.DataFrame([real_class])
        dftemp=pd.concat([df_temp,pd.DataFrame([classes[y_pred]])],axis=1)
        df=pd.concat([df,dftemp],axis=0)
        print('Actual class: {}, Predicted class: {}'.format(real_class, classes[y_pred]))

        results.append(y_mean)
    df.to_csv(os.path.join('logs/predict_log', pred_fn+"divider"+str(divider)+"_dropout"+str(dropout)+"_epoch"+str(epoch)+".csv"))
    


def main():
    for divider in parameters.DIVIDER:
        for epoch in parameters.EPOCH:
            for dropout in parameters.DROPOUT:
                make_prediction(divider,dropout,epoch)
