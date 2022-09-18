""" Upload all files to snowflake stage """
import glob
import os
from src.env import TARGET_DB_URL
from src.db import DBSession
from src.env import DATA_DIR

if __name__ == '__main__':
    print("========== Upload started ==========")
    # upload all files
    files = glob.glob(os.path.join(DATA_DIR,"*.json"))
    target_db = DBSession(TARGET_DB_URL)
    target_db.connect()
    for file_path in files:
        put_file_sql=f"put file://{file_path} @raw.load_stage OVERWRITE = TRUE;"
        target_db.execute_sql(put_file_sql)
    target_db.close()
    print("========== Upload completed ==========")
