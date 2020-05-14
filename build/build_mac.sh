#! /bin/bash

rm -r ../bin/ReBel*;
pyinstaller --noconsole --onefile --icon=../img/ReBel_Icon.ico ReBel.spec;
cp -r dist/ReBel ../bin/ReBel&
cp -r dist/ReBel.app ../bin/ReBel.app;

mkdir ../bin/ReBel.app/Contents/audio&
mkdir ../bin/ReBel.app/Contents/config&
mkdir ../bin/ReBel.app/Contents/fonts&
mkdir ../bin/ReBel.app/Contents/img&
mkdir ../bin/ReBel.app/Contents/log;

cp ../audio/handbell.wav ../bin/ReBel.app/Contents/audio/handbell.wav&
cp ../config/config.txt ../bin/ReBel.app/Contents/config/config.txt&
cp -r ../fonts/* ../bin/ReBel.app/Contents/fonts/&
cp ../img/handbell.png ../bin/ReBel.app/Contents/img/handbell.png&
cp ../img/logo.png ../bin/ReBel.app/Contents/img/logo.png&
cp ../img/ReBel_Icon.png ../bin/ReBel.app/Contents/img/ReBel_Icon.png&
cp ../LICENSE ../bin/ReBel.app/Contents/LICENSE&
cp ../README.md ../bin/ReBel.app/Contents/README.md;

rm -r build dist;
