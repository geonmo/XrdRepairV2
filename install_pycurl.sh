#!/bin/bash
pip3 uninstall pycurl
pip3 install --compile --install-option="--with-nss" pycurl
