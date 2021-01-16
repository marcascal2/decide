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
  

 
  def test_importPage(self):                    
    self.driver.get(f'{self.live_server_url}/census/login')
    self.driver.find_element(By.ID, "id_username").send_keys("admin")
    self.driver.find_element(By.ID, "id_password").send_keys("qwerty")
    self.driver.find_element(By.ID, "loginForm").submit()
    
    time.sleep(1)
    self.driver.find_element(By.CSS_SELECTOR, ".import-button > input").click()
    time.sleep(1)
    elements = self.driver.find_elements(By.ID, "import_form")
    assert len(elements) > 0 '''

  


  
 