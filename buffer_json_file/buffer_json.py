import os
import sys
import threading
# To not be necessary install the dependecy at the Operational System(requests and schedule do not come by default in python), that version was embbebed 
parent_dir = os.path.abspath(os.path.dirname(__file__))
vendor_dir = os.path.join(parent_dir, 'vendor')
sys.path.append(vendor_dir)
from multiprocessing import Process
from datetime import datetime
from datetime import timedelta
import schedule_
import time
import json
import requests_
import shutil
import time
import traceback
import filecmp
import http.server
import socketserver
import logging
from pyftpdlib.authorizers import DummyAuthorizer
from pyftpdlib.handlers import FTPHandler
from pyftpdlib.servers import FTPServer
try:
    # Python 2
    from future_builtins import filter
except ImportError:
    # Python 3
    pass
import os

## That service download the json file as configurated on the file files_to_be_download
## It was tested in the python version >= 3.0
## developed by @Claudio Resende<c.resende@rheagroup.com>
TIME_TO_NORMALIZE_LIST = 60
TIME_LOG_FILE = 1
FILE_TIME_FORMAT = "%Y-%m-%dT%H-%M-%S"
UTC_FIELD_FORMAT_TO = "%Y-%m-%dT%H:%M:%S.%f"

list_of_to_be_download_source = [];
list_of_data_set = []
last_file_ingested = ""
# That list store the json read in memory and time to time store in the file, and also time to time that list is refresh and removed the records that is expired
# Now it is in memory, but in the future if the system grow(the number of data_set for instance) can be used a python temp file structure it is a  bit heavier than memory(ram), but still works fine
list_of_json_ingested = {}
LOG_FILE_NAME = 'buffer_json.log'
LOG_DIRECTORY = os.getcwd() + '/logs/'
FULL_PATH_LOG = LOG_DIRECTORY + LOG_FILE_NAME
if not os.path.exists(LOG_DIRECTORY):
    os.makedirs(LOG_DIRECTORY)

class DataSet:
    def __init__(self, url, file, timer, active, time_file, save_in):
        self.url = url
        self.file = file
        self.timer = timer
        self.active = active
        self.time_file = time_file
        self.save_in = save_in
class Setup:
    def __init__(self, http_port, http_dir, http_enable, ftp_dir, ftp_port, ftp_enable, debug_enable):
        self.http_port = http_port
        self.http_dir = http_dir
        self.http_enable = http_enable
        self.ftp_dir = ftp_dir
        self.ftp_port = ftp_port
        self.ftp_enable = ftp_enable
        self.debug_enable = debug_enable

# load the configuration file
def load_configuration_file():

    with open("config.json", "r") as read_file:
        list_of_to_be_download_source.append(json.load(read_file))

# parser the raw json to an object DataSet and append to the list to be read after
def load_dataser_and_setup_object():
    for each in list_of_to_be_download_source[0] :
        if each["TYPE"].upper() == "DATA_SET" :
            data_set = DataSet(each["url"], each["file"], each["timer"], each["active"], each["time_file"], each["save_in"])
            list_of_data_set.append(data_set)
        if each["TYPE"].upper() == "SETUP" :
            global setup
            setup = Setup(each["http_port"], each["http_dir"], each["http_enable"], each["ftp_dir"], each["ftp_port"], each["ftp_enable"], each["debug_enable"])


def rename_file(old_name):
    try:
        logging.debug('RENAMING FILE %s', old_name)
        shutil.move(old_name, (old_name + ("_" + time.strftime(FILE_TIME_FORMAT))))
    except Exception as e:
            logging.error('ERRO RENAMING FILE %s', e)


## load the essentials list before start the process of importation
load_configuration_file()
load_dataser_and_setup_object()
if setup.debug_enable == 1 :
    logging.basicConfig(filename=FULL_PATH_LOG,level=logging.DEBUG,format='%(asctime)s %(message)s', datefmt='%m/%d/%Y %I:%M:%S %p')
    logging.warning('DEBUG MODE IS ACTIVATED')
else :
    logging.basicConfig(filename=FULL_PATH_LOG,level=logging.INFO,format='%(asctime)s %(message)s', datefmt='%m/%d/%Y %I:%M:%S %p')

schedule_.every(TIME_LOG_FILE).hour.do(rename_file,FULL_PATH_LOG)

logging.debug('LOADED CONFIGURATION %s',setup)
def start_http_server(http_port, http_dir):
    web_dir = os.path.join(os.path.dirname(http_dir), '')
    os.chdir(web_dir)

    Handler = http.server.SimpleHTTPRequestHandler
    httpd = socketserver.TCPServer(("", http_port), Handler)
    logging.info("SERVING AT PORT %s", http_port)
    httpd.serve_forever()

def start_ftp_server(ftp_port, ftp_dir):
    authorizer = DummyAuthorizer()
    authorizer.add_user("esa", "esaftp", ftp_dir, perm="elradfmw")
    authorizer.add_anonymous(ftp_dir, perm="elradfm")
    logging.info("SERVING AT PORT %s", ftp_port)
    handler = FTPHandler
    handler.authorizer = authorizer

    server = FTPServer(("0.0.0.0", ftp_port), handler)
    server.serve_forever()

# read the json file from  provider using the libary request and return the json data
def read_json_from_provider(url, file):
    data = ""
    logging.debug("STARTING FETCHING DATA OF: %s",file)
    try:
        response = requests_.get((url + file))
        data = json.loads(response.text)
    except Exception as e:
        logging.error('ERRO FETCHING DATA %s ... TRYING AGAIN', e)

    logging.debug("ADDING DATA OF %s, TO MEMORY",file)
    insert_json_object_to_memory_list(data, file)
    return data

def load_the_last_file(directory, file):
    logging.debug("RETRIEVING THE LAST FILE STORED IN DISC",file)
    data = ""
    if not os.path.exists(directory):
        os.makedirs(directory)
    with open((directory + file), "r") as read_file:
        data = json.load(read_file)
    return data

# save the json on disk with name defined at the configuration file and with parameter a with means it will update the file not generate another
def save_json_file(file_name, directory, data):
    if not os.path.exists(directory):
        os.makedirs(directory)
    with open((directory + file_name), "w") as write_file:
        json.dump(list_of_json_ingested.get(file_name), write_file)

#that function insert the list of record read from provider in the big list in the memory, aftterward that list will be store in the file
def insert_json_object_to_memory_list(list_data, file_name):
    for data in reversed(list_data) :
        if data not in list_of_json_ingested.get(file_name):
            list_of_json_ingested.get(file_name).insert(0,data)

# orchestration of the process to pull the date from provider
def fetch_json_from_provider(provider):
    response = read_json_from_provider(provider.url, provider.file)
    save_json_file(provider.file, provider.save_in, response)


# according with the configuration time_file remove of the list the records expired
def normalize_json_list(file_name, time_file):
    list_of_json_ingested[file_name] = list(filter(lambda x: (datetime.strptime(normalize_wrong_date(x["time_tag"]), UTC_FIELD_FORMAT_TO)) > (datetime.utcnow() - timedelta(seconds=time_file)), list_of_json_ingested.get(file_name)))

# some date come in the utc field without the value if milissecound(%f)
def normalize_wrong_date(date):
    new_date = date
    if len(date) == 19:
        new_date += ".000"
    return new_date


# Initialize a schedule receive a callable a timer and a list of arguments to use on the callable
def initialize_schedule(cal, timer, *args):
    try :
        schedule_.every(timer).seconds.do(cal,*args)
    except Exception as e:
        logging.error('ERROR WHEN WAS TRYING RUN SCHEDULE %s',e)


if __name__ == '__main__':
    logging.info('INITIALIZING BUFFER SERVICE')
    for provider in list_of_data_set:
        if provider is not None and provider.active == 1:
            try:
                logging.debug('ADDING FILE TO BE DOWNLOAD %s',provider.file)
                list_of_json_ingested[provider.file] = load_the_last_file(provider.save_in , provider.file)
            except Exception as e:
                logging.error('ERROR ADDING FILE %S EXCEPTION %s',provider.file,e)
                list_of_json_ingested[provider.file] = []


            threading.Thread(target=initialize_schedule, args=(fetch_json_from_provider, provider.timer, provider,)).start()
            threading.Thread(target=initialize_schedule, args=(normalize_json_list, TIME_TO_NORMALIZE_LIST, provider.file, provider.time_file,)).start()



# put http and ftp server(if it is the case) in a thread to be run in parallel with the rest of the system
if setup is not None:
    if setup.http_enable == 1 :
        threading.Thread(target=start_http_server, args=(setup.http_port, setup.http_dir,)).start()
    if setup.ftp_enable == 1:
        threading.Thread(target=start_ftp_server, args=(setup.ftp_port, setup.ftp_dir,)).start()

# keeps on running all time.
while True:
    schedule_.run_pending()
    time.sleep(1)
