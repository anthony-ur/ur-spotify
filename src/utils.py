"""
Utils module
~~~~~~~~~~~~~~~~~~~~~

Utilities and commonly used functions
"""

import os
import datetime
import shutil
import json
import logging
import re

logger = logging.getLogger('pipeline')

def get_timestamp():
    """get timestamp"""
    return datetime.datetime.now().strftime("%Y%m%d%H%M%S")

def get_epoch_s_from_date(year, month, day):
    """get epoch from date"""
    return round(datetime.datetime(year,month,day,0,0).timestamp())

def get_epoch_ms_from_date(year, month, day):
    """get epoch in milliseconds from date"""
    return get_epoch_s_from_date(year, month, day)*1000

def get_seconds_from_interval(days, hours, minutes, seconds):
    """get seconds from interval"""
    return days*24*60*60 + hours*60*60 + minutes*60 + seconds

def now():
    """get now"""
    return datetime.datetime.now()

def delete_file(path):
    """delete file if exists"""
    if os.path.exists(path):
        os.remove(path)

def read_file(path):
    """read file content"""
    content = None
    with open(path, 'r') as file:
        content = file.read()
    return content

def get_file_size(path):
    """get file size"""
    if os.path.exists(path):
        return os.stat(path).st_size

def write_file(path, content, write="w"):
    """write content to file"""
    with open(path, write) as file:
        file.write(content)
    return os.path.exists(path)

def read_file_json(path):
    """read file content as json"""
    with open(path, 'r') as file:
        data = json.load(file)
    return data

def save_to_file_json(data,path):
    """write content as json to a file"""
    with open(path, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=4)

def make_dir(directory, clear=False):
    """make a new directory , clear(delete all inner files) if specified"""
    if os.path.exists(directory) and clear:
        remove_dir(directory)
    if not os.path.exists(directory):
        os.makedirs(directory,exist_ok=True)

def remove_dir(directory):
    """remove a directory"""
    # Handle errors while calling os.remove()
    try:
        if os.path.exists(directory):
            #os.remove(directory)
            shutil.rmtree(directory)
            logger.info("Deleted %s",directory)
    except:
        logger.info("Could not delete %s directory", directory)

def get_calendar_dir_from_date(base_dir, iso_dt, strf_pattern_list):
    """ Get nested directory path based on input formatting pattern list """
    date = datetime.date.fromisoformat(iso_dt)
    joins = [date.strftime(strf) for strf in strf_pattern_list]
    return os.path.join(base_dir, *joins)

def camel_to_snake(text):
    pattern = re.compile(r'(?<!^)(?=[A-Z])')
    return pattern.sub('_', text).lower()

def print_ts(message='Current time'):
    print("{0} - {1}".format(now().strftime("%H:%M:%S"), message))

def remove_dict_null_values(data):
    return { key: value for key, value in data.items() if value is not None } 
 