# bin/bash

echo "*******************"
echo "*** START BUILD ***"
echo "*******************"

echo "Checking if venv exists:"
FILE=./venv
if test -f "$FILE"; then
    echo "$FILE exist"
else
    echo "$FILE didn't exist, make it..."
    python3 -m venv venv
fi

echo "Access to the virtualenv for the setting"
source venv/bin/activate

echo "****** INSTALLING DEPENDENCIES ******"
pip install numpy

echo "***** INSTALLING DECODERS *******"
sh ctc-decoders.sh

echo "***** INSTALLING REQUIREMENTS ******"
pip install -r requirements.txt

echo "***** BUILD DOCKER IMAGES ******"
cd rasa
sudo docker network create jarvis-net
sudo docker run -it -p 5055:5055 --network jarvis-net --mount "type=bind,source=$(pwd)/,target=/app" --name action-server rasa-actions
sudo docker run -it -p 5005:5005 --network jarvis-net --mount "type=bind,source=$(pwd)/,target=/app" rasa-shell

echo " Build successfull: Status OK"
