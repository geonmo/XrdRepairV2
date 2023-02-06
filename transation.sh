#!/bin/bash

if [ ! -e messages.po ]; then
    xgettext --from-code=utf-8 -d messages geonmolib/*.py
fi
if [ ! -e locale/ko_KR/LC_MESSAGES ]; then
    mkdir -p locale/ko_KR/LC_MESSAGES
fi
cp messages.po locale/ko_KR/LC_MESSAGES
cd locale/ko_KR/LC_MESSAGES
msgfmt messages.po -o messages.mo
cd -
