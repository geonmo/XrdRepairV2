# geonmolib
This library collection is intended to collect Python libraries needed to operate CMS T3\_KR\_KISTI. A library related to xrootd will be convened
mainly.

## geonmolib.datasetinfo
The library (executable) is used to import data set information into the Python program through CMS DAS queries. Because most code is processed using
the dbs3-client, it is written to be useful for processing multiple data sets.

The actual way to handle refer to the contents of xrdrepair.

## About curl compile,
The --with option when the curl program is installed is very important. --with-nss does not appear to read directory information about
/etc/grid-security, so you need to use a different curl binary, such as cmsenv, or add your certificate issuer and CERN Grid certificate to nss.

## Requirement
* C++14 Complier
