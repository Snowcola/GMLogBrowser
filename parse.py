import sqlite3
from pathlib import Path
import re
from dateutil.parser import parse
import sqlalchemy as db
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, DateTime, Numeric, Boolean
from sqlalchemy.orm import sessionmaker, relationship, scoped_session
from sqlalchemy import ForeignKey, MetaData
from datetime import datetime
import pandas as pd
import time, os.path

Base = declarative_base()
meta = Base.metadata
engine = db.create_engine('sqlite:///logs.db')
connection = engine.connect()
Session = sessionmaker(bind=engine)
if __name__ != "__main__":
    Session = scoped_session(sessionmaker(bind=engine))
    Base.query = Session.query_property()
session = Session()


class HourlyRecord(Base):
    __tablename__ = 'hourly_records'
    id = Column(Integer, primary_key=True)
    item = Column(Integer)
    timestamp = Column(DateTime)
    total_fwd_corr_vol = Column(Integer)
    total_fwd_uncorr_vol = Column(Integer)
    avg_pressure = Column(Numeric)
    min_pressure = Column(Numeric)
    temperature = Column(Numeric)
    max_flowrate = Column(Numeric)
    max_flowrate_timestamp = Column(DateTime)
    ambient_temperature = Column(Numeric)
    log_id = Column(Integer, ForeignKey('logs.id'))
    log = relationship("Log", back_populates='hourly_records')

    corr_usage = Column(Numeric)
    uncorr_usage = Column(Numeric)
    min_pressure_timestamp = Column(DateTime)
    avg_pressure_gauge = Column(Numeric)
    min_pressure_gauge = Column(Numeric)

class DailyRecord(Base):
    __tablename__ = 'daily_records'
    id = Column(Integer, primary_key=True)
    item = Column(Integer)
    timestamp = Column(DateTime)
    total_fwd_corr_vol = Column(Integer)
    total_fwd_uncorr_vol = Column(Integer)
    max_flowrate = Column(Numeric)
    max_flowrate_timestamp = Column(DateTime)
    min_pressure = Column(Numeric)
    min_pressure_timestamp = Column(DateTime)
    max_pressure = Column(Numeric)
    avg_temperature = Column(Numeric)
    log_id = Column(Integer, ForeignKey('logs.id'))
    log = relationship("Log", back_populates='daily_records')

    #additional ufg fields
    avg_pressure = Column(Numeric)
    min_flowrate = Column(Numeric)
    corr_usage = Column(Numeric)
    uncorr_usage = Column(Numeric)
    max_hourly_vol = Column(Numeric)
    max_hourly_vol_timestamp = Column(DateTime)
    min_pressure_gauge = Column(Numeric)
    max_pressure_gauge = Column(Numeric)


class MonthlyRecord(Base):
    __tablename__ = 'monthly_records'
    id = Column(Integer, primary_key=True)
    item = Column(Integer)
    timestamp = Column(DateTime)
    total_fwd_corr_vol = Column(Integer)
    total_fwd_uncorr_vol = Column(Integer)
    min_pressure = Column(Numeric)
    avg_pressure = Column(Numeric)
    avg_temperature = Column(Numeric)
    avg_flowrate = Column(Numeric)
    max_hourly_vol = Column(Numeric)
    max_hourly_vol_timestamp = Column(DateTime)
    log_id = Column(Integer, ForeignKey('logs.id'))
    log = relationship("Log", back_populates='monthly_records')

    corr_usage = Column(Numeric)
    uncorr_usage = Column(Numeric)
    max_flowrate = Column(Numeric)
    max_flowrate_timestamp = Column(DateTime)
    min_flowrate = Column(Numeric)
    min_pressure_gauge = Column(Numeric)
    avg_pressure_gauge = Column(Numeric)

class Log(Base):
    __tablename__ = 'logs'

    id = Column(Integer, primary_key=True)
    instrument_id = Column(String, ForeignKey('instruments.id'))
    date_collected = Column('Date Collected', DateTime)
    instrument = relationship("Instrument", back_populates="logs")  
    hourly_records = relationship("HourlyRecord", order_by=HourlyRecord.id, back_populates='log')
    has_hourly = Column(Boolean, default=False)
    daily_records = relationship("DailyRecord", order_by=DailyRecord.id, back_populates='log')
    has_daily = Column(Boolean, default=False)
    monthly_records = relationship("MonthlyRecord", order_by=MonthlyRecord.id, back_populates='log')
    has_monthly = Column(Boolean, default=False)


class Instrument(Base):
    __tablename__ = 'instruments'

    id = Column(Integer, primary_key=True)
    instrument = Column(String, unique=True)
    logs = relationship("Log", order_by=Log.date_collected, back_populates='instrument')

    def __repr__(self):
        return f'<Instrument {self.instrument}>'


Base.metadata.create_all(engine)

def get_or_create(session, model, **kwargs):
    instance = session.query(model).filter_by(**kwargs).first()
    created = False
    if not instance:
        instance = model(**kwargs)
        session.add(instance)
        created = True

    return instance, created


def test_adding_records():
    inst = get_or_create(session, Instrument, instrument='A12345')
    print(inst.logs)
    current_log = inst.logs[0]
    record = HourlyRecord(log=current_log, total_fwd_corr_vol=12)
    #logg = Log(instrument=inst, date_collected=datetime(2018, 5, 26, 0, 0))
    session.add(record)
    session.commit()

def parse_timestamp(timestamp):
    date, hour = timestamp.split(' ')
    year, month, day = map(int, date.split('-'))
    return datetime(year, month, day, int(hour), 0,0)

    #"3237.A05867.19.6.5.HourlyLog.csv"

def parse_log_file_name(log_name):
    inst_pattern = r"(A\d{5})[. ](\d{2,4}[. ]\d{1,}[. ]\d{1,})"
    x = re.search(inst_pattern, log_name)
    if not x:
        return None, None, None

    instrument=x.group(1)
    date_collected=parse(x.group(2), yearfirst=True)
    
    log_type = 'unknown'
    types = ['hourly', 'daily', 'monthly']
    for t in types:
        if t in log_name.lower():
            log_type = t

    return instrument, date_collected, log_type

def txdr_name(columns):
    for col in columns:
        if 'Press' in col:
            return re.search(r'\[(.{1,})\]', col).group(1)

def parse_log_hourly_records(log_name):
    df = pd.read_csv(log_name, skiprows=2)
    tdxr = txdr_name(df.columns)
    avg_temperature = next(filter(lambda x: "PT 100 RTD" in x, df.columns), 'PT 100 RTD')
    column_map = {
        'Item #': 'item', 
        'time': 'timestamp',
        'Total Forward Corrected Volume(CF)': 'total_fwd_corr_vol',
        'Total Forward Uncorrected Volume(CF)':'total_fwd_uncorr_vol',
        f'Hourly Ave. Press-a Txdr [{tdxr}](Psia)': 'avg_pressure',
        f'Hourly Min. Press-a Txdr [{tdxr}](Psia)': 'min_pressure',
        avg_temperature: 'temperature', 
        'Hourly Max. Flow Rate(CF)': 'max_flowrate',
        'Hourly Max. Flow Rate TS.(time)': 'max_flowrate_timestamp', 
        'Ambient Temperature(Deg. F)': 'ambient_temperature',

        'Hourly Min. Press-a Txdr [08123] TS.(time)': 'min_pressure_timestamp',
        'Hourly Fwd. Corr. Vol.(CF)': 'corr_usage',
        'Hourly Fwd. Uncor. Vol.(CF)': 'uncorr_usage',
        f'Hourly Ave. Press-g Txdr [{tdxr}](Psi)': 'avg_pressure_gauge',
        f'Hourly Min. Press-g Txdr [{tdxr}](Psi)': 'min_pressure_gauge'

    }

    new_map = {item: column_map[item] for item in df.columns if item in column_map.keys()}

    column_map = new_map
    df.rename(columns=column_map, inplace=True)

    timestamps = list(filter(lambda x: 'timestamp' in x, df.columns))
    for item in timestamps:
        df[item] = pd.to_datetime(df[item])

    #parse this separately due to hour component
   # df['timestamp'] = df['timestamp'].apply(parse_timestamp)

    log_data = df.to_dict(orient='records') 

    #print(df.tail())
    return log_data


def parse_log_daily_records(log_name):
    df = pd.read_csv(log_name, skiprows=2)
    tdxr = txdr_name(df.columns)

    avg_temperature = next(filter(lambda x: "Ave. PT 100 RTD" in x, df.columns), 'Ave. PT 100 RTD')

    column_map = {
        'Item #': 'item', 
        'time': 'timestamp',
        'Total Forward Corrected Volume(CF)': 'total_fwd_corr_vol',
        'Total Forward Uncorrected Volume(CF)':'total_fwd_uncorr_vol',
        'Daily Max. Flow Rate(CF)': 'max_flowrate',
        'Daily Max. Flow Rate TS.(time)': 'max_flowrate_timestamp', 
        f'Daily Min. Press-a Txdr [{tdxr}](Psia)': 'min_pressure',
        f'Daily Min. Press-a Txdr [{tdxr}] TS.(time)': 'min_pressure_timestamp',
        f'Daily Max. Press-a Txdr [{tdxr}](Psia)': 'max_pressure',
        avg_temperature: 'avg_temperature',
        
        f'Daily Ave. Press-a Txdr [{tdxr}](Psia)': 'avg_pressure',
        'Daily Min. Flow Rate(CF)': 'min_flowrate',
        'Daily Fwd. Corr. Vol.(CF)': 'corr_usage',
        'Daily Fwd. Uncor. Vol.(CF)': 'uncorr_usage',
        'Daily Max. Hourly Vol.(CF)': 'max_hourly_vol',
        'Daily Max. Hourly Vol. TS.(time)': 'max_hourly_vol_timestamp',
        f'Daily Min. Press-g Txdr [{tdxr}](Psi)': 'min_pressure_gauge',
        f'Daily Min. Press-g Txdr [{tdxr}] TS.(time)': 'min_pressure_timestamp',
        f'Daily Max. Press-g Txdr [{tdxr}](Psi)': 'max_pressure_gauge',
        f'Daily Max. Press-g Txdr [{tdxr}] TS.(time)': 'max_pressure_timestamp',
    }

    new_map = {item: column_map[item] for item in df.columns if item in column_map.keys()}

    column_map = new_map
    df.rename(columns=column_map, inplace=True)

    timestamps = list(filter(lambda x: 'timestamp' in x, df.columns))
    for item in timestamps:
        df[item] = pd.to_datetime(df[item])

    log_data = df.to_dict(orient='records') 

    #print(df.tail())
    return log_data

def parse_log_monthly_records(log_name):
    df = pd.read_csv(log_name, skiprows=2)
    tdxr = txdr_name(df.columns)
    avg_temperature = next(filter(lambda x: "PT 100 RTD" in x, df.columns), 'PT 100 RTD')
    print(tdxr)
    column_map = {
        'Item #': 'item', 
        'time': 'timestamp',
        'Total Forward Corrected Volume(CF)': 'total_fwd_corr_vol',
        'Total Forward Uncorrected Volume(CF)':'total_fwd_uncorr_vol',
        f'Monthly Min. Press-a Txdr [{tdxr}](Psia)': 'min_pressure',
        f'Monthly Ave. Press-a Txdr [{tdxr}](Psia)': 'avg_pressure',
        avg_temperature: 'avg_temperature',
        'Monthly Ave. Flow Rate(CF)': 'avg_flowrate',
        'Monthly Max. Hourly Vol.(CF)': 'max_hourly_vol', 
        'Monthly Max. Hourly Vol. TS.(time)': 'max_hourly_vol_timestamp', 

        'Monthly Fwd. Corr. Vol.(CF)': 'corr_usage',
        'Monthly Fwd. Uncor. Vol.(CF)': 'uncorr_usage',
        'Monthly Max. Flow Rate(CF)': 'max_flowrate',
        'Monthly Max. Flow Rate TS.(time)': 'max_flowrate_timestamp',
        'Monthly Min. Flow Rate(CF)':'min_flowrate',
        f'Monthly Min. Press-g Txdr [{tdxr}](Psi)': 'min_pressure_gauge',
        f'Monthly Ave. Press-g Txdr [{tdxr}](Psi)': 'avg_pressure_gauge',
    }

    new_map = {item: column_map[item] for item in df.columns if item in column_map.keys()}

    column_map = new_map
    df.rename(columns=column_map, inplace=True)

    timestamps = list(filter(lambda x: 'timestamp' in x, df.columns))
    for item in timestamps:
        df[item] = pd.to_datetime(df[item])
    '''
    df['timestamp'] = pd.to_datetime(df['timestamp'])
    df['max_hourly_vol_timestamp'] = pd.to_datetime(df['max_hourly_vol_timestamp'])
    '''
    log_data = df.to_dict(orient='records') 
    return log_data

def get_log_type(file_name):
        types = ['hourly', 'daily', 'monthly']
        for t in types:
            if t in file_name.lower():
                return t

def commit_daily_data(session, log, instrument, date, file_name):
    if not log.has_daily:
        log_data = parse_log_daily_records(file_name)

        for row in log_data:
            record = DailyRecord(log=log, **row)
            session.add(record)
        log.has_daily = True
        session.commit()

        print(f'SUCCESS :: Daily Log for {instrument} on {date} imported successfully')
    else: 
        print(f'FAILED :: Daily Log for {instrument} on {date} already exists.')

def commit_monthly_data(session, log, instrument, date, file_name):
    if not log.has_monthly:
        log_data = parse_log_monthly_records(file_name)

        for row in log_data:
            record = MonthlyRecord(log=log, **row)
            session.add(record)
        log.has_monthly = True
        session.commit()
        print(f'SUCCESS :: Monthly Log for {instrument} on {date} imported successfully')
    else: 
        print(f'FAILED :: Monthly Log for {instrument} on {date} already exists.')

def commit_hourly_data(session, log, instrument, date, file_name):
    if not log.has_hourly:
        log_data = parse_log_hourly_records(file_name)

        for row in log_data:
            record = HourlyRecord(log=log, **row)
            session.add(record)

        log.has_hourly = True
        session.commit()

        print(f'SUCCESS :: Hourly Log for {instrument} on {date} imported successfully')
    else: 
        print(f'FAILED :: Hourly Log for {instrument} on {date} already exists.')

def ingest_log(file_name):
    instrument, date, log_type = parse_log_file_name(file_name)
    if not instrument:
        return 
        
    equipment, eqip_created = get_or_create(session, Instrument, instrument=instrument)
    log, log_created = get_or_create(session, Log, instrument=equipment, date_collected=date)

    log_types = {
        'hourly': commit_hourly_data,
        'daily':commit_daily_data,
        'monthly':commit_monthly_data
        }
    x = log_types[log_type](session, log, instrument, date, file_name)
    # TODO add daily and monthly log ingestions

def find_log_csv_files(location='.'):
    

    x = list(Path(location).glob('*.csv'))
    logs = []
    for f in x:
        x = re.search(inst_pattern, str(f))
        instrument=x.group(1)
        date_collected=parse(x.group(2), yearfirst=True)
        logs.append((instrument, date_collected))

    return logs

if __name__ == "__main__":
    log_files = map(str, list(Path("testing/").glob('*.csv')))

    #file_name = str(Path("testing\\3237.A05866.19.6.5.MonthlyLog.csv"))
    try:
        errors = Path('testing/errors').mkdir()
    except:
        print('errors folder already exists')
    error_list = []
    for fname in log_files:
        #print(f'starting {fname}')
        print(fname)
        ingest_log(fname)
        try:
            pass
        except Exception as e:
            error_list.append([fname, e])
            floc = Path(fname)
            floc.replace(Path('testing/errors')/floc.name)
    date = datetime.now().strftime("%Y-%m-%d")
    errorlog = pd.DataFrame.from_records(error_list).to_csv(f'testing/errors/error-log_{date}.csv')
