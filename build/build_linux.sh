#! /bin/bash

rm -r ../bin/*;
pyinstaller --noconsole --onefile ReBel.spec;
cp dist/ReBel ../bin/ReBel;
rm -r build dist;
