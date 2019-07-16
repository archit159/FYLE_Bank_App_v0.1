from application import application, Config
from sqlalchemy import create_engine
import pandas as pd, codecs

engine = create_engine(application.config['SQLALCHEMY_DATABASE_URI'])

def init_db():
    with codecs.open('./Inputs/bank_branches.csv', 'r', encoding='utf-8', errors='ignore') as infile, \
                codecs.open('./Inputs/bank_branches_ascii.csv', 'w', encoding='ASCII', errors='ignore') as outfile:
            for line in infile.readlines():
                for word in line.split()[:-1]:
                    outfile.write(word + " ")
                outfile.write(line.split()[-1])
                outfile.write("\n")
    df = pd.read_csv('./Inputs/bank_branches_ascii.csv',low_memory=False)
    print(df)
    try:
        df.to_sql(con=engine, name='bank_details', if_exists='replace', index=False, chunksize=2000)
        print('Table initialized...')
        return True
    except Exception as e:
        print('Exception in initializing table: ',e)
        return False
