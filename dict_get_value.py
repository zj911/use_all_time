更新： 增加字典中包含列表的查询，即{'streams':[{'name':"jack"}]}
def dict_get(dict1, objkey, default):
    tmp = dict1
    for k,v in tmp.items():
        if k == objkey:
            return v
        else:
            if type(v) is dict:
                ret = dict_get(v, objkey, default)
                if ret is not default:
                    return ret
            if type(v) is list:
                ret = dict_get(v[0], objkey, default)
                if ret is not default:
                    return ret
    return default



import types
 
#获取字典中的objkey对应的值，适用于字典嵌套
#dict:字典
#objkey:目标key
#default:找不到时返回的默认值
def dict_get(dict1, objkey, default):
  tmp = dict1
  for k,v in tmp.items():
    if k == objkey:
      return v
    else:
      if type(v) is dict:
        ret = dict_get(v, objkey, default)
        if ret is not default:
          return ret
  return default
 
#如
dicttest={"result":{"code":"110002","msg":"设备设备序列号或验证码错误"}}
ret=dict_get(dicttest, 'msg', None)
print(ret)