import time
import requests
import re
import io
import os
import shutil

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException, StaleElementReferenceException

options = Options()
options.headless = True

driver = webdriver.Chrome(r"C:\Users\olive\Downloads\chromedriver_win323\chromedriver.exe")

CLONE = False

shutil.rmtree("/output/")


def formatOutputurl(url, filename):
	output = "output/"
	if url:
		if url[0] == "/":
			output += url[1:]
		else:
			output += url
		output += "/" + filename
	else:
		output += filename
	return output


def run(url):
	global driver
	driver.get("https://github.com/techiehelper/actual-quizsite/tree/main" + url)

	todos = []

	time.sleep(1)
	#print(driver.find_elements_by_class_name(""))
	elements = driver.find_elements_by_xpath("//div[@class=\"Box-row Box-row--focus-gray py-2 d-flex position-relative js-navigation-item \"]")
	for element in elements:
		#print(url)
		try:
			fileName = element.text.split("\n")[0]
			if fileName != ". .":  # .\xe2\x80\x8a.
				try:
					element.find_element_by_class_name("octicon-file-directory")
					todos.append(fileName)
				except NoSuchElementException:
					if CLONE:
						os.makedirs(os.path.dirname(formatOutputurl(url, fileName)), exist_ok=True)
						print(requests.get("https://raw.githubusercontent.com/TechieHelper/actual-quizsite/main" + url + "/" + fileName).text, file=open(formatOutputurl(url, fileName), "w", encoding="utf-8"))
		except StaleElementReferenceException:
			print("Stale")

	for todo in todos:
		run(url + "/" + todo)


run("")

driver.quit()
