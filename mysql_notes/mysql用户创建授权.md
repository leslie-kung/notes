### 创建用户
```
create user 'username'@'host' identified by 'password'
```
### 授权
```
grant all privileges on 数据库名.表名 to 'username'@'host'
```
### 用户创建并授权
```
grant all privileges on database.table to 'username'@'host' identified by 'password'
```
### 刷新权限
```
flush privileges
```
- localhost 表示只能在本地连，"%" 表示可以在任意一台机器连，"host" 指定ip 表示可以在指定机器上连
- database: 指定数据库，如果是所有数据库可以用 * 代替
- table: 指定表，如果是所有表可以用 * 代替
- all privileges ： 赋予所有权限

### 设置&修改用户密码
```
set password for 'username'@'host'=password('newpassowrd')
```
### 撤销用户权限
```
REVOKE privilege ON databasename.tablename FROM 'username'@'host'
```
- 假如你在给用户'dog'@'localhost'授权的时候是这样的(或类似的): GRANT SELECT ON test.user TO 'dog'@'localhost',则在使用REVOKE SELECT ON \*.\* FROM 'dog'@'localhost',命令并不能撤销该用户对test数据库中user表的SELECT 操作
- 相反,如果授权使用的是GRANT SELECT ON \*.\* TO 'dog'@'localhost',则REVOKE SELECT ON test.user FROM 'dog'@'localhost'命令也不能撤销该用户对test数据库中user表的Select 权限

### 查看用户权限
```
show grants for 'username'@'host'
```
### 删除用户
```
DROP USER 'username'@'host'
```
