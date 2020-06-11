# -*- coding: utf-8 -*-
import base64
import string


def encryption(str):
    try:
        base_str = str.encode("utf8")
        base_str = base64.b64encode(base_str).decode("utf8")
        before = string.digits + string.ascii_letters + string.punctuation
        after = string.digits[3:] + string.digits[:3] + string.ascii_letters[3:] + string.ascii_letters[
                                                                                   :3] + string.punctuation[
                                                                                         3:] + string.punctuation[:3]
        table = ''.maketrans(before, after)
        return base_str.translate(table)
    except Exception:
        print("加密失败")


def decryption(str):
    try:
        before = string.digits[3:] + string.digits[:3] + string.ascii_letters[3:] + string.ascii_letters[
                                                                                   :3] + string.punctuation[
                                                                                         3:] + string.punctuation[:3]
        after = string.digits + string.ascii_letters + string.punctuation
        table = ''.maketrans(before, after)

        base_str = str.translate(table)
        return base64.b64decode(base_str).decode("utf8")
    except Exception:
        print("解密失败")


def run():
    while True:
        type_num = input("需要加密输入0，需要解密输入1：")
        if type_num == "0":
            mesg = input("请输入要加密的信息：")
            b = encryption(mesg)
            print("密文：", b)
        elif type_num == "1":
            mesg = input("请输入要解密的信息：")
            b = decryption(mesg)
            print("明文：", b)


if __name__ == '__main__':
    run()
