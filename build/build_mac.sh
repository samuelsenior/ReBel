#! /bin/bash

rm -r ../bin/*
pyinstaller --noconsole --onefile --icon=../img/ReBel_Icon.ico ReBel.spec;
cp -r dist/ReBel ../bin/ReBel&
cp -r dist/ReBel.app ../bin/ReBel.app;
rm -r build dist
