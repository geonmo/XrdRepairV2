#!/bin/bash
pip3 uninstall pycurl
pip3 install --compile --global-option="--with-nss" pycurl

