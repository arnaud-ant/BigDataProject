# IMPORT
import os
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import parameters

def main():
    """
    # Fonction main
    """
    directory = '.\\logs\\train_log\\' 
    pathSaveGraph = '.\\graph'
    index = 0
    change = 0
    nb_file = len([entry for entry in os.listdir(directory) if os.path.isfile(os.path.join(directory, entry))])
    figure, axis = plt.subplots(nb_file, 2)
    plt.subplots_adjust(left=0, bottom=0, right=1, top=1, wspace=0, hspace=0)

    #Definition des chemins d'acces a nos fichiers log
    for filename in os.listdir(directory):
        f = os.path.join(directory, filename)
        print(f)
        # checking if it is a file
        if os.path.isfile(f):
            data = pd.read_csv(f)
            axis[index, 0].plot(data['accuracy'])
            axis[index, 0].plot(data['val_accuracy'])
            title=""
            for name in filename.split("history.csv")[0].split("_")[1:]:
                if title!="":
                    title = title+"_"+name 
            axis[index, 0].set_title("Accuracy" + title)
            
            axis[index, 1].plot(data['loss'])
            axis[index, 1].plot(data['val_loss'])
            title=""
            for name in filename.split("history.csv")[0].split("_")[1:]:
                if title!="":
                    title = title+"_"+name 
            axis[index, 1].set_title("Loss" + title)
        
            index+=1
    
    plt.savefig(pathSaveGraph +'\\TRAIN_VAL_loss_' + filename.split("history.csv")[0])
    #plt.show()


    fig, ax = plt.subplots()
    width = 0.8
    index=0
    for divider in parameters.DIVIDER:
        predict_accuracy=[]
        file_name="./logs/predict_log/predictionsdivider"+str(divider)+".csv"
        print(file_name)
        df=pd.read_csv(file_name, header=1)
        df.drop(df.columns[[0]], axis=1, inplace=True)
        inacurate_total=0
        total=0
        for classe in df['Actual class'].drop_duplicates():
            inacurate_class=0
            total_class=0
            for predict in df['Prediction'].drop_duplicates():
                number=df.loc[((df["Actual class"]==classe) & (df["Prediction"]==predict))].shape[0]
                stringprint=str(classe) +":"+str(predict)+" "+str(number)
                print(stringprint)
                if(predict!=classe):
                    inacurate_total+=number
                    inacurate_class+=number
                total+=number
                total_class+=number   
            predict_accuracy.append((total-inacurate_total)/total)
            print("Precision ",classe,":",(total-inacurate_total)/total,"%")
        
        labels=df['Actual class'].drop_duplicates()
        x = np.arange(len(labels))
        rect1 = ax.bar(x+index*width/7-width/2,predict_accuracy,width/7, label=str(divider))
        index+=1

    ax.set_title('Predict')
    ax.set_xticks(x, labels)
    ax.set_ylim([0.85, 0.95])
    ax.legend()
    fig.tight_layout()
    plt.show()



if __name__ == "__main__":
    """
    # MAIN
    """
    main()