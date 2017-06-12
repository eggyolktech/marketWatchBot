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

# At Window
cd C:\Users\Hin\djangodev\
myvenv\Scripts\activate
cd C:\Users\Hin\djangodev\pricewatch\
run_fx_bot_watcher.py

# At digital Ocean
cd /app/marketWatchBot
nohup python run_fx_bot_watcher.py >> ./log/run_fx_bot_watcher.log 2> /dev/null &

# Crontab
32 07 * * 1-5 python /app/marketWatchBot/get_daily_fx_calendar.py >> /app/marketWatchBot/log/get_daily_fx_calendar.log 2>&1
32 07 * * 1-5 python /app/marketWatchBot/get_aastocks_calendar.py >> /app/marketWatchBot/log/get_aastocks_calendar.log 2>&1
