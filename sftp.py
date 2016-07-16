# -*- coding: utf-8 -*-
import paramiko
import os
import datetime
hostname = 'ftp.ipf.tuwien.ac.at'
username = 'esacci_sm_v022'
passwd = 'unoleferu164'
port = 22
local_dir = 'E:/data_collection/ESA_SoilMoisture/'
remote_dir = '_down/'
if not os.path.exists(local_dir):
    os.makedirs(local_dir)

def down_report(a,b):
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

try:
    t = paramiko.Transport(hostname,port)
    t.connect(username=username,password=passwd)
    sftp = paramiko.SFTPClient.from_transport(t)
    files = sftp.listdir(remote_dir)
    for f in files:
        print f
        print '#########################################'
        print 'Beginning to download file  from %s  %s ' % (hostname,datetime.datetime.now())
        sftp.get(os.path.join(remote_dir,f),os.path.join(local_dir,f),callback=down_report)
    t.close()
except Exception,e:
    print str(e)
