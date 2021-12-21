echo "Starting server with Rasa models..."

MODELS=models

rasa run -m $MODELS --enable-api --cors “*” --debug

