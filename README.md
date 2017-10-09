# stock_alerts
Provides real-time email stock alerts when the value of the stock is under a certain pre-defined threshold

Includes a JSON configuration file 
- set the destination addresses
- with credentials into your remote SMTP server (GMail, YMail, AOL,.. email accounts)
- set the list of stock symbols to check allow with their thresholds

# Setup
1. Clone this repository
2. Modify the included config.json with the to and from email addresses, email credentials, the stocks symbols and their respoective values
3. Setup Cron/Crontab to run the _stock_alerts.py_ script every hour/day/week. For more info: (https://help.ubuntu.com/community/CronHowto)
