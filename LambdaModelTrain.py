from scipy.io import wavfile
import os
from glob import glob
import numpy as np
from librosa.core import resample, to_mono
from tqdm import tqdm
import wavio
from keras.utils import to_categorical,Sequence
from keras.callbacks import  ModelCheckpoint

delta_time=1.0
sr=16000
divider=6

import pandas as pd
from keras.models import load_model
from kapre.time_frequency import STFT, Magnitude, ApplyFilterbank, MagnitudeToDecibel
from sklearn.preprocessing import LabelEncoder
import numpy as np

dt=delta_time

def train_model(wav_enr,model_file,label):
    df=pd.DataFrame(['Actual class'])
    df=pd.concat([df,pd.DataFrame(['Prediction'])],axis=1)
    model_fn=model_file
    model = load_model(model_fn,
        custom_objects={'STFT':STFT,
                        'Magnitude':Magnitude,
                        'ApplyFilterbank':ApplyFilterbank,
                        'MagnitudeToDecibel':MagnitudeToDecibel})
    classes = sorted(['Un','Deux','Trois','Quatre','Oui','Non'])
    target_dir = os.path.join("./temp", label)
    cp = ModelCheckpoint(model_file, monitor='val_loss', save_weights_only=False,
                        mode='auto', save_freq='epoch', verbose=1)
    wav_paths = glob('{}/**'.format(target_dir), recursive=True)
    wav_paths = [x.replace(os.sep, '/') for x in wav_paths if '.wav' in x]
    print(wav_paths)
    tg = DataGenerator(wav_paths, label, sr, dt,  
                       6, batch_size=1)
    model.fit(tg, 
              epochs=1, verbose=1,
              callbacks=[cp])
    return True


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
    fn = fn.split('.wav')[0].split("/")[len(fn.split('.wav')[0].split("/"))-1]
    dst_path = os.path.join(target_dir, fn+'_{}.wav'.format(str(ix)))
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


def split_wavs(wav_enr,model_file,label):
    dt=delta_time
    wav_paths = wav_enr
    wav_paths = [x for x in wav_paths if '.wav' in x]
    classes = sorted(['Un','Deux','Trois','Quatre','Oui','Non'])
    check_dir("./temp")
    for _cls in classes:
        target_dir = os.path.join("./temp", _cls)
        check_dir(target_dir)   
        if(_cls==label): 
            src_fn = wav_enr
            rate, wav = downsample_mono(src_fn, sr)
            threshold=get_threshold(wav)
            mask, y_mean = envelope(wav, rate, threshold=threshold)
            wav = wav[mask]
            delta_sample = int(dt*rate)

            # cleaned audio is less than a single sample
            # pad with zeros to delta_sample size
            if wav.shape[0] < delta_sample:
                sample = np.zeros(shape=(delta_sample,), dtype=np.int16)
                sample[:wav.shape[0]] = wav
                save_sample(sample, rate, target_dir, wav_enr, 0)
            # step through audio and save every delta_sample
            # discard the ending audio if it is too short
            else:
                trunc = wav.shape[0] % delta_sample
                for cnt, i in enumerate(np.arange(0, wav.shape[0]-trunc, delta_sample)):
                    start = int(i)
                    stop = int(i + delta_sample)
                    sample = wav[start:stop]
                    save_sample(sample, rate, target_dir, wav_enr, cnt)
    return train_model(wav_enr,model_file,label)

class DataGenerator(Sequence):
    def __init__(self, wav_paths, labels, sr, dt, n_classes,
                 batch_size=32, shuffle=True):
        self.wav_paths = wav_paths
        self.labels = labels
        self.sr = sr
        self.dt = dt 
        self.n_classes = n_classes
        self.batch_size = batch_size
        self.shuffle = True
        self.on_epoch_end()


    def __len__(self):
        return int(np.floor(len(self.wav_paths) / self.batch_size))


    def __getitem__(self, index):

        # generate a batch of time data
        X = np.empty((self.batch_size, int(self.sr*self.dt), 1), dtype=np.float32)
        Y = np.empty((self.batch_size, self.n_classes), dtype=np.float32)
        classes = sorted(['Un','Deux','Trois','Quatre','Oui','Non'])
        le = LabelEncoder()
        le.fit(classes)
        labels = le.transform([self.labels])
        rate, wav = wavfile.read(self.wav_paths[0])
        X[0,] = wav.reshape(-1, 1)
        Y[0,] = to_categorical(labels, num_classes=self.n_classes)

        return X, Y


    def on_epoch_end(self):
        self.indexes = np.arange(len(self.wav_paths))
        if self.shuffle:
            np.random.shuffle(self.indexes)
DataGenerator


print(split_wavs("./enregistrements/oui/oui10.wav","./models/conv2d_divider6_dropout0.5_epoch50.h5","Oui"))