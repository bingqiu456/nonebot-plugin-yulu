 # -*- coding: utf-8 -*-
import setuptools
setuptools.setup(
    name = "nonebot_plugin_yulu",
    version = "3.0",
    packages = setuptools.find_packages(),
    author="bingyue",
    author_email="hello-yiqiu@qq.com",
    description="""语录娱乐小插件""",
    url="https://github.com/bingqiu456/nonebot_plugin_yulu",
    install_requires=[
        "bs4>=0.0.1",
        "beautifulsoup4>=4.11.1",
        "nonebot2>=2.0.0b2",
        "nonebot-adapter-onebot>=2.0.0b1",
        "httpx==0.23.1"
    ],
    keywords=["nonebot_plugin_yulu","nonebot","nonebot_plugin"],
    package_data={
        'nonebot_plugin_yulu':['jitang.txt','yiyan.txt'],
    }
)
