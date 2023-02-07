# geonmolib
This library collection is intended to collect Python libraries needed to operate CMS T3\_KR\_KISTI. A library related to xrootd will be convened
mainly.

## geonmolib.datasetinfo
The library (executable) is used to import data set information into the Python program through CMS DAS queries. Because most code is processed using
the dbs3-client, it is written to be useful for processing multiple data sets.

The actual way to handle refer to the contents of xrdrepair.

## About curl compile, 
### pycurl.error: (35, 'Peer does not recognize and trust the CA that issued your certificate.')
The --with option when the curl program is installed is very important. 
Curl which is compiled "--with-nss" can not parse proxy certificate propely (/tmp/x509up\_uXXX).
So, you need to use a different curl binary, such as cmsenv, 
or remove proxy CA(voms-proxy-destroy) and userkey's passphase + set env "X509\_USER\_CERT" and "X509\_USER\_KEY".

## Requirement
* C++14 Complier
