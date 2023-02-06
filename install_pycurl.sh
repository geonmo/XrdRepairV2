#!/bin/bash
pip3 uninstall pycurl
pip3 install --compile --global-option="--with-nss" pycurl



sudo wget https://cafiles.cern.ch/cafiles/certificates/CERN%20Grid%20Certification%20Authority.crt -O /etc/pki/ca-trust/source/anchors/cern-grid-ca.crt
sudo update-ca-trust force-enable
sudo update-ca-trust extract

