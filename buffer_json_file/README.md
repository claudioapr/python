Some 3d party datasources provides json files that is updated from time to time and after a period it is deleted, so for avoiding losing data from those datasource and do not overhead 
the internal app with several calls it stores the file in a buffer so you can fetch it anytime you want

To run the service python 3 or greater should be installed.
The service has a configuration file which is a json file where you must setup the configuration of the data_set to download and the setup in case you want
an FTP or HTTP server running to make available the files.
you can insert many json files to be downloaded using http or https in the file  file_to_be_download.json just make to sure to set the TYPE to data_set


after change according to with your need the file file_to_be_download.json
within of the directory of the source code, you should run the command, python3 buffer_json.py & or python buffer_json.py & (it depends how is setup your python environment) 

