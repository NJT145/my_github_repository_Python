from selenium import webdriver
import time
driver = webdriver.Firefox()
driver.get("http://www.sehir.edu.tr/en/Pages/home.aspx")
search = driver.find_element_by_id("textfield")
button = driver.find_element_by_class_name("ara_rsm") 
search.send_keys("Computer Engineering") # send words to box

button.click() # click search button
time.sleep(10)  # wait 10 sec
#html = driver.page_source
driver.close()
#print html
