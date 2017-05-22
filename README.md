# <img src="https://image.ibb.co/gd2eY5/7140ed35_9c05_47b8_ac23_72c2eeb6ec21.jpg" width=50 /> OiBusLeh

A telegram bot that provides Singapore bus information.

Bus logo is made by Freepik (www.freepik.com) from www.flaticon.com

## Set up
1. Set up python 3 environment. 
2. Install package from requirement.txt using `pip install requirements.txt`
2. Add in Telegram Bot API-KEY at `TOKEN = ""` in app.py. Create a new bot using [@BotFather](https://telegram.me/botfather) at Telegram. 
3. Add in LTA Datamall API-KEY at `API_KEY = ""` in bus.py which is inside the api folder. More info can be found at [mytransport.sg](https://www.mytransport.sg/content/mytransport/home/dataMall.html?myRad=3)
4. Add in Google Map Street View Image API at at `API_KEY = ""` in streetview.py. More info can be found at [here](https://developers.google.com/maps/documentation/streetview/intro)


## Testing the bot
### Local testing
Simply comment out these lines of code at app.py and using `python app.py`
```python
 updater.start_webhook(listen="0.0.0.0", port=PORT, url_path=TOKEN)
 updater.bot.set_webhook("https://<app_name>.herokuapp.com/" + TOKEN)
```

### Cloud testing
Create an application at heroku and update the url at app.py
```python
updater.bot.set_webhook("https://<app_name>.herokuapp.com/" + TOKEN)
```

## Reference
- This package is used to build this bot. [python-telegram-bot](https://github.com/python-telegram-bot/python-telegram-bot)
- Heroku set up guide. [Find out more](https://devcenter.heroku.com/articles/getting-started-with-nodejs#introduction)
- LTA Datamall API guide. [Find out more](https://www.mytransport.sg/content/dam/mytransport/DataMall_StaticData/LTA_DataMall_API_User_Guide.pdf)
- Street View API docs. [Learn more](https://developers.google.com/maps/documentation/streetview/intro)
- Try out this bot here [@OiBusLehBot](https://telegram.me/oibuslehbot)
