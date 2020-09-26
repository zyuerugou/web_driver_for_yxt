# -*- coding: utf-8 -*-
"""
Created on Thu Apr  9 19:44:46 2020

自动学习yxt，15门

@author: zyuerugou
"""

import os
import time
import logging
from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.chrome.options import Options

url = 'https://*****.html'
org_code = '****'
usr = '******'
psw = '******'
content = r'学习学习学习'
# 每天需要的课程数量
course_num = 15
# 初始的专栏
zl_index = 9
# 初始的课程系列
class_i = 1
# 初始的课程节数
course_begin = 1
# 初始的课程计数
course_j = 5

logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s - %(filename)s[line:%(lineno)d] - %(levelname)s: %(message)s')



def back_btn_test(driver):
    '''
    退出按钮，测试是否未学
    @return    True:   未学
               False:  已学
    '''
    flg = True
    # 退出按钮
    btn_0 = driver.find_element_by_id('back_btn')
    btn_0.click()
    # 延时
    driver.implicitly_wait(3)
    try:
        # 有弹窗
        btn_0 = driver.find_element_by_id('_confirm_btnB')
        btn_0.click()
    except BaseException as e:
        # 没有弹窗
        logging.error(e.__str__())
        # 延时
        time.sleep(5)
        # 设置标记
        flg = False
    
    return flg



def post_comment(driver):
    '''
    发送评论
    '''
    # 点击评论
    btn_0 = driver.find_element_by_id('post_btn')
    btn_0.click()
    
    
    # 输入评论内容
    content_0 = driver.find_element_by_id('content')
    content_0.send_keys(content)
    
    # 发送评论
    btn_0 = driver.find_element_by_id('send_btn')
    btn_0.click()
    
    # 延时
    time.sleep(10)
    
    try:
        btn_0 = driver.find_element_by_id('cancel_btn')
        btn_0.click()
    except BaseException as e:
        logging.info('post comment')


def web_refresh(driver):
    '''
    刷新页面
    '''
    try:
        driver.refresh() # 刷新方法 refresh
        time.sleep(5)
    except BaseException as e:
        logging.error(e.__str__())


def get_one_course(driver, course, j):
    '''
    进入单节课程操作
    @return    j:   累计课程
    '''
    ActionChains(driver).click_and_hold(course).perform()
    time.sleep(0.5)
    ActionChains(driver).release(course).perform()
    
    # 延时
    time.sleep(5)
    
    # 轮询
    cnt = 0
    while True:
        try:
            driver.find_element_by_id('post_btn')
            break
        except BaseException as e:
            web_refresh(driver)
            cnt = cnt + 1
            logging.error('web refresh {0} times'.format(cnt))
        
        
    
    # 判断是否未学
    flg_study = back_btn_test(driver)
    if not flg_study:
        return j
            
    
    # 发送评论
    post_comment(driver)
    
    
    try:
        # 音频
        audio_0 = driver.find_element_by_tag_name('audio')
        driver.execute_script("arguments[0].play()",audio_0)
    except BaseException as e:
        logging.error(e.__str__())
    
    try:
        # 视频
        vedio_0 = driver.find_element_by_id('view_btn')
        vedio_0.click()
        
    except BaseException as e:
        logging.error(e.__str__())
    
    
    # 轮询
    flg = True
    while flg:
        
        time.sleep(60)
        
        # 判断是否未学
        flg_study = back_btn_test(driver)
        if not flg_study:
            flg = False
            j = j + 1
            logging.info('get_one_course j={0}'.format(j))
            time.sleep(3)
            
    return j
                    

def get_one_class(driver, j, class_elemt):
    '''
    进入一个课程系列
    @return j
    '''
    class_elemt.click()
    
    
    # 获取课程系列的课程列表
    course_list = driver.find_elements_by_class_name('course')
    
    course_length = len(course_list)
    
    # 进入单个课程
    k = 0
    for k in range(course_begin, course_length):
        
        # 轮询
        cnt = 0
        while True:
            try:
                # 获取课程系列的课程列表
                course_list = driver.find_elements_by_class_name('course')
                break
            except BaseException as e:
                web_refresh(driver)
                cnt = cnt + 1
                logging.error('web refresh {0} times'.format(cnt))
            
        # 进入单个课程
        j = get_one_course(driver, course_list[k], j)  
        
        # 达到课程数量以后跳出循环
        if j >= course_num:
            break
    
    btn_0 = driver.find_element_by_id('back_btn')
    btn_0.click()
    
    logging.info('get_one_class k={0}'.format(k))
    return j



def get_classes(driver, index):
    '''
    进入专栏部分
    '''
    
    # 进入专栏
    btn_0 = driver.find_element_by_class_name('FUN_STUDY_COURSE_PAGE_SHOTCUT_ZT')
    btn_0.click()
    
    
    # 进入对应的专栏
    btn_0 = driver.find_element_by_xpath('//*[@id="contentInfo_title"]/div/ul/div/div/div/li[{0}]/a'.format(index))
    ActionChains(driver).click_and_hold(btn_0).perform()
    time.sleep(0.5)
    ActionChains(driver).release(btn_0).perform()
    
    
    # 获取课程列表
    class_list = driver.find_elements_by_class_name('topic')
    
    i = class_i
    j = course_j
    
    # 进入课程系列
    while j < course_num:
        
        class_list = driver.find_elements_by_class_name('topic')
        
        # 进入课程系列
        j = get_one_class(driver, j, class_list[i])
        
        logging.info('get_classes i={0}'.format(i))
        
        
        i = i + 1
        




def opera_for_once():
    '''
    操作浏览器的主要流程
    '''
    
    # 打开chrome
    chrome_options = Options()
    chrome_options.add_argument('--mute-audio') # 静音
    driver=webdriver.Chrome(options = chrome_options)
    driver.get(url)
    driver.maximize_window()
    
    # 输入企业码并点击下一步
    input_0 = driver.find_element_by_id('orgCode')
    input_0.send_keys(org_code)
    
    btn_0 = driver.find_element_by_id('next_btn')
    btn_0.click()
    
    # 延时
    driver.implicitly_wait(30)
    
    # 输入用户名密码，点击登录
    input_0 = driver.find_element_by_id('username')
    input_0.send_keys(usr)
    
    input_0 = driver.find_element_by_id('password')
    input_0.send_keys(psw)
    
    btn_0 = driver.find_element_by_id('login_btn')
    btn_0.click()
    
    
    time.sleep(3)
    
    # 关闭登录的提示弹窗
    btn_0 = driver.find_element_by_class_name('closedBtn')
    btn_0.click()
    
    
    # 查找具体的课程
    index = zl_index
    get_classes(driver, index)
    
    logging.info('opera_for_once done')
    logging.info('class_index index={0}'.format(index))
    
    # 暂停
    os.system('pause')
    
    
if __name__ == '__main__':
    opera_for_once()
    

