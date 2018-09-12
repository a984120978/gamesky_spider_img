from lxml import etree
import requests
import os
num = 1
img_num = 1
print('游民星空福利一键下载，请输入正文第一页图片的地址')
url = input('请输入浏览器地址\n')
while True:
    if num ==1:
        r = requests.get(url)

        r = r.content.decode()

        html = etree.HTML(r)
        num += 1
        try:
            os.makedirs('./img')
        except:
            pass

        ret_list = html.xpath('//div[@class="Mid2L_con"]/p/a/@href')
        # del ret_list[0]
        for src_link in ret_list:
            link = src_link[52:]
            try:
                img = requests.get(link)
                img = img.content

                with open('./img/%03d.jpg' % img_num, 'wb')as f:
                    f.write(img)

                print(img_num)
                img_num += 1
            except:
                pass

    else:
        # https://www.gamersky.com/ent/201808/1093224_2.shtml
        url1 = url[:-6]
        r = requests.get(url1 + '_%s.shtml'%num)
        num += 1

        r = r.content

        html = etree.HTML(r)
        try:
            os.makedirs('./img')
        except:
            pass

        ret_list = html.xpath('//div[@class="Mid2L_con"]/p/a/@href')
        if len(ret_list) == 0:
            exit()
        for src_link in ret_list:
            link = src_link[52:]
            img = requests.get(link)
            img = img.content

            with open('img/%03d.jpg'%img_num,'wb')as f:
                f.write(img)

            print(img_num)
            img_num += 1
