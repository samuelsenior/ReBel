#! /bin/bash

rm -r ../bin/ReBel*;
pyinstaller --noconsole --onefile ReBel.spec;
cp dist/ReBel ../bin/ReBel;
rm -r build dist;

