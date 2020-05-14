#! /bin/bash

rm -r ../bin/server*;
pyinstaller --onefile server.spec;
cp dist/server ../bin/server;

rm -r build dist;

