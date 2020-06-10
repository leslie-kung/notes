## 搭建jupyter服务器

### 安装jupyter

### 一、选择安装anaconda

1. 根目录下创建一个文件夹用来放anaconda安装包

2. 下载anaconda安装包（可以在官网上自行选择版本）
    ```
    wget https://repo.continuum.io/archive/Anaconda3-4.4.0-Linux-x86_64.sh
    ```
<!--more-->
3. 运行安装程序，安装anaconda
    ```
    Anaconda3-4.4.0-Linux-x86_64.sh
    ```
    **PS:** 该文件是一个可执行文件，如果下载的文件没有可执行权限，执行命令 chmod  641  Anaconda3-4.4.0-Linux-x86_64.sh 修改权限。
4. 配置环境变量
    ```
    vim /etc/environment
    ```
    将anaconda的bin文件夹的路径添加到环境变量中去（一般安装目录为/root/anaconda3/bin）
    ```
    source /etc/environment  # 使文件生效
    ```

### 二、配置jupyter notebook 的配置文件

1. 生成jupyter notebook 的配置文件
    ```
    # 该命令对于root用户
    jupyter notebook  --allow-root  --generate-config
    # 或者
    # 对于一般用户
    jupyter notebook  --generate-config 
    ```
    执行完该命令后会在 .jupyter文件夹下生成一个jupyter_notebook_config.py的配置文件

2. 修改配置
    ```
    vim jupyter_notebook_config.py # 打开文件修改配置项
    ```
    ```
    #  星号为允许任意ip访问服务
    c.NotebookApp.ip='*'
    # 该处设置登录jupyter 的密码
    c.NotebookApp.password = u'此处填写密码'
    # 该项为启动服务默认打开浏览器，设置为False默认不打开
    c.NotebookApp.open_browser = False
    # 端口号
    c.NotebookApp.port =8080
    # 该项设置notebook 的工作目录
    c.NotebookApp.notebook_dir = '/home/ubuntu/anaconda'
    ```
    **PS:** 对于密码的配置，我们不应该直接配置明文密码，因此需要对密码进行加密处理

    #### 打开ipython
    ```
    from notebook.auth import passwd
    passwd()
    ```
    该命令会让你输入密码，确认密码，然后返回一串加密后的字符串，类似于：sha1:f97cc330b40c:fb618ac068bd66fb36563e15da4f7462131ad5ee

    配置完成之后保存文件。

## 三、启动jupyter notebook应用
```
# 启动 notebook 服务
nohup jupyter notebook &

# 或者更加高级的用法
nohup jupyter notebook > /dev/null 2>&1 &
```
&emsp;&emsp;其中 nohup 是让进程在ssh连接断开时正常运行，&是为了让进程在后台运行。如果想结束该进程，通过 ps aux|grep jupyter-notebook 查找到进程的pid，通过kill命令结束进程。

&emsp;&emsp;/dev/null : 代表空设备文件，2：代表标准错误， 1：代表标准输出

&emsp;&emsp;该命令是将标准输出重定向到文件/dev/null，标准错误输出重定向到标准输出，最终都重定向到/dev/null 文件中.

&emsp;&emsp;服务启动后，我们就可以通过公网ip + 端口访问我们的服务了。

&emsp;&emsp;ps：如果是普通用户启动jupyter notebook应用的话，可能会报错  Permission denied: '/run/user/0/jupyter'，这时可以打开文件~/.bashrc，添加一行export XDG_RUNTIME_DIR=""，可以解决这个权限问题。

&emsp;&emsp;如果在创建新的文件的时候出现 Permission denied: Untitled.ipynb的问题，找到你的jupyter的工作家目录，ls -al 查看你的文件的权限， chmod 777 yourdir/ 修改文件的权限。

## 总结
&emsp;&emsp; 该服务的搭建过程中，有些重要的对方没有做，没有进行nginx反向代理，没有添加ssl证书。

