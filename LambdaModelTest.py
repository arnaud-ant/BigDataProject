from scipy.io import wavfile
import os
from glob import glob
import numpy as np
from librosa.core import resample, to_mono
from tqdm import tqdm
import wavio

delta_time=1.0
sr=16000
divider=6

import pandas as pd
from keras.models import load_model
from kapre.time_frequency import STFT, Magnitude, ApplyFilterbank, MagnitudeToDecibel
from sklearn.preprocessing import LabelEncoder
import numpy as np

dt=delta_time


def make_prediction(wav_enr,model):
    model_fn=model
    model = load_model(model_fn,
        custom_objects={'STFT':STFT,
                        'Magnitude':Magnitude,
                        'ApplyFilterbank':ApplyFilterbank,
                        'MagnitudeToDecibel':MagnitudeToDecibel})
    classes = sorted(['Un','Deux','Trois','Quatre','Oui','Non'])
    le = LabelEncoder()
    y_true = le.fit_transform(classes)
    results = []
    rate, wav = downsample_mono(wav_enr, sr)
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
    return(classes[y_pred])


def envelope(y, rate, threshold):
    mask = []
    y = pd.Series(y).apply(np.abs)
    y_mean = y.rolling(window=int(rate/20),
                       min_periods=1,
                       center=True).max()
    for mean in y_mean:
        if mean > threshold:
            mask.append(True)
        else:
            mask.append(False)
    return mask, y_mean


def downsample_mono(path, sr):
    obj = wavio.read(path)
    wav = obj.data.astype(np.float32, order='F')
    rate = obj.rate
    try:
        channel = wav.shape[1]
        if channel == 2:
            wav = to_mono(wav.T)
        elif channel == 1:
            wav = to_mono(wav.reshape(-1))
    except IndexError:
        wav = to_mono(wav.reshape(-1))
        pass
    except Exception as exc:
        raise exc
    wav = resample(wav, rate, sr)
    wav = wav.astype(np.int16)
    return sr, wav


def save_sample(sample, rate, target_dir, fn, ix):
    fn = fn.split('.wav')[0]
    dst_path = os.path.join(target_dir.split('.')[0], fn+'_{}.wav'.format(str(ix)))
    if os.path.exists(dst_path):
        return
    wavfile.write(dst_path, rate, sample)


def check_dir(path):
    if os.path.exists(path) is False:
        os.mkdir(path)

def get_area(wav,sliding_window,x):
    area=0
    if(sliding_window+x <= len(wav)):
        for indice in range(0,sliding_window):
            area=area+ abs(wav[x+indice])
    return area
    
def get_max_X_area(wav,sliding_window):
    max_X=0
    max_area=0
    for indice in np.arange(0,len(wav),round(sliding_window/50)):
        area=get_area(wav,sliding_window,indice)
        if(max_area<=area):
            max_area=area
            max_X=indice
    return max_X

def get_maxes_amplitude(wav,sliding_window,x):
    max_y=0
    max_Y_X=0
    max_Y2=0
    for indice in range(0,sliding_window):
        if(sliding_window+indice <= len(wav)):
            if max_y<abs(wav[x+indice]):
                max_y=abs(wav[x+indice])
                max_Y_X=x+indice
    for indice in range(0,sliding_window):
        if(sliding_window+indice <= len(wav)):
            if max_Y2<abs(wav[x+indice]) and abs(max_Y_X-(x+indice))>sliding_window*0.2:
                max_Y2=abs(wav[x+indice])
    return int(max_y),int(max_Y2)

def get_threshold(wav,time_window=0.4,sr=16000,divider=divider):
    sliding_window=round(time_window*sr)
    max_x=get_max_X_area(wav,sliding_window)
    max_1,max_2=get_maxes_amplitude(wav,sliding_window,max_x)
    max_avg_amplitude=(max_1+max_2)/2
    return max_avg_amplitude/divider

print(make_prediction("./enregistrements/oui/oui10.wav","./models/conv2d_divider6_dropout0.5_epoch50.h5"))