#!/usr/bin/env python

try:
  from setuptools import setup
except ImportError:
  from distutils.core import setup

setup(name='aliquant-client',
      version='1.0',
      description='AliQuant Client',
      author='inno-algo',
      packages=[
        'aliquant',
        'com',
        'com.aliyun',
        'com.aliyun.api',
        'com.aliyun.api.gateway',
        'com.aliyun.api.gateway.sdk',
        'com.aliyun.api.gateway.sdk.auth',
        'com.aliyun.api.gateway.sdk.common',
        'com.aliyun.api.gateway.sdk.http',
        'com.aliyun.api.gateway.sdk.util'
      ],
      install_requires=[
        "oss2"
      ]
)
