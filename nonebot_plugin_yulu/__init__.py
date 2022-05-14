from ast import For
from email import header
import imp
from bs4 import BeautifulSoup
import random,httpx,asyncio,os,datetime,time
from re import A, RegexFlag
from nonebot import on_command,on_regex
from nonebot.adapters.onebot.v11 import Message, MessageSegment,event,Event,Bot,GroupMessageEvent
from nonebot.params import RegexMatched,RegexGroup,RegexDict,ArgPlainText,CommandArg,Arg
from nonebot.matcher import Matcher
from hashlib import md5
import re,os
from nonebot import get_driver,logger

chu = get_driver().config.dict()
on_group = chu.get('yulu_on_group',[])
if on_group == []:
    logger.warning('yulu:未配置开启群号 默认[]')


mulu = on_command('菜单')
@mulu.handle()
async def mulu_handle(event:GroupMessageEvent):
    enjoy = ['🍏','🍎','🍐','🍊','🍋']
    a = random.randint(0,len(enjoy)-1)
    if str (event.group_id) in on_group:
        await mulu.finish(f'     {enjoy[a]}小月豪华版{enjoy[a]}\n     {enjoy[a]}一言  鸡汤{enjoy[a]}\n   {enjoy[a]}翻译 应用查询{enjoy[a]}\n{enjoy[a]}国内新闻 每日一图{enjoy[a]}\n———————————\n🔧PS:发送指令即可查看🔧\n🔧例如:/一言🔧')




async def fanyi(msg):
    try:
        lts  =  int(time.time() * 1000)
        salt = str(lts) +str(random.randint(0,9))
        sign = md5(("fanyideskweb" + msg + str(salt) + "Ygy_4c=r#e#4EX^NUGUc5").encode()).hexdigest()
        header =   {'Content-Type':'application/x-www-form-urlencoded; charset=UTF-8',
    'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/101.0.4951.64 Safari/537.36',
    'Referer': 'https://fanyi.youdao.com/',
    'Cookie': 'OUTFOX_SEARCH_USER_ID=-807799036@10.110.96.159; OUTFOX_SEARCH_USER_ID_NCOO=659977799.288254; JSESSIONID=aaaAQ7LuqvrpF7puSFWcy; fanyi-ad-id=305838; fanyi-ad-closed=1; ___rl__test__cookies=1652228559425/',
    }
        post_data = f'i={msg}&from=zh-CHS&to=en&smartresult=dict&client=fanyideskweb&salt={salt}&sign={sign}&lts={lts}&bv=579f97fa966a5b4ed6b4eaabfc7637e8&doctype=json&version=2.1&keyfrom=fanyi.web&action=FY_BY_REALTlME'
        r = await httpx.AsyncClient().post(url='https://fanyi.youdao.com/translate_o?smartresult=dict&smartresult=rule',data=post_data,headers=header)
        p = r.json()    
    except (httpx.NetworkError,KeyError,httpx.ConnectError):
        return '查询失败'
    else:
        return f'原文:{p["translateResult"][0][0]["src"]}\n翻译:{p["translateResult"][0][0]["tgt"]}'

async def yingy(msg,n):
    try:
        header = {'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/101.0.4951.64 Safari/537.36'}
        u = await httpx.AsyncClient().get(url='https://mobile.baidu.com/api/appsearch?word='+str(msg)+'&v=undefined&sid=undefined',headers=header)
        u = u.json()
    except (httpx.NetworkError,KeyError,httpx.ConnectError):
            return '网络请求失败'
    else:
        b = [f'你搜索的内容是{msg}\n']
        if n is None:
            for i in range(len(u["data"]["data"])):
                a = i + 1
                b.append(str(a)+","+u["data"]["data"][i]["sname"]+"\n")

            b.append(f'一共为你找到{len(b)-1}个应用\n请发送序号')

            return b

        else:
            na = u["data"]["data"][n-1]["icon"] 
            return f'应用名字:{u["data"]["data"][n-1]["sname"]}\n应用大小:{u["data"]["data"][n-1]["size"]}\n应用下载链接:{u["data"]["data"][n-1]["download_inner"]}\n'\
                f'应用类型:{u["data"]["data"][n-1]["catename"]}\n应用下载量:{u["data"]["data"][n-1]["strDownload"]}\n应用图标:'+MessageSegment.image(na.replace('//','https://'))
        
async def news ():
    try:
        head = {"User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/101.0.4951.64 Safari/537.36",
        "Content-Type":"text/html"
        }
        r = httpx.get(url='http://www.people.com.cn/GB/59476/index.html',headers=head)
    except(httpx.NetworkError,KeyError,httpx.ConnectError):
        return '获取失败 请检查网络'
    else:
        soup = BeautifulSoup(r.text, 'html.parser')
        a = soup.find_all(target="_blank")
        o= ['————今日新闻————']
        for i in range(27):
            if i>15 :
                o.append("\n" + str(BeautifulSoup(str(a[i]),'html.parser').get_text()))

        return o





xinwen = on_command('国内新闻')
@xinwen.handle()
async def _(event:GroupMessageEvent):
    if str (event.group_id) in on_group:
        await xinwen.finish(await news())

bing = on_command('每日一图')
@bing.handle()
async def bing_image_handle(event:GroupMessageEvent):
    try:
        headinfos = {'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/101.0.4951.64 Safari/537.36',
             }
        bing_json = httpx.get( url='https://bing.com/HPImageArchive.aspx?format=js&idx=0&n=1',headers=headinfos )
        print(bing_json.text)
        b = bing_json.json()
        if str (event.group_id) in on_group:
            await bing.finish(MessageSegment.image("https://bing.com"+b["images"][0]["url"]))
    except (httpx.NetworkError, httpx.HTTPStatusError, KeyError):
        await bing.finish('网络连接失败')

yy = on_command('应用查询')
@yy.handle()
async def yy_handle(o:GroupMessageEvent, event:Event,f: Message = CommandArg()):
    if str (o.group_id) in on_group:
        await yy.send(await yingy(msg=f,n=None))
        global xxx
        xxx = {"xxxx":"xxxx"}
        xxx[event.get_user_id()] = event.get_plaintext().replace("/应用查询","").replace(" ","")
    

@yy.got("yingy")
async def yy_got(o:GroupMessageEvent,event:Event,a: str = ArgPlainText("yingy")):
    b = xxx[event.get_user_id()]
    try:
       a =  await yingy(msg=str(b),n=int(a))
    except(IndexError,ValueError):
        await  yy.finish()
    else:
        if str (o.group_id) in on_group:
            await yy.finish(a)


fy = on_regex('/翻译(\w+)')
@fy.handle()
async def fy_http(event:GroupMessageEvent,foo : str = RegexMatched()):
    if str (event.group_id) in on_group:
        a = re.match(r'^/翻译\s*(\w+)\s*$', foo)
        await fy.finish(await fanyi(a.group(1)))



yiyan = on_command('一言')
@yiyan.handle()
async def _(event:GroupMessageEvent):
    try:
        with open(str(os.path.dirname(__file__))+'/yiyan.txt','r',encoding='utf-8') as f:
            a = f.readlines()
            b = random.randint(0,len(a))
    except FileNotFoundError:
        await jitang.finish()
    else:
        
        if str (event.group_id) in on_group:
            await jitang.finish(a[b].strip('\n'))
    

jitang = on_command('鸡汤')
@jitang.handle()
async def jitang_handle(event:GroupMessageEvent):
    try:
        with open(str(os.path.dirname(__file__))+'/jitang.txt','r',encoding='utf-8') as f:
            a = f.readlines()
            b = random.randint(0,len(a))
    except FileNotFoundError:
        await jitang.finish()
    else:
        if str (event.group_id) in on_group:
            await jitang.finish(a[b].strip('\n'))