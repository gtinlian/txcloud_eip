#!/usr/bin/env python
# coding=utf-8
from tencentcloud.common import credential
from tencentcloud.common.profile.client_profile import ClientProfile
from tencentcloud.common.profile.http_profile import HttpProfile
from tencentcloud.common.exception.tencent_cloud_sdk_exception import TencentCloudSDKException
from tencentcloud.vpc.v20170312 import vpc_client, models
import json

# 认证信息 腾讯云授权
SecretId = ""
SecretKey = ""
Region = ""

# 内置变量 new_eip 返回创建eip获取的ip地址  ， eiplist 返回当前所有的eip信息列表
new_eip = {}
eiplist = []


def user_interface():
    cred = credential.Credential(SecretId, SecretKey)
    httpProfile = HttpProfile()
    httpProfile.endpoint = "vpc.tencentcloudapi.com"

    clientProfile = ClientProfile()
    clientProfile.httpProfile = httpProfile
    client = vpc_client.VpcClient(cred, Region, clientProfile)
    return client


def new():
    try:
        global new_eip
        client = user_interface()
        req = models.AllocateAddressesRequest()
        params = '{}'
        req.from_json_string(params)

        resp = client.AllocateAddresses(req)
        new_eip = json.loads(resp.to_json_string())
        return 0
    except TencentCloudSDKException as err:
        print(err)
        return -1


def get_list():
    try:
        global eiplist
        client = user_interface()

        req = models.DescribeAddressesRequest()
        params = '{}'
        req.from_json_string(params)
        req = json.loads(client.DescribeAddresses(req).to_json_string())

        if req['TotalCount'] == 0:
            print("创建错误")
            return 0
        else:
            eiplist = []
            for i in req['AddressSet']:
                eiplist.append(i)
            return req['TotalCount']


    except Exception as err:
        # print(err)
        print("test")
        return -1


def delete(eip):
    try:
        client = user_interface()

        req = models.ReleaseAddressesRequest()
        params = '{"AddressIds":["' + eip + '"]}'
        req.from_json_string(params)

        resp = client.ReleaseAddresses(req)
        print("delete ok")
        return 0

    except TencentCloudSDKException as err:
        print(err)
        return -1


def rebind(eip):
    try:
        client = user_interface()

        req = models.DisassociateAddressRequest()
        params = '{"AddressId":"' + eip + '"}'

        req.from_json_string(params)

        resp = client.DisassociateAddress(req)
        print('rebind ok')
        return 0

    except TencentCloudSDKException as err:
        print(err)
        return -1


def bind(eip, ins):
    try:
        client = user_interface()

        req = models.AssociateAddressRequest()
        params = '{"AddressId":"' + eip + '","InstanceId":"' + ins + '"}'
        req.from_json_string(params)

        resp = client.AssociateAddress(req)
        print('bind ok')

    except TencentCloudSDKException as err:
        print(err)
