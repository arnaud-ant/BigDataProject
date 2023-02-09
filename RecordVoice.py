import pyaudio
import wave
import numpy as np
import os
import parameters
labels=parameters.WORD_LIST
# Demandez à l'utilisateur ce qu'il souhaite dire
for u in range(0,20):
    for index_boucle in range(0,6):
        print("Que souhaitez-vous dire ?")
        index=1
        for label in labels:
            print(index," pour ",label)
            index=index+1
        print(labels[index_boucle-1])
        label_index = index_boucle#input()

        label=""
        flag=0
        try:
            label=labels[int(label_index)-1]
            flag=1
        except:
            print("Le numéro donner ne correspont a aucun label")
            flag=0

        # Créez les dossiers s'ils n'existent pas
        if not os.path.exists("./enregistrements/"):
            os.makedirs("./enregistrements/")
        for name in labels:
            if not os.path.exists("./enregistrements/"+name):
                os.makedirs("./enregistrements/"+name)
                
        if flag==1:
            # Récupérez tous les fichiers pour ajouter le nouveau
            file_path="./enregistrements/"+label
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
