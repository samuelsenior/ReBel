#! /bin/bash

rm -r ../bin/server*;
pyinstaller --onefile server.spec;
cp -r dist/server ../bin/server;

rm -r build dist;
