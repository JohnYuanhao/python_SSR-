import requests
import re
import base64


proxies = {
    "http": "127.0.0.1:1080",
    "https": "127.0.0.1:1080"
}

html = requests.get("https://shadowsocksr.ru/")#, proxies=proxies)

# 设置编码规则
html.encoding = "utf-8"
# print(html.text)

# 设置正则规则
pattern = re.compile('ssr:\/\/[\d\w=^_]*(?=\")')

# 找到所有目标并返回数组
result = pattern.findall(html.text)


# 去除数组重复
def dropDuplicate(arr):
    dic = {}
    ptr = 0
    while True:
        if ptr >= len(arr):
            break
        if arr[ptr] in dic:
            arr.pop(ptr)
            ptr -= 1
        else:
            dic[arr[ptr]] = 1
        ptr += 1

# 编码
def urlsafe_b64encode(str):
    data=base64.urlsafe_b64encode(str).decode('utf-8')
    data=data.replace("+","-").replace("/","_").replace("=","")
    return data

# 解码
def urlsafe_b64decode(str):
    data=str.replace("-","+").replace("_","/")
    num=len(data)%4
    if num:
        data=data.ljust(num+len(data),"=")
    data=base64.urlsafe_b64decode(data)
    return data.decode('utf-8')


if __name__ == "__main__":
    dropDuplicate(result)
    result.insert(0,"ssr://MTI3LjAuMC4xOjEwODA6b3JpZ2luOm5vbmU6cGxhaW46TUEvP29iZnNwYXJhbT0mcmVtYXJrcz01cHlzNTd1RTVweU41WXFoNVptbzVwMmw1cnFRTFhOb1lXUnZkM052WTJ0emNpNXlkUSZncm91cD1RRk5vWVdSdmQxX2x2YkU2TWc")

def changeSsr(str):
    str=urlsafe_b64decode(str.replace("ssr://",""))
    if re.search("group=[\d\w]*(?=&)?",str):
        str=re.sub("group=[\d\w]*(?=&)?","group=QFNoYWRvd1_lvbE6Mg",str)
    else:
        if re.search("\/\?",str):
            str+="&group=QFNoYWRvd1_lvbE6Mg"
        else:
            str+="/?group=QFNoYWRvd1_lvbE6Mg"
    str=str.encode(encoding='utf-8')
    return "ssr://"+urlsafe_b64encode(str)


# 转换list内每一个元素
result=[changeSsr(i) for i in result]
result.insert(0,"MAX=99\r")
result="\n".join(result)
print(result)
#sys.stdout.flush() #不启用缓存


# # 添加说明信息
# result.insert(0,"ssr://MTI3LjAuMC4xOjEwODA6b3JpZ2luOm5vbmU6cGxhaW46TUEvP29iZnNwYXJhbT0mcmVtYXJrcz01cHlzNTd1RTVweU41WXFoNVptbzVwMmw1cnFRTFhOb1lXUnZkM052WTJ0emNpNXlkUSZncm91cD1RRk5vWVdSdmQxX2x2YkU2TWc")
# result.insert(0,"MAX=99\r")
# # result = [x + "\n" for x in result]
# result="\n".join(result)
