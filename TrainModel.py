import tensorflow as tf
from keras.callbacks import CSVLogger, ModelCheckpoint
from keras.utils import to_categorical
import os
from scipy.io import wavfile
import pandas as pd
import numpy as np
from sklearn.utils.class_weight import compute_class_weight
from sklearn.preprocessing import LabelEncoder
from sklearn.model_selection import train_test_split
from models import Conv1D_, Conv2D_, LSTM_
from tqdm import tqdm
from glob import glob
import warnings
import parameters
from keras.models import load_model
from kapre.time_frequency import STFT, Magnitude, ApplyFilterbank, MagnitudeToDecibel
import clean
#import



model_type=parameters.MODEL_TYPE
src_root=parameters.DST_ROOT
batch_size=parameters.BATCH_SIZE
delta_time=dt=parameters.DELTA_TIME
sample_rate=sr=parameters.SR
load_model_bool=parameters.LOAD_MODEL
model_fn=parameters.MODEL_FN
class DataGenerator(tf.keras.utils.Sequence):
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
        indexes = self.indexes[index*self.batch_size:(index+1)*self.batch_size]

        wav_paths = [self.wav_paths[k] for k in indexes]
        labels = [self.labels[k] for k in indexes]

        # generate a batch of time data
        X = np.empty((self.batch_size, int(self.sr*self.dt), 1), dtype=np.float32)
        Y = np.empty((self.batch_size, self.n_classes), dtype=np.float32)

        for i, (path, label) in enumerate(zip(wav_paths, labels)):
            rate, wav = wavfile.read(path)
            X[i,] = wav.reshape(-1, 1)
            Y[i,] = to_categorical(label, num_classes=self.n_classes)

        return X, Y


    def on_epoch_end(self):
        self.indexes = np.arange(len(self.wav_paths))
        if self.shuffle:
            np.random.shuffle(self.indexes)
DataGenerator

def train(epoch,dropout):
    params = {'dropout':dropout,
              'N_CLASSES':len(os.listdir(src_root)),
              'SR':sr,
              'DT':dt}
    models = {#'conv1d':Conv1D_(**params),
              'conv2d':Conv2D_(**params)#,
              #'lstm':  LSTM_(**params)
              }
    assert model_type in models.keys(), '{} not an available model'.format(model_type)
    csv_path = os.path.join('logs/train_log', '{}_history.csv'.format(model_type+"_divider"+str(divider)+"_dropout"+str(dropout)+"_epoch"+str(epoch)))

    wav_paths = glob('{}/**'.format(src_root), recursive=True)
    wav_paths = [x.replace(os.sep, '/') for x in wav_paths if '.wav' in x]
    classes = sorted(os.listdir(src_root))
    le = LabelEncoder()
    le.fit(classes)
    labels = [os.path.split(x)[0].split('/')[-1] for x in wav_paths]
    labels = le.transform(labels)
    wav_train, wav_val, label_train, label_val = train_test_split(wav_paths,
                                                                  labels,
                                                                  test_size=0.1,
                                                                  random_state=0)

    assert len(label_train) >= batch_size, 'Number of train samples must be >= batch_size'
    if len(set(label_train)) != params['N_CLASSES']:
        warnings.warn('Found {}/{} classes in training data. Increase data size or change random_state.'.format(len(set(label_train)), params['N_CLASSES']))
    if len(set(label_val)) != params['N_CLASSES']:
        warnings.warn('Found {}/{} classes in validation data. Increase data size or change random_state.'.format(len(set(label_val)), params['N_CLASSES']))

    tg = DataGenerator(wav_train, label_train, sr, dt,
                       params['N_CLASSES'], batch_size=batch_size)
    vg = DataGenerator(wav_val, label_val, sr, dt,
                       params['N_CLASSES'], batch_size=batch_size)
    model=""
    if(load_model_bool):
        model = load_model(model_fn,
        custom_objects={'STFT':STFT,
                        'Magnitude':Magnitude,
                        'ApplyFilterbank':ApplyFilterbank,
                        'MagnitudeToDecibel':MagnitudeToDecibel})
    else:
        model = models[model_type]
    cp = ModelCheckpoint('models/{}.h5'.format(model_type+"_divider"+str(divider)+"_dropout"+str(dropout)+"_epoch"+str(epoch)), monitor='val_loss',
                         save_best_only=True, save_weights_only=False,
                         mode='auto', save_freq='epoch', verbose=1)
    csv_logger = CSVLogger(csv_path, append=False)
    model.fit(tg, validation_data=vg,
              epochs=epoch, verbose=1,
              callbacks=[csv_logger, cp])

def main_divider():
    for i in parameters.DIVIDER:
        global src_root
        global divider
        src_root=parameters.DST_ROOT+"_divider"+str(i)
        divider=i
        train(epoch=15,dropout=0.6)
def main_dropout():
    for epoch in parameters.EPOCH:
        for dropout in parameters.DROPOUT:
            global src_root
            global divider
            divider=6
            src_root=parameters.DST_ROOT+"_divider"+str(divider)
            train(epoch=epoch,dropout=dropout)
if __name__ == '__main__':  
    for i in range(1,15):
        src_root=parameters.DST_ROOT+"_divider"+str(i)
        divider=i
        train()