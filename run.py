#!/usr/bin/env python
# coding=utf-8
from yunapi import txy_eip as eip, aliyun_domain
import time


def create_bind():
    eip.get_list()
    if len(eip.eiplist) > 0:
        return 0
    else:
        eip.new()
        while True:
            time.sleep(5)
            eip.get_list()
            if eip.eiplist == None:
                continue
            if eip.eiplist == 0:
                continue
            for i in eip.eiplist:
                print(i['AddressId'])
                eip.bind(i['AddressId'], 'ins-kbczzagy')
            if eip.eiplist[0]['AddressStatus'] == 'BIND':
                break

        return 1


def free_all():
    eip.get_list()
    for i in eip.eiplist:
        if i['AddressStatus'] == 'BIND':
            eip.rebind(i['AddressId'])
            time.sleep(10)
        eip.delete(i['AddressId'])


def free_unbind():
    eip.get_list()
    for i in eip.eiplist:
        if i['AddressStatus'] != 'BIND':
            eip.delete(i['AddressId'])


while True:
    # 释放eip
    free_all()
    time.sleep(10)

    eip.eiplist = []
    # 创建绑定ip
    create_bind()
    time.sleep(10)

    # 释放掉没有绑定的ip
    free_unbind()
    eip.get_list()
    if len(eip.eiplist) != 1:
        continue
    if eip.eiplist[0]["AddressStatus"] != 'BIND':
        continue
    eip.get_list()
    print(eip.eiplist)

    # 将ip地址绑定到域名中
    if aliyun_domain.change(eip.eiplist[0]['AddressIp']) == 0:
        print("绑定ip成功\n\tip地址为:" + eip.eiplist[0]['AddressIp'])

    time.sleep(86400)
