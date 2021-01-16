'''from django.test import TestCase
from django.contrib.staticfiles.testing import StaticLiveServerTestCase

from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys

from base.tests import BaseTestCase
from django.contrib.auth.models import User
from census.models import Census
from voting.models import Voting, Question
from datetime import date
import time

class TestGroupingbyadscripciontest(StaticLiveServerTestCase):
  
  def setUp(self):
    self.base = BaseTestCase()
    self.base.setUp()
    options = webdriver.ChromeOptions()
    options.headless = True
    self.driver = webdriver.Chrome(options=options)

    super().setUp()
  
  def tearDown(self):
    super().tearDown()
    
    self.driver.quit()
    self.base.tearDown()  
  

  def test_Login(self):                    
    self.driver.get(f'{self.live_server_url}/census/login')
    self.driver.find_element(By.ID, "id_username").send_keys("admin")
    self.driver.find_element(By.ID, "id_password").send_keys("qwerty")
    self.driver.find_element(By.ID, "loginForm").submit()
    
    time.sleep(2)
    actualTitle = self.driver.current_url
    print(self.driver.current_url)
    self.assertIn("/census/admin/",actualTitle)
    
  def test_errorLoginPage(self):                    
    self.driver.get(f'{self.live_server_url}/census/admin')
    print(self.driver.current_url)
    self.driver.find_element(By.LINK_TEXT, "aquí").click()
    actualTitle = self.driver.current_url
    expectedTitle = "/census/login/"    
    print(self.driver.current_url)
    #In case of a correct loging, a element with id 'user-tools' is shown in the upper right part
    self.assertIn("/census/login/",actualTitle)


  def test_eroor_Login(self):                    
    self.driver.get(f'{self.live_server_url}/census/login')
    self.driver.find_element(By.ID, "id_username").send_keys("admin")
    self.driver.find_element(By.ID, "id_password").send_keys("wrongpass")
    self.driver.find_element(By.ID, "loginForm").submit()
    
    time.sleep(2)
    actualTitle = self.driver.current_url
    print(self.driver.current_url)
    self.assertIn("/census/login/",actualTitle) '''

  

  


  
 