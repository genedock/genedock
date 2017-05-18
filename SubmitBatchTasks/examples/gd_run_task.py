#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import logging
import gdpy

# 记录任务运行的日志信息，日志信息存储在当前目录下的gd_task.log文件中
LOG_FILENAME = os.path.join(os.getcwd(), 'gd_task.log')
LOG_FORMAT = "[%(asctime)s] - %(filename)s - %(funcName)s - %(lineno)d - [%(levelname)s] : %(message)s"

# 填写秘钥信息，账号信息及ENDPOINT地址（此处需修改-1）
ACCESS_KEY_ID = ''
ACCESS_KEY_SECRET = ''
ENDPOINT = 'cn-beijing-api.genedock.com' # 北京域
RES_ACCOUNT_NAME = '' # 填写自己在GeneDock网站申请的账号

# 工作流名称，版本及所属账号（此处需修改-2）
WORKFLOW_NAME = 'Fastqc'
WORKFLOW_VERSION = 1
WORKFLOW_OWNER = 'public' # 工作流所属的账号，如果是公共工作流，则为public；若属于自己账号，则与RES_ACCOUNT_NAME相同

# 运行任务配置文件和样本文件列表（此处需修改-3）
TEMPLATE_FILE = 'Fastqc_param_test.yml'
SAMPLE_LIST = 'samples.txt'

# 初始化Auth信息
auth = gdpy.GeneDockAuth(ACCESS_KEY_ID, ACCESS_KEY_SECRET)


def init_logger():
    """
    初始化记录日志信息
    """
    logging.captureWarnings(True)
    logging.basicConfig(filename=LOG_FILENAME, format=LOG_FORMAT)
    logger = logging.getLogger("GeneDock")
    logger.setLevel(logging.INFO)
    return logger

_logger = init_logger()


def active_workflow(auth):
    """
    创建一个task对象，运行工作流，提交任务，同时处理可能的错误信息
    """
    task = gdpy.Tasks(auth, ENDPOINT, RES_ACCOUNT_NAME, connect_timeout=3600)

    try:
        resp = task.active_workflow(TEMPLATE_FILE + '_tmp', WORKFLOW_NAME, WORKFLOW_VERSION, WORKFLOW_OWNER)
        _logger.info('Start task successfully! task_name: {}, task_id: {}'.format(
            resp.task_name, resp.task_id))
        print('Start task successfully!\ntask_name: {}, task_id: {}'.format(
            resp.task_name, resp.task_id))
    except gdpy.exceptions.RequestError as e:
        _logger.warning('Failed to start task! status: {}, error: {}'.format(
            e.status, e.error_message.decode('utf-8')))
        print('Failed to start task! status: {}\nerror: {}'.format(
            e.status, e.error_message.decode('utf-8')))
        print('NetWork Connection Error, please check your network and retry.')
    except gdpy.exceptions.ServerError as e:
        _logger.warning('Failed to start task! status: {}, error: {}, 错误: {}'.format(
            e.status, e.error_message.decode('utf-8'), e.error_message_chs.decode('utf-8')))
        print('Failed to start task! status: {}\nerror: {} 错误: {}'.format(
            e.status, e.error_message.decode('utf-8'), e.error_message_chs.decode('utf-8')))
        if e.status // 100 == 5:
            print('Please retry, if failed again, contact with the staff of GeneDock.\n')
        elif e.status // 100 == 4:
            print('Please check the workflow name/version/owner or template file.\n')
    except ValueError as e:
        _logger.warning('Failed to start task! error: {}'.format(e))
        print('Failed to start task!\nerror: {}'.format(e))
        print('Please check the input "workflow name" or "workflow version".\n')


def main():
    """
    加载配置文件，根据样本文件列表循环替换配置文件，每次替换完提交一个任务
    """
    workflow_template = gdpy.yml_utils.yaml_loader(TEMPLATE_FILE)

    for line in open(SAMPLE_LIST):
        if line.startswith('#'):
            continue
        line = line.strip()
        ele = line.split('\t') # tab分割

        # 根据样本文件列表中相应元素，替换配置文件中需根据样本信息变动的地方，即"{$##}"（此处需修改-4）
        workflow_param = str(workflow_template).replace("{$read}", ele[1])
        workflow_param = workflow_param.replace("{$sample}", ele[0])
        workflow_param = eval(workflow_param)

        workflow_param = gdpy.yml_utils.yaml_dumper(workflow_param)
        with open(TEMPLATE_FILE + '_tmp', 'w') as f:
            f.write(workflow_param.decode('utf-8'))

        active_workflow(auth)

        # 测试时，可以注释掉下方，取消删除临时文件，便于查看替换后的临时配置文件内容和查找错误原因。
        os.remove(TEMPLATE_FILE + '_tmp')

if __name__ == '__main__':
    main()
