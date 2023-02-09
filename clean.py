import matplotlib.pyplot as plt
from scipy.io import wavfile
import os
from glob import glob
import numpy as np
import pandas as pd
from librosa.core import resample, to_mono
from tqdm import tqdm
import wavio
import parameters

src_root=parameters.SRC_ROOT
dst_root=parameters.DST_ROOT
delta_time=parameters.DELTA_TIME
sr=parameters.SR
divider=1
fn=parameters.FN
time_window=parameters.TIME_WINDOW
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

def get_threshold(wav,time_window=parameters.TIME_WINDOW,sr=parameters.SR,divider=divider):
    sliding_window=round(time_window*sr)
    max_x=get_max_X_area(wav,sliding_window)
    max_1,max_2=get_maxes_amplitude(wav,sliding_window,max_x)
    max_avg_amplitude=(max_1+max_2)/2
    return max_avg_amplitude/divider

def split_wavs():
    dt=delta_time
    wav_paths = glob('{}/**'.format(src_root), recursive=True)
    wav_paths = [x for x in wav_paths if '.wav' in x]
    dirs = os.listdir(src_root)
    check_dir(dst_root)
    classes = os.listdir(src_root)
    for _cls in classes:
        target_dir = os.path.join(dst_root, _cls)
        check_dir(target_dir)
        src_dir = os.path.join(src_root, _cls)
        for fn in tqdm(os.listdir(src_dir)):
            src_fn = os.path.join(src_dir, fn)
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
                save_sample(sample, rate, target_dir, fn, 0)
            # step through audio and save every delta_sample
            # discard the ending audio if it is too short
            else:
                trunc = wav.shape[0] % delta_sample
                for cnt, i in enumerate(np.arange(0, wav.shape[0]-trunc, delta_sample)):
                    start = int(i)
                    stop = int(i + delta_sample)
                    sample = wav[start:stop]
                    save_sample(sample, rate, target_dir, fn, cnt)


def test_threshold():

    wav_paths = glob('{}/**'.format(src_root), recursive=True)
    wav_path = [x for x in wav_paths if fn in x]
    if len(wav_path) != 1:
        print('Could not find a file for sub-string: {}'.format(fn))
        return
    rate, wav = downsample_mono(wav_path[0], sr)
    threshold=get_threshold(wav)
    mask, env = envelope(wav, rate, threshold=threshold)
    plt.style.use('ggplot')
    plt.title('Signal Envelope, Threshold = {}'.format(str(threshold)))
    plt.plot(wav[np.logical_not(mask)], color='r', label='remove')
    plt.plot(wav[mask], color='c', label='keep')
    plt.plot(env, color='m', label='envelope')
    plt.grid(False)
    plt.legend(loc='best')
    plt.show()
    return input("Le seuil est-il bon ? y/n")

def main():
    for i in parameters.DIVIDER:
        global dst_root
        global divider
        dst_root=parameters.DST_ROOT+"_divider"+str(i)
        divider=i
        split_wavs()



   
