from selenium import webdriver

browser = webdriver.Chrome()
browser.get('http://localhost:1337')

assert 'Django' in browser.title
