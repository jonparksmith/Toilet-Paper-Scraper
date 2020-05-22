import requests
from bs4 import BeautifulSoup
import smtplib
import time

#Importing the confidential data from a private file
from private import user_agent, email, email_password

#This URL is where the product lives that you are trying to get the price from
URL = 'https://www.amazon.fr/Andrex-Classic-rouleaux-toilette-%C3%A9paisseurs/dp/B01KLXG3LA/ref=sr_1_5?__mk_fr_FR=%C3%85M%C3%85%C5%BD%C3%95%C3%91&dchild=1&keywords=toilet+paper&qid=1590161900&sr=8-5'

#You can find this by searching "My User Agent" in Google
headers = {'User-Agent': user_agent}

def check_price():

	page = requests.get(URL, headers = headers)

	soup = BeautifulSoup(page.content, "html.parser")
	soup2 = BeautifulSoup(soup.prettify(),"html.parser")

	title = soup2.find(id="title").get_text(strip=True)

	price = soup2.find(id="priceblock_ourprice").get_text(strip=True)

	#Depending on the price point, you may need to adjust this range to account for the total cost
	converted_price = float(price[0:1])

	#Here you can specify what your actual price threshold is
	if converted_price < 40:
		send_mail()

def send_mail():
	server = smtplib.SMTP('smtp.gmail.com', 587)
	server.ehlo()
	server.starttls()
	server.ehlo()

	server.login(email, email_password)

	subject = "Price fell down!"
	body = "Check the amazon link and buy now: {}".format(URL)
	msg = "Subject: {}\n\n{}".format(subject,body)

	try:
		server.sendmail(
			"pythontest@gmail.com",
			email, 
			msg)
		print('Email has been successfully sent')
	except SMTPException:
		print('Error: Email was not sent')
	finally:
		server.quit()


check_price()

