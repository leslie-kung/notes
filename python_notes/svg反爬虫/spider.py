# -*- coding: utf8 -*-
import requests
import re
from scrapy import Selector

def get_file():
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.132 Safari/537.36'
    }
    # index
    url = 'http://www.porters.vip/confusion/food.html'
    resp = requests.get(url, headers=headers)
    with open('index.html', 'w', encoding='utf-8') as f:
        f.write(resp.text)
    # css file
    url_css = 'http://www.porters.vip/confusion/css/food.css'
    css_resp = requests.get(url_css, headers=headers)
    with open('test.css', 'w') as f:
        f.write(css_resp.text)
    # svg file
    url_svg = 'http://www.porters.vip/confusion/font/food.svg'
    svg_resp = requests.get(url_svg, headers=headers)
    with open('test.svg', 'w') as f:
        f.write(svg_resp.text)


def get_tensor_value():
    # 需要映射的class属性值
    with open('index.html', encoding='utf-8') as f:
        data = f.read()
    html = Selector(text=data)
    css_class_names = html.xpath('//div[@class="col more"]/d/@class').extract()
    print(css_class_names)
    # SVG字符定位
    with open('test.svg') as f:
        svg_data = f.read()
    # 按需求确认svg中的文字大小，需要找到font-size属性的值
    font_size = re.search('font-size:(\d+)px', svg_data).group(1)
    print(font_size)
    # 提取css样式文件中标签属性对应的坐标值
    with open('test.css') as f:
        css_data = f.read()
    css = css_data.replace(' ', '').replace('\n', '')
    nums = []
    for item in css_class_names:
        if not item:
            continue
        pile = '.%s{background:-(\d+)px-(\d+)px;}' % item
        obj = re.compile(pile)
        coord = obj.findall(css)
        if coord:
            x, y = coord[0]
            x, y = int(x), int(y)
            print(x, y)
            html = Selector(text=svg_data)
            # 定位坐标在svg文件中属于哪个text标签
            texts_y = html.xpath('//text/@y').extract()
            svg_y = [i for i in texts_y if y <= int(i)][0]
            # 获取该text下的内容
            svg_text = html.xpath('//text[@y="%s"]/text()'% svg_y).extract_first()
            print(svg_text)
            # 每个字符大小为 14 px，只需要将 CSS 样式中的 x 值除以字符大小，得到的就是该字符在字符串中的位置。除法得到的结果有可能是整数也有可能是非整数，
            # 当结果是整数是说明定位完全准确，我们利用切片特性就可以拿到字符。如果结果是非整数，就说明定位不完全准确，由于字符不可能出现一半，
            # 所以我们利用地板除（编程语言中常见的向下取整除法，返回商的整数部分。）
            nums.append(svg_text[x // int(font_size)])
    print(''.join(nums))


def main():
    # 先获取文件内容
    # get_file()
    # 获取坐标值
    get_tensor_value()

if __name__ == '__main__':
    main()
