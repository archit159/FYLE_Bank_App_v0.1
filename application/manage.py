from application import application, Config, models
from sqlalchemy import create_engine
from flask_sqlalchemy import SQLAlchemy
from flask import jsonify
import pandas as pd, codecs, json, flask

engine = create_engine(application.config['SQLALCHEMY_DATABASE_URI'])
db = SQLAlchemy(application)

def init_db():
    with codecs.open('./Inputs/bank_branches.csv', 'r', encoding='utf-8', errors='ignore') as infile, \
                codecs.open('./Inputs/bank_branches_ascii.csv', 'w', encoding='ASCII', errors='ignore') as outfile:
            for line in infile.readlines():
                for word in line.split()[:-1]:
                    outfile.write(word + " ")
                outfile.write(line.split()[-1])
                outfile.write("\n")
    df = pd.read_csv('./Inputs/bank_branches_ascii.csv',low_memory=False)
    try:
        df.to_sql(con=engine, name='bank_details', if_exists='replace', index=False, chunksize=2000)
        print('Table initialized...')
        return True
    except Exception as e:
        print('Exception in initializing table: ',e)
        return False

def _find_from_ifsc(ifsc=None,limit=None,offset=None):
    if not ifsc:
        print("IFSC code not provided...")
        return False
    else:
        offset = 0 if offset is None else offset
        if limit is None:
            df = pd.read_sql("select * from public.bank_details where upper(ifsc) like '%%{0}%%' offset {1}".format(ifsc.upper(),offset),con=engine)
        else:
            df = pd.read_sql("select * from public.bank_details where upper(ifsc) like '%%{0}%%' limit {1} offset {2}".format(ifsc.upper(),limit,offset),con=engine)
        if df.empty:
            return 'IFSC Code not found. Please check again...'
        return application.response_class(json.dumps(json.loads(df.to_json(orient='index')), indent=2), mimetype="application/json")

def _find_from_name(name=None,city=None,limit=None,offset=None):
    if not name or not city:
        print("Bank Name and/or City not provided...")
        return False
    else:
        offset = 0 if offset is None else offset
        if limit is None:
            df = pd.read_sql("select * from public.bank_details where upper(bank_name) like '%%{0}%%' and city like '%%{1}%%' offset {2}".format(name.upper(),city.upper(),offset),con=engine)
        else:
            df = pd.read_sql("select * from public.bank_details where upper(bank_name) like '%%{0}%%' and city like '%%{1}%%' limit {2} offset {3}".format(name.upper(),city.upper(),limit,offset),con=engine)
        print(df)
        if df.empty:
            return 'No Records found. Please check Bank Name and/or City again...'
        return application.response_class(json.dumps(json.loads(df.to_json(orient='index')), indent=2), mimetype="application/json")
