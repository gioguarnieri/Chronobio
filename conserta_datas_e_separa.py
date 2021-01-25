# -*- coding: utf-8 -*-
"""
Created on Fri Aug 14 13:42:55 2020

@author: gio-x
"""

import pandas as pd
import datetime as dt
import matplotlib.pyplot as plt
import os
import gc

def find1970(df):
    x = 0
    for i in df["DATE/TIME"]:
        x += 1
        if "1970" in i:
            return x-1
    return 0


def graph(df):
    start_date = pd.to_datetime(df["DATE/TIME"][0].date())
    day_delta = dt.timedelta(days=1)
    last_day = pd.to_datetime(df["DATE/TIME"][len(df)-1].date()) + day_delta
    kk = (last_day - start_date).days
    # print(kk)
    plt.figure(figsize=(20, kk*8))
    j = 1
    column = "PIMn"
    while(start_date != last_day):
        resol = 1
        end_date = start_date+day_delta
        mask = (df['DATE/TIME'] > start_date) & (df['DATE/TIME'] <= end_date)
        df2 = df.loc[mask]
        df2 = df2.reset_index()
        # lcol = (df2.groupby(df2.index//resol).mean()[column]).tolist()
        mask = (df2.index % resol == 0)
        ldate = df2.loc[mask]['DATE/TIME'].tolist()
        lhour = [i.strftime("%H:%M") for i in ldate]
        ax1 = plt.subplot(kk, 1, j)
        ax1.plot(lhour, df2["PIMn"])
        plt.xticks(rotation=45)
        plt.grid()
        print(j)
        # ax.set_ylabel(column)
        # ax.set_xlabel("Hour")
        ax1.set_title("Date: {} Column: {}\n Resolution: {}min"\
                       .format(start_date.date(), column, resol))
        ax1.set_xticks(ax1.get_xticks()[::60//resol])
        ax2 = ax1.twinx()
        ax2.plot(lhour, df2["TEMPERATURE"])
        start_date = end_date
        j += 1
    plt.savefig(subject+".png")
    del df2
    plt.show()
    plt.close()
    gc.collect()

formato = "%d/%m/%Y %H:%M:%S"
directory = r'C:\Users\gio-x\Documents\Python Scripts\Pandas\Arrumando dados\Dados'
folder = "Arrumados"

try:
    os.mkdir(folder)
    os.mkdir("Before")
    os.mkdir("After")
except:
    print("Já existente")

# files = ['S01', 'S02', 'S03', 'S04', 'S05', 'S06', 'S07', 'S09', 'S10', 'S13',
#          'S14', 'S15', 'S16', 'S17', 'S18', 'S19', 'S20', 'S21', 'S24', 'S25',
#          'S26', 'S27', 'S28', 'S29', 'S30', 'S31', 'S32', 'S33', 'S34', 'S39',
#          'S42', 'S44', 'S47', 'S48', 'S54', 'S56', 'S57', 'S58', 'S60', 'S66']

files2 = ['S03', 'S04', 'S06', 'S07', 'S08', 'S09', 'S10', 'S11', 'S12', 'S13',
          'S16', 'S17', 'S18', 'S19', 'S21', 'S23', 'S24', 'S25', 'S26', 'S27',
          'S28', 'S34', 'S35', 'S36', 'S38', 'S39', 'S40', 'S41', 'S42', 'S43',
          'S44', 'S45', 'S48', 'S49', 'S52', 'S53', 'S54', 'S56', 'S57', 'S58',
          'S59', 'S60', 'S61', 'S62', 'S64', 'S65', 'S66', 'S68', 'S71', 'S72',
          'S73', 'S74', 'S75']


dates = ['20/06/2020','21/06/2020', '22/06/2020', '20/06/2020', '22/06/2020',
         '20/06/2020', '20/06/2020', '21/06/2020', '22/06/2020', '21/06/2020',
         '22/06/2020', '22/06/2020', '21/06/2020', '21/06/2020', '20/06/2020',
         '20/06/2020', '21/06/2020', '20/06/2020', '30/06/2020', '01/07/2020',
         '01/07/2020', '08/07/2020', '08/07/2020', '10/07/2020', '28/07/2020',
         '29/07/2020', '17/08/2020', '29/07/2020', '28/07/2020', '28/07/2020',
         '28/07/2020', '14/08/2020', '17/08/2020', '18/08/2020',
         '17/08/2020', '31/08/2020', '31/08/2020', '30/08/2020', '31/08/2020',
         '31/08/2020', '01/09/2020', '31/08/2020', '31/08/2020', '02/09/2020',
         '31/08/2020', '31/08/2020', '31/08/2020', '08/09/2020', '08/09/2020',
         '08/09/2020', '08/09/2020', '18/09/2020', '5/10/2020']

cont = 0
for entry in os.scandir(directory):
    os.chdir(directory)
    if (entry.path.endswith(".txt") and entry.is_file()):
        subject = entry.path[69:72]
        # if subject in files:
        df = pd.read_csv(entry.path, sep=";", skiprows=25)
        print(subject)
        os.chdir(os.path.join(directory, folder))
        x = find1970(df)
        if x != 0:
            start_date = (pd.to_datetime(df["DATE/TIME"][x-1], dayfirst=True))
            min_delta = dt.timedelta(minutes=1)
            time = start_date + min_delta
            for i in range(x, len(df)):
                df["DATE/TIME"][i] = time.strftime(formato)
                time += min_delta
        df["DATE/TIME"] = pd.to_datetime(df["DATE/TIME"], dayfirst=True)
        df['weekday'] = df['DATE/TIME'].apply(lambda x: x.weekday())
        # graph(df)
        df.plot(x="DATE/TIME", y="PIMn", figsize=(15,10), grid=True, title=subject)
        plt.savefig(subject + "_" + str(cont) + ".png")
        plt.show()
        df = df.set_index("DATE/TIME")
        df.to_csv(entry.path[69:], sep=';', date_format=formato)
        if subject in files2:
            split_date = pd.to_datetime(dates[cont], dayfirst=True)
            df_training = df.loc[df['DATE/TIME'] <= split_date]
            df_test = df.loc[df['DATE/TIME'] > split_date]
            # df_training.plot(x="DATE/TIME", y="PIMn", figsize=(15,10), grid=True, title=subject, backend = "matplotlib")
            # df_test.plot(x="DATE/TIME", y="PIMn", figsize=(15,10), grid=True, title=subject, backend = "matplotlib")
            plt.figure(figsize = (15,10))
            plt.grid()
            plt.title(subject)
            plt.plot(df_training["DATE/TIME"], df_training["PIMn"], label = "PIMn before")
            plt.plot(df_test["DATE/TIME"], df_test["PIMn"], c = "firebrick", label = "PIMn after")
            plt.legend()
            plt.savefig(subject+"_divided"+ str(cont)+".png")
            df_training = df_training.set_index("DATE/TIME")
            df_training.to_csv("before_"+entry.path[69:], sep=';', date_format=formato)
            df_test = df_test.set_index("DATE/TIME")
            df_test.to_csv("after_" + entry.path[69:], sep=';', date_format=formato)
            del df_test
            del df_training
        cont+=1
        df = df.set_index("DATE/TIME")
        df.to_csv(entry.path[69:], sep=';', date_format=formato)
        del df
        gc.collect()