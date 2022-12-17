from pymongo import MongoClient
import pandas as pd
import os

# Carregando dados do arquivo csv
df = pd.read_csv("dados.csv",low_memory=False)

# Selecionando apenas a data, hora e consumo de cada ambiente
df1 = df[['Date','Time','Sub_metering_1', 'Sub_metering_2', 'Sub_metering_3']]

# Conectando com o Mongo DB
mongo_client = MongoClient(os.environ.get("DB_STRING"))

# Criando banco de dados 'energy'
db = mongo_client["consumo"]
# Criando coleção 'medidas'
colecao = db["medidas"]

# Inserindo dados
db.medidas.insert_many(df1.to_dict('records'))
