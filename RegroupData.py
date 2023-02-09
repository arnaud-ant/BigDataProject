import numpy as np 
import pandas as pd
import parameters
for divider in parameters.DIVIDER:

    file_name="./logs/predict_log/predictionsdivider6_dropout0.5_epoch50.csv"
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
        print("Precision ",classe,":",(total-inacurate_total)/total,"%")

    print("Precision:",(total-inacurate_total)/total,"%")
    print("")
    print("")