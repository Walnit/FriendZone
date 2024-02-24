#!/bin/sh

curl https://alphacephei.com/vosk/models/vosk-model-small-en-us-0.15.zip -o model.zip
7z x model.zip
rm model.zip
mv vosk-model-small-en-us-0.15 model
