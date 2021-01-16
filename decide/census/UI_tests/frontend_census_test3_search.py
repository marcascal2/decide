from django.test import TestCase
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
    options.headless = False
    self.driver = webdriver.Chrome(options=options)


    question = Question(desc='desc')
    question.save()

    v1 = Voting(id = 1, name='voting_testing1', question=question)
    v1.save()
    
    v2 = Voting(id = 3, name='voting_testing2', question=question)
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
  


  def test_search_voting(self):                    
    self.driver.get(f'{self.live_server_url}/census/login')
    self.driver.find_element(By.ID, "id_username").send_keys("admin")
    self.driver.find_element(By.ID, "id_password").send_keys("qwerty")
    self.driver.find_element(By.ID, "loginForm").submit()
    
    time.sleep(1)

    self.driver.find_element(By.ID, "q").send_keys("voting_testing1")
    self.driver.find_element(By.ID, "search_form").submit()

    time.sleep(1)

    elements = self.driver.find_elements(By.ID, "linea_votings")
    assert len(elements) < 2
    assert len(elements) > 0

  def test_search_voter1(self):                    
    self.driver.get(f'{self.live_server_url}/census/login')
    self.driver.find_element(By.ID, "id_username").send_keys("admin")
    self.driver.find_element(By.ID, "id_password").send_keys("qwerty")
    self.driver.find_element(By.ID, "loginForm").submit()

    time.sleep(1)
    
    self.driver.find_element(By.ID, "q").send_keys("voter1")
    self.driver.find_element(By.ID, "search_form").submit()

    time.sleep(1)

    elements = self.driver.find_elements(By.ID, "linea_votings")
    assert len(elements) < 2
    assert len(elements) > 0

  def test_search_voter(self):                    
    self.driver.get(f'{self.live_server_url}/census/login')
    self.driver.find_element(By.ID, "id_username").send_keys("admin")
    self.driver.find_element(By.ID, "id_password").send_keys("qwerty")
    self.driver.find_element(By.ID, "loginForm").submit()

    time.sleep(1)
    
    self.driver.find_element(By.ID, "q").send_keys("voter")
    self.driver.find_element(By.ID, "search_form").submit()

    time.sleep(1)

    elements = self.driver.find_elements(By.ID, "linea_votings")
    assert len(elements) < 3
    assert len(elements) > 1


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


  
 