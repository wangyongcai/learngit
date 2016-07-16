#/usr/bin/python
# -*- coding:utf-8 -*-
from ftplib import FTP
import os
import sys
host = 'n5eil01u.ecs.nsidc.org'
username = 'anonymous'
passwd = 'kbqinfang@163.com'
port = 22
timeout = 30
remote_path = '/SAN/SMAP/SPL4SMGP.002/'
current_path = 'E:/data_collection/SMAP/SPL4SMGP.002/'
ftp = FTP()
ftp.connect(host)  #连接ftp服务器
ftp.login(username,passwd)     #登陆ftp服务器
print ftp.getwelcome()     #输出欢迎信息
a = []
ftp.cwd(remote_path)   #切换到数据目录

def add_str(line):
    '''回调函数
    :param line:ftp 服务器的所有行
    '''
    return a.append(line)
def down_info(a,b):
    '''回调函数
    :param a:已经下载的数据块
    :param b:数据块大小
    :param c:远程文件大小
    :return:返回下载进度
    '''
    per = 100.0 * a / b
    if per > 100:
        per = 100
    print '%.2f%%' % per
ftp.retrlines('LIST',callback=add_str)

for i in a:
    if i.startswith('d'):    #判断ftp server中文件夹方便递归
        path = i.split(' ')[-1]
        ftp.cwd(os.path.join(remote_path,path))
        local_path = os.path.join(current_path,path)
        if not os.path.exists(local_path):
            os.mkdir(local_path)
        for j in ftp.nlst():
            print j
            file_handler = os.path.join(local_path,j)
            ftp.retrbinary('RETR %s' % j,open(file_handler,'wb').write)

for j in ftp.nlst():
    file_handler = os.path.join(current_path,j)
    ftp.retrbinary('RETR %s' % j,open(file_handler,'wb').write)
