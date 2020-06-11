# -*- coding: utf-8 -*-
import traceback
import requests
from others_notes.logs import init_log
from concurrent.futures import wait

# 当文件大小小于1M时，开启一个线程
MIN_FILE_SIZE = 1 * 1024 * 1024
# 当文件大小小于10M时，开启十个线程
MAX_FILE_SIZE = 10 * 1024 * 1024


class VideoDownload(object):
    def __init__(self, url=None, proxies=None, headers=None, thread_num=None, filename=None, log=None, executor=None):
        self.url = url
        self.proxies = proxies
        self.headers = headers
        self.thread_num = thread_num
        self.filename = filename
        self.logger = log
        self.executor = executor

    def _handler(self, start, end, thread_id):
        self.headers['Range'] = 'bytes=%d-%d' % (start, end)
        try:
            # 开启stream流模式
            r = requests.get(self.url, headers=self.headers, proxies=self.proxies, timeout=30, stream=True)
            # 写入文件对应位置
            # r+ 以读写方式打开文件，可对文件进行读和写操作
            with open(self.filename, "r+b") as fp:
                fp.seek(start)  # 移动当文件第p个字节处，绝对位置
                fp_position = fp.tell()  # 文件指针位置
                self.logger.info(f'线程{thread_id + 1}，文件指针位置{fp_position}，起始位置{start}，中止位置{end}，'
                                 f'写入{len(r.content)}字节')
                fp.write(r.content)
        except:
            self.logger.error(f"video download fail: filename:{self.filename}, messages:{traceback.format_exc()}")

    def download(self):
        # 用很少的流量获取响应头部信息！
        r = requests.head(self.url, headers=self.headers, proxies=self.proxies, timeout=30)
        self.logger.info(f"content_length: {r.headers['Content-Length']}")
        try:  # Content-Length获得文件主体的大小
            file_size = int(r.headers['content-length'])
        except:  # 当http服务器使用Connection:keep-alive时，不支持Content-Length
            self.logger.error("检查URL，或不支持对线程下载")
            return

        #  创建一个和要下载文件一样大小的文件
        fp = open(self.filename, "wb")
        # fp.truncate(file_size)  # 指定文件大小
        fp.close()

        if file_size <= MIN_FILE_SIZE:
            thread_num = 1
        elif file_size <= MAX_FILE_SIZE:
            thread_num = 10
        else:
            thread_num = 30

        if not self.thread_num:  # 如果没有传入线程数，按照文件大小处理线程数
            self.thread_num = thread_num

        part = file_size // self.thread_num
        array = []
        for i in range(self.thread_num):
            start = part * i
            if i == self.thread_num - 1:  # 最后一块
                end = file_size
            else:
                end = start + part
            array.append([start, end, i])
        future_list = []
        for args in array:
            future = self.executor.submit(self._handler, args[0], args[1], args[2])
            future_list.append(future)
            # wait 接收3个参数，FIRST_COMPLETED, FIRST_EXCEPTION 和ALL_COMPLETE，默认设置为ALL_COMPLETED。
            # 如果采用默认的ALL_COMPLETED，程序会阻塞直到线程池里面的所有任务都完成，再执行主线程
            wait(future_list)
        return file_size

        # self.executor.map(self._handler, array)
        # # 启动多线程写文件
        # part = file_size // self.thread_num  # 如果不能整除，最后一块应该多几个字节
        # self.logger.info(f'开启{self.thread_num}个线程')
        # for i in range(self.thread_num):
        #     start = part * i
        #     if i == self.thread_num - 1:  # 最后一块
        #         end = file_size
        #     else:
        #         end = start + part
        #
        #     t = threading.Thread(target=self._handler, args=(start, end, i,))
        #     t.setDaemon(True)
        #     t.start()
        #     threading_list.append(t)
        #     self.logger.info(f"线程{t.name}开启..")

        # # 等待所有线程下载完成
        # for t in threading_list:
        #     t.join()
        #     self.logger.info(f"线程{t.name}已经完成..")
        # self.logger.info(f"{self.filename}下载完成...")


if __name__ == '__main__':
    test_url = ''
    # 自定义请求头
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.87 Safari/537.36'
    }
    folder = "../log/"
    log_name = "video_all"
    filename = "../videos/haha.mp4"
    thread_num = None
    log = init_log(folder, log_name)
    video_kwargs = {
        "url": test_url,
        "headers": headers,
        "log": log,
        "filename": filename,
        "thread_num": thread_num
    }
    VideoDownload(**video_kwargs).download()
