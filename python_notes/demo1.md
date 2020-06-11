#### 导包 
```
import datetime
```

#### 代码

```
def get_date_list(num=1):
    now = datetime.datetime.now()
    year = now.strftime('%Y')
    mon = now.strftime('%m')
    day = now.strftime('%d')
    date_list = []
    date_list.append([day, mon, year])
    temp = now
    for i in range(1, num):
        last_mon_day = temp - datetime.timedelta(days=temp.day)
        last_day = last_mon_day.strftime('%d')
        mon = last_mon_day.strftime('%m')
        year = last_mon_day.strftime('%Y')
        date_list.append([last_day, mon, year])
        temp = last_mon_day
    return date_list

# 返回过去一年每个月的时间
date_list = get_date_list(12)
print(date_list)
```
