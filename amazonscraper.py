import requests
from bs4 import BeautifulSoup
import smtplib
import time

URL = 'https://www.amazon.ca/Cottonelle-Toilet-Cleancare-Strong-Biodegradable/dp/B07BNS6J62/ref=sr_1_6?keywords=toilet+paper&qid=1588865515&sr=8-6'

headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.129 Safari/537.36'
}

def check_price():

	page = requests.get(URL, headers = headers)

	soup = BeautifulSoup(page.content, 'html.parser')

	title = soup.find(id ="productTitle").get_text()
	price = soup.find(id="priceblock_ourprice").get_text()
	converted_price = float(price[5:7])

	if converted_price < 10:
		send_mail()

def send_mail():
	server = smtplib.SMTP('smtp.gmail.com', 587)
	server.ehlo()
	server.starttls()
	server.ehlo()

	server.login('YOUR EMAIL HERE', 'YOUR EMAIL PASSWORD HERE')

	subject = "Price fell down!"
	body = f"Check the amazon link and buy now: {URL}"
	msg = f"Subject: {subject}\n\n{body}"

	try:
		server.sendmail(
			"YOUR EMAIL HERE",
			"RECIPIENT EMAIL HERE", 
			msg)
		print('Email has been successfully sent')
	except SMTPException:
		print('Error: Email was not sent')
	finally:
		server.quit()


while True:
	check_price()
	time.sleep(86000)

