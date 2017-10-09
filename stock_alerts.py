import json
from urllib2 import urlopen
import re
import smtplib
from email.mime.text import MIMEText

confg = None

# Sends an email to alert for the requested stock symbol
def send_alert(symbol, price):
    print 'Alerting for symbol ', symbol
    body = 'Current value of %s is %s' % (symbol, price)
    to = confg["mail"]["to"]
    frm = confg["mail"]["from"]
    mail = create_email(to, frm, 'Stock Alert!', body)
    send_email(mail, to, frm)

# Creates the contents of the email
def create_email(to, frm, subject, body):
    msg = MIMEText(body)
    msg['Subject'] = subject
    msg['From'] = frm
    msg['To'] = to

    return msg

# Logs into the remote SMTP server and sends the created email
def send_email(msg, to, frm):
    mail_account = confg['mail_account']

    server = smtplib.SMTP( str(mail_account['server']), int(mail_account['port']))
    server.set_debuglevel(False)

    server.starttls()
    server.login( str(mail_account['username']), str(mail_account['password']) )

    server.sendmail(frm, to, msg.as_string())
    server.quit()

    print 'Email sent'

if __name__ == '__main__':

    # Read the config file
    with open('config.json') as json_config_file:
        confg = json.load(json_config_file)
    stocks = confg["stocks"]
    alert = confg["alerts"]
    stockNames = '%22' + '%22,%22'.join(stocks) + '%22'

    # Request stock prices for those stock symbols specified in the config file
    response = urlopen("https://query.yahooapis.com/v1/public/yql?q=select%20Symbol,LastTradeWithTime%20from%20yahoo.finance.quotes%20where%20symbol%20in%20("+ stockNames +")&format=json&env=store%3A%2F%2Fdatatables.org%2Falltableswithkeys&callback=")

    results = json.load(response)

    # Regex to search for the current stock price
    s = re.compile('<b>[0-9]*[.][0-9]*</b>')
    p = re.compile(r"\d+[.]?\d*")

    for quote in results['query']['results']['quote']:
        symbol = quote['Symbol']
        print 'Symbol: ', symbol
        time_price = s.search(quote['LastTradeWithTime'])
        if time_price is None:
            print 'Price: ', quote['LastTradeWithTime']
        else:
            price = p.search(time_price.group())
            price = price.group()
            print 'Price: ', price

            # Send an alert if the current price is lower than our threshold
            if alert.has_key(symbol) and float(price) <= alert[symbol]:
                send_alert(symbol, price)

