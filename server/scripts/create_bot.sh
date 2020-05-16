cd ..
BotID="$1"
cp -r hummingbot hummingbot_$BotID
cp -r interface/* hummingbot_$BotID/bin/
cd hummingbot_$BotID
python bin/main.py