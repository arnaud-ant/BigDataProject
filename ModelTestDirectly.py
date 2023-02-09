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


import pyaudio
import wave
import numpy as np
import os
import parameters
labels=parameters.WORD_LIST
def prediction_ask():
    print("Que souhaitez-vous dire ?")
    index=1
    for label in labels:
        print(index," pour ",label)
        index=index+1
    label_index = input()

    label=""
    flag=0
    try:
        label=labels[int(label_index)-1]
        flag=1
    except:
        print("Le numéro donner ne correspont a aucun label")
        flag=0

    # Créez les dossiers s'ils n'existent pas
    if not os.path.exists("./test/"):
        os.makedirs("./test/")
    for name in labels:
        if not os.path.exists("./test/"+name):
            os.makedirs("./test/"+name)
            
    if flag==1:
        # Récupérez tous les fichiers pour ajouter le nouveau
        file_path="./test/"+label
        number=0
        files_list = []
        for root, directories, files in os.walk(file_path):
            for name in files:
                if label in name:        
                    number = int(name.split(".wav")[0][len(name.split(".wav")[0])-1])
                    number=number+1
        newFilePath=file_path+"/"+label+str(number)+".wav"

        # Définissez les paramètres de l'enregistrement
        CHUNK = 1024
        FORMAT = pyaudio.paInt16
        CHANNELS = 2
        RATE = 44100
        RECORD_SECONDS = 2

        # Créez un objet PyAudio
        p = pyaudio.PyAudio()

        # Ouvrez un flux d'enregistrement
        stream = p.open(format=FORMAT,
                        channels=CHANNELS,
                        rate=RATE,
                        input=True,
                        frames_per_buffer=CHUNK)

        print("Enregistrement en cours...")

        # Initialisez la liste des données de l'enregistrement
        data = []

        # Boucle d'enregistrement
        for i in range(0, int(RATE / CHUNK * RECORD_SECONDS)):
            # Lisez les données du flux
            recording = stream.read(CHUNK)
            # Ajoutez les données à la liste
            data.append(recording)

        print("Enregistrement terminé")

        # Créez un fichier audio à partir des données de l'enregistrement
        wave_file = wave.open(newFilePath, "wb")
        wave_file.setnchannels(CHANNELS)
        wave_file.setsampwidth(p.get_sample_size(FORMAT))
        wave_file.setframerate(RATE)
        wave_file.writeframes(b''.join(data))
        wave_file.close()

        # Fermez le flux
        stream.stop_stream()
        stream.close()

        # Fermez l'objet PyAudio
        p.terminate()
        import pyaudio
import wave
import numpy as np
import os
import parameters
labels=parameters.WORD_LIST
# Demandez à l'utilisateur ce qu'il souhaite dire



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


def predict_test():

    if not os.path.exists("./temp/"):
        os.makedirs("./temp/")

    newFilePath="./temp/"+"1.wav"

    # Définissez les paramètres de l'enregistrement
    CHUNK = 1024
    FORMAT = pyaudio.paInt16
    CHANNELS = 2
    RATE = 44100
    RECORD_SECONDS = 4

    # Créez un objet PyAudio
    p = pyaudio.PyAudio()

    # Ouvrez un flux d'enregistrement
    stream = p.open(format=FORMAT,
                    channels=CHANNELS,
                    rate=RATE,
                    input=True,
                    frames_per_buffer=CHUNK)

    print("Enregistrement en cours...")

    # Initialisez la liste des données de l'enregistrement
    data = []

    # Boucle d'enregistrement
    for i in range(0, int(RATE / CHUNK * RECORD_SECONDS)):
        # Lisez les données du flux
        recording = stream.read(CHUNK)
        # Ajoutez les données à la liste
        data.append(recording)

    print("Enregistrement terminé")

    # Créez un fichier audio à partir des données de l'enregistrement
    wave_file = wave.open(newFilePath, "wb")
    wave_file.setnchannels(CHANNELS)
    wave_file.setsampwidth(p.get_sample_size(FORMAT))
    wave_file.setframerate(RATE)
    wave_file.writeframes(b''.join(data))
    wave_file.close()

    # Fermez le flux
    stream.stop_stream()
    stream.close()

    # Fermez l'objet PyAudio
    p.terminate()
    return make_prediction(newFilePath,"./models/conv2d_divider6_dropout0.3_epoch50.h5")
       



print(predict_test())

