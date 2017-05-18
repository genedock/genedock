#!/usr/bin/python
# -*- coding: utf-8 -*-

import gdpy

# 填写秘钥信息及ENDPOINT（此处需修改-1）
ACCESS_KEY_ID = ''
ACCESS_KEY_SECRET = ''
ENDPOINT = 'cn-beijing-api.genedock.com' # 以北京为例

# 工作流所属的资源账号，如果是公共工作流，此处应为'public'（此处需修改-2）
WORKFLOW_NAME = 'Fastqc'
WORKFLOW_VERSION = 1
RES_ACCOUNT_NAME = 'public'

# 初始化Auth信息
auth = gdpy.GeneDockAuth(ACCESS_KEY_ID, ACCESS_KEY_SECRET)

# 创建一个workflow对象
workflow = gdpy.Workflows(auth, ENDPOINT, RES_ACCOUNT_NAME)

# 获取某个可执行的workflow参数模板
resp = workflow.get_exc_workflow(WORKFLOW_NAME, WORKFLOW_VERSION)

# 将获取参数模板信息转换成yaml格式并输出
workflow_param = gdpy.yml_utils.yaml_dumper(resp.parameter)
print workflow_param
