import queue
import threading

from lxml import etree
import requests
import os


def file(img, img_num):
    with open('./img/%03d.jpg' % img_num, 'wb')as f:
        f.write(img)


def r_dow(url, img_num):
    print(url)
    link = url[52:]
    try:
        img = requests.get(link)
        img = img.content
        file(img, img_num)
        print(img_num)
    except:
        pass


def main():
    q_list = queue.Queue()
    num = 1

    print('游民星空福利一键下载，请输入正文第一页图片的地址')
    url = input('请输入浏览器地址\n')
    while True:
        if num == 1:
            r = requests.get(url)
            r = r.content.decode()
            html = etree.HTML(r)
            num += 1
            try:
                os.makedirs('./img')
            except:
                pass
            ret_list = html.xpath('//div[@class="Mid2L_con"]/p/a/@href')
            q_list.put(ret_list)
        else:
            # https://www.gamersky.com/ent/201808/1093224_2.shtml
            url1 = url[:-6]
            r = requests.get(url1 + '_%s.shtml' % num)
            num += 1
            r = r.content
            html = etree.HTML(r)
            try:
                os.makedirs('./img')
            except:
                pass
            ret_list = html.xpath('//div[@class="Mid2L_con"]/p/a/@href')
            if len(ret_list) == 0:
                break
            q_list.put(ret_list)
    img_num = 0
    list1 = list()
    while True:
        if q_list.empty():
            break
        list1.extend(q_list.get())
    for url in list1:
        t = threading.Thread(target=r_dow, args=(url, img_num))
        img_num += 1
        t.start()


if __name__ == '__main__':
    main()
