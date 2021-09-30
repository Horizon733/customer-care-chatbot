cd /app

rasa train && rasa run --enable-api --cors "*" --debug -p $PORT