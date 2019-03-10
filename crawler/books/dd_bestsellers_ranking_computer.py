# -*- coding: utf-8 -*-
# 爬取当当网的‘计算机/网络’类别的图书畅销排行榜书籍信息的爬虫


from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import TimeoutException, NoSuchElementException
import json

def format_publisher_info(Publication_date, Publishing_house):
    try:
        publisher_info = {}
        publisher_info['Publication_date'] = Publication_date
        publisher_info['Publishing_house'] = Publishing_house
        return publisher_info
    except TypeError as e:
        print('TypeError:', e)

def format_price(price_original, price_current, discount):
    try:
        price = {}
        price['price_original'] = price_original
        price['price_current'] = price_current
        price['discount'] = discount
        return price
    except TypeError as e:
        print('TypeError:', e)

def write_json_file(bestsellers):
    json_str = json.dumps(bestsellers, ensure_ascii=False)
    with open('./sample.json', 'w', encoding='utf-8') as f:
        f.write(json_str)
    print('文件写入完毕')
        




url = 'http://bang.dangdang.com/books/bestsellers/01.54.00.00.00.00-recent30-0-0-1-1'
def main(url):
    try:
        bestsellers = []
        chrome_options = Options()
        chrome_options.add_argument('--headless')
        chrome_options.add_argument('--disable-gpu')
        driver = webdriver.Chrome(chrome_options=chrome_options)
        driver.get(url)
        currentBookList = driver.find_elements_by_css_selector('.bang_list.clearfix.bang_list_mode li')

        

        for index, bookItem in enumerate(currentBookList):
            dictionary = {}
            name = bookItem.find_element_by_css_selector('.name a').text
            pic = bookItem.find_element_by_css_selector('.pic a').get_attribute('href')
            publisher_info_eles = bookItem.find_elements_by_css_selector('.publisher_info')
            
            # 获取完整 author_info 成功方案1 xpath
            author_info = publisher_info_eles[0].find_element_by_xpath("./a[1]").get_attribute('title')
            # 获取完整 author_info 成功方案2 css_selector
            # author_info2 = bookItem.find_element_by_css_selector('.publisher_info a').get_attribute('title')

            Publication_date = publisher_info_eles[1].find_element_by_css_selector('span').text
            Publishing_house = publisher_info_eles[1].find_element_by_css_selector('a').text
            publisher_info = format_publisher_info(Publication_date, Publishing_house)

            price_original = bookItem.find_element_by_css_selector('.price_n').text
            price_current = bookItem.find_element_by_css_selector('.price_r').text
            discount = bookItem.find_element_by_css_selector('.price_s').text
            price = format_price(price_original, price_current, discount)
            
            print('排行：' + str(index + 1))
            print('图片封面：' + pic)
            print('书名：' + name)
            print('作者：' + author_info)
            print('出版日期：' + publisher_info['Publication_date'])
            print('出版社：' + publisher_info['Publishing_house'])
            print('原价：' + price_original)
            print('现价：' + price_current)
            print('折扣：' + discount)


            
            dictionary['ranking'] = str(index + 1)
            dictionary['pic'] = pic
            dictionary['name'] = name
            dictionary['author_info'] = author_info
            dictionary['publisher_info'] = publisher_info
            dictionary['price'] = price
            
            
            bestsellers.append(dictionary)

            print('--------------')

        write_json_file(bestsellers)
        return bestsellers


        
    except TimeoutException as e:
        print('TimeoutError:', e)
    except ConnectionRefusedError as e:
        print('ConnectionRefusedError:', e)
    except NoSuchElementException as e:
        print('NoSuchElementException:', e)
        print('No Element:')
    except ValueError as e:
        print('ValueError:', e)
    except TypeError as e:
        print('TypeError:', e)
    finally:
        driver.close()

main(url)