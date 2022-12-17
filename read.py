from pymongo import MongoClient
import numpy as np
import pandas as pd
import os

mongo_client = MongoClient(os.environ.get("DB_STRING"))

db = mongo_client.consumo
collection = db.medidas
df1 = pd.DataFrame(list(collection.find()))

df1['DateTime'] = df1['Date'] + ' ' + df1['Time'] # combinando data e hora em uma unica coluna
df1['DateTime'] = pd.to_datetime(df1.DateTime,format='%d/%m/%Y %H:%M:%S' ) # convertendo p/ formato datetime

# Removendo linhas com '?' no lugar do consumo
linhas_erradas = df1[(df1['Sub_metering_1'] == '?') | (df1['Sub_metering_2'] == '?')| (df1['Sub_metering_3'] == '?')].index
df2 = df1.drop(linhas_erradas)

# convertendo as colunas restantes para formato numerico
df2[['Sub_metering_1','Sub_metering_2','Sub_metering_3']] = df2[['Sub_metering_1','Sub_metering_2','Sub_metering_3']].apply(pd.to_numeric)
# gerando vetores para armazenar as medias
media_total = np.ndarray(shape=(24,),dtype=float)
sub1 = np.ndarray(shape=(24,),dtype=float)
sub2 = np.ndarray(shape=(24,),dtype=float)
sub3 = np.ndarray(shape=(24,),dtype=float)

# Calculando as medias de consumo para cada hora
for h in range(24):
    print('Hora:', h)
    hora = str(h)
    df2.index = pd.to_datetime(df2['DateTime'])
    df3=df2.between_time(hora+':00:00',hora+':59:59')

    sub1[h] = df3['Sub_metering_1'].mean()
    sub2[h] = df3['Sub_metering_2'].mean()
    sub3[h] = df3['Sub_metering_3'].mean()

    print('Sub meter 1:', sub1[h])
    print('Sub meter 2:', sub2[h])
    print('Sub meter 3:', sub3[h])
    print(' ')
