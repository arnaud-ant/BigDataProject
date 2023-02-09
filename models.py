import keras
from keras.models import Model
from keras.layers import Dense, Dropout, Flatten, Conv2D, MaxPooling2D, LSTM,Reshape,LayerNormalization,TimeDistributed,MaxPooling1D,Bidirectional,concatenate
from keras.utils import to_categorical
from kapre.composed import get_melspectrogram_layer
from keras.regularizers import l2

def Conv1D_(N_CLASSES=6,SR=16000,DT=1.0):
    return 0
def Conv2D_(dropout,N_CLASSES=6,SR=16000,DT=1.0):
    input_shape = (int(SR*DT), 1)
    i = get_melspectrogram_layer(input_shape=input_shape,
                                 n_mels=128,
                                 pad_end=True,
                                 n_fft=512,
                                 win_length=400,
                                 hop_length=160,
                                 sample_rate=SR,
                                 return_decibel=True,
                                 input_data_format='channels_last',
                                 output_data_format='channels_last')
    x = LayerNormalization(axis=2, name='batch_norm')(i.output)
    x = Conv2D(8, kernel_size=(7,7), activation='tanh', padding='same', name='conv2d_tanh')(x)
    x = MaxPooling2D(pool_size=(2,2), padding='same', name='max_pool_2d_1')(x)
    x = Conv2D(16, kernel_size=(5,5), activation='relu', padding='same', name='conv2d_relu_1')(x)
    x = MaxPooling2D(pool_size=(2,2), padding='same', name='max_pool_2d_2')(x)
    x = Conv2D(16, kernel_size=(3,3), activation='relu', padding='same', name='conv2d_relu_2')(x)
    x = MaxPooling2D(pool_size=(2,2), padding='same', name='max_pool_2d_3')(x)
    x = Conv2D(32, kernel_size=(3,3), activation='relu', padding='same', name='conv2d_relu_3')(x)
    x = MaxPooling2D(pool_size=(2,2), padding='same', name='max_pool_2d_4')(x)
    x = Conv2D(32, kernel_size=(3,3), activation='relu', padding='same', name='conv2d_relu_4')(x)
    x = Flatten(name='flatten')(x)
    x = Dropout(rate=dropout, name='dropout')(x)
    x = Dense(64, activation='relu', activity_regularizer=l2(0.001), name='dense')(x)
    o = Dense(N_CLASSES, activation='softmax', name='softmax')(x)
    model = Model(inputs=i.input, outputs=o, name='2d_convolution')
    model.compile(optimizer='adam',
                  loss='categorical_crossentropy',
                  metrics=['accuracy'])
    return model

def LSTM_(dropout,N_CLASSES=6,SR=16000,DT=1.0):
    input_shape = (int(SR*DT), 1)
    i = get_melspectrogram_layer(input_shape=input_shape,
                                     n_mels=128,
                                     pad_end=True,
                                     n_fft=512,
                                     win_length=400,
                                     hop_length=160,
                                     sample_rate=SR,
                                     return_decibel=True,
                                     input_data_format='channels_last',
                                     output_data_format='channels_last',
                                     name='2d_convolution')
    x = LayerNormalization(axis=2, name='batch_norm')(i.output)
    x = TimeDistributed(Reshape((-1,)), name='reshape')(x)
    s = TimeDistributed(Dense(64, activation='tanh'),
                        name='td_dense_tanh')(x)
    x = Bidirectional(LSTM(32, return_sequences=True),
                             name='bidirectional_lstm')(s)
    x = concatenate([s, x], axis=2, name='skip_connection')
    x = Dense(64, activation='relu', name='dense_1_relu')(x)
    x = MaxPooling1D(name='max_pool_1d')(x)
    x = Dense(32, activation='relu', name='dense_2_relu')(x)
    x = Flatten(name='flatten')(x)
    x = Dropout(rate=dropout, name='dropout')(x)
    x = Dense(32, activation='relu',
                         activity_regularizer=l2(0.001),
                         name='dense_3_relu')(x)
    o = Dense(N_CLASSES, activation='softmax', name='softmax')(x)
    model = Model(inputs=i.input, outputs=o, name='long_short_term_memory')
    model.compile(optimizer='adam',
                  loss='categorical_crossentropy',
                  metrics=['accuracy'])

    return model
    