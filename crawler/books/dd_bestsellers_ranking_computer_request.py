import requests
import json

from bs4 import BeautifulSoup

def request_dandan(url):
    try:
        response = requests.get(url)
        if response.status_code == 200:
            return response.text
    except requests.RequestException:
        return None

def write_item_to_file(bestsellers):
    print("开始写入数据")
    with open("book.json", "a", encoding="UTF-8") as f:
        f.write(json.dumps(bestsellers, ensure_ascii=False))
        f.close()
    print("文件写入完毕")

def parse_result(html):
    soup = BeautifulSoup(html, "lxml")
    list = soup.select("div.bang_list_box > ul > li")
    for bookItem in list:
        
        item_range = bookItem.find(class_="list_num").string.split('.')[0]
        item_name = bookItem.find(class_="name").a["title"]
        item_pic = bookItem.find(class_="pic").img["src"]
        publisherInfo = bookItem.select(".publisher_info")
        item_authorInfo = publisherInfo[0].a.string
        publicationDate = publisherInfo[1].span.string
        publishingHouse = publisherInfo[1].a.string if publisherInfo[1].a.string else ''
        priceOriginal = bookItem.find(class_="price_n").string
        priceCurrent = bookItem.find(class_="price_r").string
        discount = bookItem.find(class_="price_s").string        

        print("排行：" + item_range)
        print("书名：" + item_name)
        print("图片封面：" + item_pic)
        print("作者：" + item_authorInfo)
        print('出版日期：' + publicationDate)
        print('出版社：' + publishingHouse )
        print('原价：' + priceOriginal)
        print('现价：' + priceCurrent)
        print('折扣：' + discount)

        dictionary = {
            "ranking": item_range,
            "pic": item_pic,
            "name": item_name,
            "author_info": item_authorInfo,
            "publisher_info": {
                "Publication_date": publicationDate,
                "Publishing_house": publishingHouse
            },
            "price": {
                "price_original": priceOriginal,
                "price_current": priceCurrent,
                "discount": discount
            }
        }

        yield dictionary


def main():
    bestsellers = []
    for page in range(1,26):
        # url = 'http://bang.dangdang.com/books/fivestars/01.00.00.00.00.00-recent30-0-0-1-' + str(page)
        print("--------------------------------------------------------------------------")
        print('开始爬取第'+ str(page) + '页')
        print("--------------------------------------------------------------------------")
        url = (
            "http://bang.dangdang.com/books/bestsellers/01.54.00.00.00.00-recent30-0-0-1-"
            + str(page)
        )
        html = request_dandan(url)
        items = parse_result(html)
        # print(items)
        # parse_result(html)
        
        for item in items:
            print("--------------")
            bestsellers.append(item)
    write_item_to_file(bestsellers)

if __name__ == "__main__":
    main()
