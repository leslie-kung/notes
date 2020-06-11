

def gen_sql(opt='select', data=None, condition=None, table=None):
    """
    sql语句生成模块
    :param opt: 操作符，默认是查询select
    :param data: 数据
    :param condition: 条件
    :param table: 表名
    :return:
    """
    if not data or not isinstance(data, dict):
        print("没有需要处理的数据或者数据格式不是字典类型")
        return
    if not table:
        print("缺少表名")
        return
    where_str = None  # sql判断条件
    if condition and isinstance(condition, dict):
        where_str = ' and '.join([f"{key}='{value}'" if isinstance(value, str) else f"{key}={value}"
                                  for key, value in condition.items()])
    k_list, v_list = [], []
    for k, v in data.items():
        k_list.append(k)
        v_list.append(v)
    key_str = ','.join(k_list)

    message = None  # 返回的信息
    if opt.lower() == 'select':
        if not where_str:
            sql = "select {} from {}".format(key_str, table)
        else:
            sql = "select {} from {} where {}".format(key_str, table, where_str)
    elif opt.lower() == 'insert':
        sql = "insert ignore into {}({}) values {}".format(table, key_str, tuple(v_list))
    elif opt.lower() == 'update':
        set_value = ' and '.join([f"{key}='{value}'" if isinstance(value, str) else f"{key}={value}"
                                  for key, value in data.items()])
        sql = "update {} set {} where {}".format(table, set_value, where_str)
    else:
        sql = None
        message = "未定义的操作符:{}".format(opt)

    return sql, message


def test():
    data = {
        "name": "joe",
        "age": 18,
        "gender": "man"
    }
    condition = {
        "id": 100
    }
    table = "student"

    sql, msg = gen_sql(opt="select", data=data, condition=condition, table=table)
    print(sql, msg)
    sql, msg = gen_sql(opt="update", data=data, condition=condition, table=table)
    print(sql, msg)
    sql, msg = gen_sql(opt="insert", data=data, condition=condition, table=table)
    print(sql, msg)
    sql, msg = gen_sql(opt="select", data=data, table=table)
    print(sql, msg)
    sql, msg = gen_sql(opt="delete", data=data, condition=condition, table=table)
    print(sql, msg)


if __name__ == '__main__':
    test()
