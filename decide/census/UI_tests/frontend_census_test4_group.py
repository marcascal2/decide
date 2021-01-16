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


    question = Question(desc='desc')
    question.save()

    question1 = Question(desc='desc1')
    question1.save()

    v1 = Voting(id = 1, name='voting_testing1', question=question)
    v1.save()
    
    v2 = Voting(id = 3, name='voting_testing2', question=question1)
    v2.save()

    user1 = User(id=5, username='voter1', password='test_password')
    user1.save()
    
    user2 = User(id=6, username='voter2', password='test_password')
    user2.save()

    c1 = Census(id=21, voting_id=1, voter_id=5, adscripcion='Colegio1', date=date(2021, 1, 16))
    c1.save()

    c2 = Census(id=22,voting_id=3, voter_id=6, adscripcion='Colegio2', date=date(2021, 1, 15))
    c2.save()

    super().setUp()
  
  def tearDown(self):
    super().tearDown()
    
    self.driver.quit()
    self.base.tearDown()

    super().setUp()
  
  def tearDown(self):
    super().tearDown()
    
    self.driver.quit()
    self.base.tearDown()

  def test_groupBy_voting(self):                    
    self.driver.get(f'{self.live_server_url}/census/login')
    self.driver.find_element(By.ID, "id_username").send_keys("admin")
    self.driver.find_element(By.ID, "id_password").send_keys("qwerty")
    self.driver.find_element(By.ID, "loginForm").submit()

    time.sleep(2)

    self.driver.find_element(By.LINK_TEXT, "voting_testing1").click()
    

    time.sleep(1)

    elements = self.driver.find_elements(By.ID, "voting_name")
    element = elements[0].get_attribute("innerText")
    print(element)

    assert len(elements) < 2
    assert len(elements) > 0
    self.assertIn("voting_testing1",element)


  def test_groupBy_adscription(self):                    
    self.driver.get(f'{self.live_server_url}/census/login')
    self.driver.find_element(By.ID, "id_username").send_keys("admin")
    self.driver.find_element(By.ID, "id_password").send_keys("qwerty")
    self.driver.find_element(By.ID, "loginForm").submit()

    time.sleep(2)

    self.driver.find_element(By.CSS_SELECTOR, "#headingTwo > .accordion-button").click()
    time.sleep(2)
    self.driver.find_element(By.LINK_TEXT, "Colegio1").click()
    

    time.sleep(1)

    

    elements = self.driver.find_elements(By.ID, "voting_adscription")
    element = elements[0].get_attribute("innerText")
    print(element)
 
    assert len(elements) < 2
    assert len(elements) > 0
    self.assertIn("Colegio1",element)

  def test_groupBy_voter(self):                    
    self.driver.get(f'{self.live_server_url}/census/login')
    self.driver.find_element(By.ID, "id_username").send_keys("admin")
    self.driver.find_element(By.ID, "id_password").send_keys("qwerty")
    self.driver.find_element(By.ID, "loginForm").submit()

    time.sleep(2)

    self.driver.find_element(By.CSS_SELECTOR, "#headingThree > .accordion-button").click()
    time.sleep(2)
    self.driver.find_element(By.LINK_TEXT, "voter1").click()
    

    time.sleep(1)

    

    elements = self.driver.find_elements(By.ID, "voter_username")
    element = elements[0].get_attribute("innerText")
    print(element)

    assert len(elements) < 2
    assert len(elements) > 0
    self.assertIn("voter1",element)

  def test_groupBy_date(self):                    
    self.driver.get(f'{self.live_server_url}/census/login')
    self.driver.find_element(By.ID, "id_username").send_keys("admin")
    self.driver.find_element(By.ID, "id_password").send_keys("qwerty")
    self.driver.find_element(By.ID, "loginForm").submit()

    time.sleep(2)

    self.driver.find_element(By.CSS_SELECTOR, "#headingFour > .accordion-button").click()
    time.sleep(2)
    self.driver.find_element(By.LINK_TEXT, "Jan. 15, 2021").click()
    
    time.sleep(1)
    
    elements = self.driver.find_elements(By.ID, "voting_date")
    element = elements[0].get_attribute("innerText")
    print(element)

    assert len(elements) < 2
    assert len(elements) > 0
    self.assertIn("Jan. 15, 2021",element)

  def test_groupBy_question(self):                    
    self.driver.get(f'{self.live_server_url}/census/login')
    self.driver.find_element(By.ID, "id_username").send_keys("admin")
    self.driver.find_element(By.ID, "id_password").send_keys("qwerty")
    self.driver.find_element(By.ID, "loginForm").submit()
    self.driver.set_window_size(1920, 1080)
    time.sleep(5)

    self.driver.find_element(By.LINK_TEXT, "desc1").click()
    

    time.sleep(1)

    

    elements = self.driver.find_elements(By.ID, "voting_name")
    element = elements[0].get_attribute("innerText")
    print(element)

    assert len(elements) < 2
    assert len(elements) > 0
    self.assertIn("voting_testing2",element)'''

  
 