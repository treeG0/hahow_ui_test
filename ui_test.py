# coding=utf-8
"""
==============================================================================
Name:       ui_test.py
Purpose:    Hahow ui test
Author:     Huck
Created:    2/3/2022
==============================================================================
"""

import json
import logging
import platform
import unittest
from datetime import datetime

from selenium import webdriver
from selenium.webdriver import ActionChains
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait


class HahowRecruitTest(unittest.TestCase):

    BASE_RUL = 'https://github.com/hahow/hahow-recruit/'

    @classmethod
    def setUpClass(cls):
        logging.basicConfig(
            format='\n%(levelname)s: %(message)s', level=logging.INFO)
        cls.driver = cls.start_webdriver()

    @classmethod
    def start_webdriver(cls):
        os = platform.system()
        if os == 'Windows':
            ser = Service("./chromedriver.exe")
        elif os == 'Darwin':
            ser = Service("./chromedriver")
        else:
            raise RuntimeError('Not support OS. ' + os)

        op = webdriver.ChromeOptions()
        op.headless = True
        return webdriver.Chrome(service=ser, options=op)

    def screen_shot(self):
        timestamp = datetime.now().strftime('%y-%m-%d_%H-%M-%S')
        self.driver.get_screenshot_as_file(
            "screenshot" + self.id() + "_" + timestamp + ".png")

    def test_find_out_contributors(self):
        # element locators
        contributors_amount = (
            By.XPATH, '//*[contains(text(),"Contributors")]/span')
        contributors_avators = (By.XPATH, '//*[@class="mb-2 mr-2"]')
        contributors_card = (By.XPATH, '//*[@class="pb-3 px-3"]/div')

        self.driver.get(self.BASE_RUL)
        num = WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located(contributors_amount)).text

        logging.info(num + " contirbutors in the ptoject")

        contributors = WebDriverWait(self.driver, 10).until(
            EC.presence_of_all_elements_located(
                contributors_avators)
        )

        contributors_list = []
        for avator in contributors:
            action = ActionChains(self.driver)
            action.move_to_element(avator).pause(0.5).perform()
            hovercard = WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located(contributors_card)
            ).get_attribute("data-hovercard-tracking")
            contributors_list.append(json.loads(hovercard)["user_login"])
            logging.info(json.loads(hovercard)["user_login"])

        logging.info(contributors_list)

    def test_check_if_the_image_wireframe_existed(self):
        # element locators
        wireframe_img_1 = (
            By.XPATH, '//img[@src="/hahow/hahow-recruit/raw/master/assets/hero-list-page.png"]')
        wireframe_img_2 = (
            By.XPATH, '//img[@src="/hahow/hahow-recruit/raw/master/assets/hero-profile-page.png"]')

        self.driver.get(
            self.BASE_RUL + "blob/master/frontend.md")

        assert WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located(wireframe_img_1)
        )
        assert WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located(wireframe_img_2)
        )

    def test_the_last_commiter(self):
        # element locators
        commiter_name = (By.XPATH, '//*[@class="commit-author user-mention"]')

        self.driver.get(
            self.BASE_RUL + "commits/master")
        name = WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located(commiter_name)
        ).text
        logging.info("The last commiter is " + name)

    def tearDown(self):
        # Take a screen-shot when the case failed
        for method, error in self._outcome.errors:
            if error:
                self.screen_shot()

    @classmethod
    def tearDownClass(cls):
        cls.driver.close()
