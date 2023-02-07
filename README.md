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
* It is similar to https://github.com/benoitc/gunicorn/issues/1934.


```bash
* NSS: client certificate from file
*       subject: CN=541999646,CN=Geonmo Ryu,CN=697493,CN=geonmo,OU=Users,OU=Organic Units,DC=cern,DC=ch
*       start date: Feb 07 06:31:34 2023 GMT
*       expire date: Feb 07 18:36:34 2023 GMT
*       common name: 541999646
*       issuer: CN=Geonmo Ryu,CN=697493,CN=geonmo,OU=Users,OU=Organic Units,DC=cern,DC=ch
* NSS error -12195 (SSL_ERROR_UNKNOWN_CA_ALERT)
```
  
## Requirement
* C++14 Complier
