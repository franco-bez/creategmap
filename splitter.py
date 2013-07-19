#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import configparser
import shutil

WORK_DIR = os.environ['HOME'] + "/map_build/"

def printinfo(msg):
  print("II: " + msg)

def printwarning(msg):
  print("WW: " + msg)

def printerror(msg):
  print("EE: " + msg)


config = configparser.ConfigParser()

"""
split raw-data

"""

def split():

  os.chdir(WORK_DIR)
  config.read('pygmap3.cfg')
  buildmap = config.get('runtime', 'buildmap')
  buildday = config.get('time_stamp', (buildmap))
  splitter_path = (WORK_DIR) + config.get('splitter', 'version') + "/splitter.jar "
  datei = open((WORK_DIR) + "tiles/" + (buildmap) + "_split.lck", "w")
  datei.close()

  java_opts = ("java -ea " + config.get('ramsize', 'ramsize') +
                  " -jar " + (splitter_path))

  logging = config.get('splitter', 'logging')
  if logging == "yes":

    log_dir = ((WORK_DIR) + "log/splitter/" + (buildday) + "/" + (buildmap))

    ExitCode = os.path.exists(log_dir)
    if ExitCode == True:
      path = (log_dir)
      for file in os.listdir(path):
        if os.path.isfile(os.path.join(path, file)):
          try:
            os.remove(os.path.join(path, file))
          except:
            print('Could not delete', file, 'in', path)

    elif ExitCode == False:
      os.makedirs(log_dir)

    log_opts = (" > " + (log_dir) + "/splitter.log ")

  else:
    log_opts = (" > /dev/null ")

  """
  splitter-options
  """

  splitter_opts = (" --geonames-file=" + (WORK_DIR) + "cities15000.zip " +
                   " --mapid=" + config.get('mapid', (buildmap)) + "0001 " +
                   " --output=o5m " +
                   " --keep-complete " +
                   " --write-kml=" + (buildmap) + ".kml "
                   " --max-nodes=" + config.get('splitter', 'maxnodes') +
                   " --overlap=0 ")

  areas_list = (" --split-file=" + (WORK_DIR) + "areas/" + (buildmap) + "_areas.list ")

  BUILD_O5M = ((WORK_DIR) + "o5m/" + (buildmap) + ".o5m")

  ExitCode = os.path.exists("areas/" + (buildmap) + "_areas.list")
  if ExitCode == True:
    os.chdir("tiles")
    os.system((java_opts) + (log_opts) + (splitter_opts) + (areas_list) + (BUILD_O5M))
  else:
    os.chdir("tiles")
    os.system((java_opts) + (log_opts) + (splitter_opts) + (BUILD_O5M))
    shutil.move("areas.list", (WORK_DIR) + "areas/" + (buildmap) + "_areas.list")

  os.chdir(WORK_DIR)

  ExitCode = os.path.exists("tiles/template.args")
  if ExitCode == True:
    datei = open("tiles/" + (buildmap) + "_split.ready", "w")
    datei.close()
  else:
    printerror("Splitter-Error!")
    quit()
  os.remove("tiles/" + (buildmap) + "_split.lck")



