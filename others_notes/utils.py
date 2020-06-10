# -*- coding: utf8 -*-
import hashlib
import six
import redis


class MultipleHash(object):
    """根据提供的原始数据，和预定义的多个salt，生成多个hash值"""
    def __init__(self, salts, hash_func_name='md5'):
        self.hash_func = getattr(hashlib, hash_func_name)
        if len(salts) < 3:
            raise Exception("please provide more than 3 element(salt) in the salts")
        self.salts = salts

    def _safe_data(self, data):
        """
        :param data: 原始数据
        :return: 处理成对应python版本可以被hash函数的update方法解析的数据
        """
        if six.PY3:
            if isinstance(data, str):
                return data.encode()
            elif isinstance(data, bytes):
                return data
            else:
                raise Exception("please provide a right str data")
        else:
            if isinstance(data, unicode):
                return data.encode()
            elif isinstance(data, str):
                return data
            else:
                raise  Exception("please provide a right str data")

    def get_hash_values(self, data):
        """根据提供的原始数据, 返回多个hash函数值"""
        hash_values = []
        hash_obj = self.hash_func()
        for salt in self.salts:
            hash_obj.update(self._safe_data(data))
            hash_obj.update(self._safe_data(salt))
            ret = hash_obj.hexdigest()
            hash_values.append(int(ret, 16))
        return hash_values


class BloomFilter(object):
    """布隆过滤器"""

    def __init__(self, salts, redis_host="localhost", redis_port=6379, redis_db=0, redis_key=None):
        self.redis_host = redis_host
        self.redis_port = redis_port
        self.redis_db = redis_db
        self.redis_key = redis_key if redis_key else "bloom_filter"
        self.client = self._get_redis_cli()
        self.multiple_hash = MultipleHash(salts=salts)

    def _get_redis_cli(self):
        """返回一个redis连接对象"""
        pool = redis.ConnectionPool(host=self.redis_host, port=self.redis_port, db=self.redis_db)
        client = redis.StrictRedis(connection_pool=pool)
        return client

    def save(self, data):
        hash_values = self.multiple_hash.get_hash_values(data)
        for hash_value in hash_values:
            offset = self._get_offset(hash_value)
            self.client.setbit(self.redis_key, offset, 1)  # default 0, set 1 when match
        return True

    def reset(self, data):
        # 重置某个位置的值
        hash_values = self.multiple_hash.get_hash_values(data)
        for hash_value in hash_values:
            offset = self._get_offset(hash_value)
            self.client.setbit(self.redis_key, offset, 0)  # default 0, set 1 when match
        return True

    def _get_offset(self, hash_value):
        # (2**9 * 2**20 * 2**3): the len of hash list 哈希表的长度
        return hash_value % (2 ** 9 * 2 ** 20 * 2 ** 3)  # Mb -> bit

    def is_exists(self, data):
        hash_values = self.multiple_hash.get_hash_values(data)
        for hash_value in hash_values:
            offset = self._get_offset(hash_value)
            v = self.client.getbit(self.redis_key, offset)
            if v == 0:
                # self.save(data)  # 如果不存在，保存数据
                return False
        return True

    def clear(self):
        self.delete()

    def delete(self):
        self.client.delete(self.redis_key)


if __name__ == '__main__':
    data = ["asfdsafweafxc", "123", "123", "hello", "hello", 'haha']
    bm = BloomFilter(salts=['1', '2', '3', '4'], redis_host="127.0.0.1", redis_db=1, redis_key='test')
    bm.clear()
    for d in data:
        if not bm.is_exists(d):
            print("mapping data success : %s" % d)
            bm.save(d)
        else:
            print("find replace data : %s" % d)
    bm.clear()
    data2 = ['aa', 'cc', '123']
    for d in data2:
        if not bm.is_exists(d):
            print("mapping data success : %s" % d)
            bm.save(d)
        else:
            print("find replace data : %s" % d)
