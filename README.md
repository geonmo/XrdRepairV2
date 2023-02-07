# geonmolib
## About curl compile,
The --with option when the curl program is installed is very important. --with-nss does not appear to read directory information about
/etc/grid-security, so you need to use a different curl binary, such as cmsenv, or add your certificate issuer and CERN Grid certificate to nss.

## Requirement
* C++14 Complier
