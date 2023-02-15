#!/bin/bash
python3 -m pip uninstall pycurl

## If use extra curl,
#export PYCURL_CURL_CONFIG=/usr/local/bin/curl-config
#export LD_LIBRARY_PATH=/usr/local/lib
#pip3 install pycurl




## NSS linked curl,
python3 -m pip install --compile --global-option="--with-nss" pycurl
