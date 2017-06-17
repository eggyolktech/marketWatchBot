# marketWatchBot Init (Digital Ocean)
sudo apt-get install python3-pip
sudo apt-get install python3-tk

pip install django
pip install beautifulsoup4
pip install html5lib
pip install pandas
pip install pandas_datareader
pip install matplotlib
pip install lxml
pip install telepot

###### At Windows ######
cd %APP_FOLDER%\telegram
bot_watcher.py

###### At digital Ocean ######
cd /app/marketWatchBot/market_watch
nohup ./bot_watcher.py >> ../log/bot_watcher.log 2> /dev/null &

# Setup at .profile
alias startBot='cd /app/marketWatchBot/market_watch/telegram; nohup ./bot_watcher.py >> ../log/bot_watcher.log 2>/dev/null &'
alias stopBot='pkill -f bot_watcher.py'

export PYTHONPATH=$(find /app/ -maxdepth 1 -type d | sed '/\/\./d' | tr '\n' ':' | sed 's/:$//')

# Crontab
00 07 * * 1-5 cd $APPMW/dailyfx; ./market_calendar.py >> $APPMW/log/dailyfx.log 2>&1
00 08 * * 1-5 cd $APPMW/aastocks; ./result_announcements.py >> $APPMW/log/aastocks.log 2>&1
00 * * * 1-7 cd $APPMW/dailyfx; ./market_alerts.py >> $APPMW/log/dailyfx.log 2>&1

