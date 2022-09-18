import os
import subprocess
from dateutil import relativedelta
import datetime
from enum import Enum
from src.env import MONGO_URI,MONGO_PASSWORD, DATA_DIR

class MongoSourceInfo():
    """Mongo Source definition"""
    def __init__(self, identifier, collection, query, output, limit=0):
        self.identifier = identifier
        self.collection = collection
        self.query = query
        self.output = output
        self.limit = limit

class RecTypeEnum(Enum):
     MotionUnpacked = "io.microshare.motion.unpacked"
     OccupancyUnpacked = "io.microshare.occupancy.unpacked"
     EnvironmentUnpacked = "io.microshare.environment.unpacked"
     FeedbackUnpacked = "io.microshare.feedback.unpacked"
    
device_source=MongoSourceInfo("devices", "devices", "", "devices.json",100)
REC_TYPES=["io.microshare.motion.unpacked","io.microshare.feedback.unpacked"]
#REC_TYPES=[]

if __name__ == '__main__':
    print("========== Extract started ==========")
    sources = [device_source]
    start = datetime.date(2022, 7, 1)
    end = datetime.date(2022, 7, 2)
    BATCH_DAYS = 1
    
    for rec_type in REC_TYPES:
        for date in [start + relativedelta.relativedelta(days=x*BATCH_DAYS) for x in range(0, int((end - start).days/BATCH_DAYS)+1)]:
            start_date =  date.isoformat()
            end_date= (date + relativedelta.relativedelta(days=BATCH_DAYS)).isoformat()
            file_suffix = f"{rec_type}_{start_date.replace('-','')}" #+ "-" + (date + relativedelta.relativedelta(days=BATCH_DAYS-1)).isoformat().replace("-","")
            query = f'{{ "recType" : "{rec_type}", "createDate" : {{ "$gte" : {{ "$date": "{start_date}T00:00:00.000Z" }} }}, "createDate" : {{ "$lt" : {{ "$date": "{end_date}T00:00:00.000Z" }} }} }}'
            output=f"objs_{file_suffix}.json"
            sources.append(MongoSourceInfo(f"objs_{file_suffix}","objs", query, output))

    for source in sources:
        #cmd=f"mongoexport --uri {MONGO_URI} --password {MONGO_PASSWORD} --collection {source.collection} --out {source.output}"
        #print(cmd)
        output = os.path.join(DATA_DIR, source.output)
        args=["mongoexport","--uri",MONGO_URI,"--password",MONGO_PASSWORD,"--collection",source.collection, "--jsonArray", "--out",output]
        if source.limit > 0:
            args.append("--limit")
            args.append(str(source.limit))
        if source.query is not None:
            args.append("--query")
            args.append(source.query)
        print(f"Extracting {source.identifier} to {source.output}")
        #output = subprocess.check_output(args)
        print(args)
    print("========== Extract completed ==========")
   