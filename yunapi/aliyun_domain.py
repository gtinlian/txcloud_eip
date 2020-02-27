#!/usr/bin/env python
# coding=utf-8

# annotation change domain aliyun cloud api

from aliyunsdkcore.client import AcsClient
from aliyunsdkcore.acs_exception.exceptions import ClientException
from aliyunsdkcore.acs_exception.exceptions import ServerException
from aliyunsdkalidns.request.v20150109.UpdateDomainRecordRequest import UpdateDomainRecordRequest

# 认证信息和地区 腾讯云授权
accessKeyId = ''
accessSecret = ''
RegionId = ''

# 域名的返 使用网页修改域名绑定F12查看url地址的RegionId
RecordId = ''

# 子域
RR = '@'


def change(ip):
    client = AcsClient(accessKeyId, accessSecret, RegionId)

    request = UpdateDomainRecordRequest()
    request.set_accept_format('json')

    request.set_RecordId(RecordId)
    request.set_RR(RR)
    request.set_Type("A")
    request.set_Value(ip)
    try:
        response = client.do_action_with_exception(request)
        # python2:  print(response)
        print(str(response, encoding='utf-8'))
        return 0
    except Exception as err:
        return -1
