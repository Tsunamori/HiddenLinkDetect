#!/usr/bin/python
# -*- coding:utf-8 -*-
'''need to install selenium, using chromedriver and install chrome to use the headless mode'''

import re
import urllib
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import os


def get_domain(domain):
    pro, rest = urllib.splittype(domain)
    domain, rest = urllib.splithost(rest)
    return ".".join(domain.split(".")[1:])

def checklink(urlprovided):
    node_list = []
    url_list = []
    hide_list = []

    try:
        options = Options()
    # use the headless mode of chrome.
        options.add_argument("--headless")
        options.add_argument('user-agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/65.0.3325.181 Safari/537.36"')
    #driver = webdriver.Chrome(chrome_options=options)
    #driver = webdriver.Chrome('D:/lzy/chromedriver_win32/chromedriver.exe')

        '''need to set the path of chromedriver manually'''
        driver = webdriver.Chrome(executable_path=r'D:/lzy/chromedriver_win32/chromedriver.exe',chrome_options=options )
        domain = urlprovided
        driver.get(domain)

    # get all the 'a' tag and return.
        all_node = driver.find_elements_by_tag_name("a")

        for a in all_node:
        # check if the node has 'href' or 'src'.
            url = a.get_attribute("href") or a.get_attribute('src')
            if url is None:
                continue

        # if it is true, check if it has http
            http_match = re.search(r"^(http).*", url)

        # get url from node
            if http_match:
                node_list.append(a)
                url_list.append(url)

        domain = get_domain(domain)
 #  check if the url has same host name
        i = 0
        while i < len(url_list):
            if domain == get_domain(url_list[i]):
                node_list.pop(i)
                url_list.pop(i)
                i -= 1
            i += 1

        for i in node_list:
            if not i.is_displayed():
                hide_list.append(i)
            else:
                value = i.value_of_css_property("font-size")
                # remove the string besides number, convert them to integer
                value = int(re.sub(r"[a-zA-Z]", "", value))
                if value < 2:
                    hide_list.append(i)

            # check visibility visible:hidden
                value = i.value_of_css_property('visibility')
                if value == "hidden":
                    hide_list.append(i)

                #check color    rgba(255, 255, 255, 1)} white
                color = i.value_of_css_property('color')
                if color == "rgba(255, 255, 255, 1)":
                    hide_list.append(i)

                #check the opacity, if it is below 0.2, we assume it is a hidden link.
                value = i.value_of_css_property('opacity')
                opacity = float(value)
                if opacity <= 0.2:
                    hide_list.append(i)

                #check the display if it is none
                value = i.value_of_css_property('display')
                if value == 'none':
                    hide_list.append(i)

        # if the marquee's height less than 5 or not displayed, we assume it is a hidden link
        marquee = driver.find_elements_by_tag_name("marquee")
        for i in marquee:
            value = i.value_of_css_property('height')
            height = float(re.sub("[a-zA-Z]", "", str(value)))
            if not i.is_displayed():
                hide_list.append(i.find_element_by_tag_name("a"))
            elif height < 5:
                hide_list.append(i.find_element_by_tag_name('a'))

        meta = driver.find_elements_by_tag_name("meta")
        for i in meta:
            if i.get_attribute("url"):
                hide_list.append(i)

        iframe = driver.find_elements_by_tag_name("iframe")
        for i in iframe:
            hide_list.append(i)

    except Exception as e:
        pass
    finally:
        test_list = []
        for i in hide_list:
            if i.get_attribute('href'):
                test_list.append(i.get_attribute("href"))
            elif i.get_attribute("src"):
                test_list.append(i.get_attribute("src"))
            elif i.get_attribute('url'):
                test_list.append(i.get_attribute('url'))
        hide_list = test_list
        print('hiddenlink:',hide_list)
        target_num = len(hide_list)
        if not os.path.exists('result.txt'):
            #fobj1 = open('result.txt', 'w')
            with open('result.txt',"w")as fobj1:
                for i in range(target_num):
                    print >> fobj1, 'the url contains hidden link: ', urlprovided
                    #print >> fobj1, hide_list[i][1:-1]
                    print >> fobj1,'the hidden link: ', hide_list[i]
                fobj1.close()
        with open('result.txt',"a") as fobj2:
            for i in range(target_num):
                print >> fobj2,'the url contains hidden link: ', urlprovided
                #print >> fobj2, hide_list[i][1:-1]
                print >> fobj2,'the hidden link: ', hide_list[i]
            fobj2.close()
        driver.quit()

