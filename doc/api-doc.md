目录

1\. 登陆/认证接口
---

**1\. 登陆/认证接口**
###### 接口功能
> 用于认证用户登陆，目前采用统一ldap认证

###### URL
> ads.test.com/api/v1/auth/

###### 支持格式
> JSON/x-www-form-urlencoded

###### HTTP请求方式
> POST

###### 请求参数
>
|参数|必选|类型|说明|
|:-----  |:-------|:-----|-----  |
|username    |true |string|用户名 |
|password    |true |string|用户密码|

###### 返回字段
>
|返回字段|字段类型|说明                              |
|:-----   |:------|:-----------------------------   |
|code   |int    |返回结果状态 2001：认证通过；5001：认证失败|
|token  |string | 认证通过获取token                      |
|msg |string |认证补充信息                         |

###### 接口示例
地址：ads.test.com/api/v1/auth/
``` javascript
{
    "username": "test",
    "password": "test",
}
```


2\. 部门信息增删改查接口
---

**1\. 获取部门信息接口**
###### 接口功能
> 获取部门信息

###### URL
> ads.test.com/api/v1/department/

###### 支持格式
> JSON/x-www-form-urlencoded

###### HTTP请求方式
> GET

###### 请求参数
>
|参数|必选|类型|说明|
|:-----  |:-------|:-----|-----  |
|limits    |false |int|限制返回数据条数 |
|token    |true |string|认证token|

###### 返回字段
>
|返回字段|字段类型|说明                              |
|:-----   |:------|:-----------------------------   |
|code   |int    |返回结果状态                      |
|data  |json |返回查询部门结果信息                |
|msg |string |认证补充信息                         |

###### 接口示例
地址：ads.test.com/api/v1/department/?limits=4&token=131c0ecc77db1a6894adbaf14ca97
``` javascript
{
    "msg": "success",
    "code": 2000,
    "data": [
        {
            "name": "北京-运维部",
            "tel": null,
            "desc": null,
            "update_time": "2018-06-27T10:43:30.861389+08:00"
        },
        {
            "name": "北京无线",
            "tel": "186120077",
            "desc": "北京无线支付部门",
            "update_time": "2018-06-27T10:47:17.665797+08:00"
        }
    ]
}
```
---

**2\. 添加部门信息接口**
###### 接口功能
> 添加部门信息接口

###### URL
> ads.test.com/api/v1/department/

###### 支持格式
> JSON/x-www-form-urlencoded

###### HTTP请求方式
> POST

###### 请求参数
>
|参数|必选|类型|说明|
|:-----  |:-------|:-----|-----  |
|name             |true  | string   |部门名称 |
|tel              |false | string   |部门联系电话|
|desc             |false | string  |部门简介|
|token            |true  | string  |认证token|
###### 返回字段
>
|返回字段|字段类型|说明                          |
|:-----   |:------|:-----------------------------|
|code   |int    |返回结果状态                     |
|data   |json   |返回增加部门结果信息              |
|msg    |string |返回增加补充信息                  |

###### 接口示例
地址：ads.test.com/api/v1/department/
``` javascript

{
	"name": "skynet",
	"desc": "skynet",
	"tel": "110"
	"token": "131c0ecc77db1a6894adbaf14ca97bed"
}
```

---

**3\. 修改部门信息接口**
###### 接口功能
> 修改部门信息接口

###### URL
> ads.test.com/api/v1/department/

###### 支持格式
> JSON/x-www-form-urlencoded

###### HTTP请求方式
> PUT

###### 请求参数
>
|参数|必选|类型|说明|
|:-----  |:-------|:-----|-----  |
|pk               |true  | int      |部门pk|
|name             |true  | string   |部门名称 |
|tel              |false | string   |部门联系电话|
|desc             |false | string  |部门简介|
|token            |true  | string  |认证token|
###### 返回字段
>
|返回字段|字段类型|说明                          |
|:-----   |:------|:-----------------------------|
|code   |int    |返回结果状态                     |
|data   |json   |返回增加部门结果信息              |
|msg    |string |返回增加补充信息                  |

###### 接口示例
地址：ads.test.com/api/v1/department/
``` javascript

{
    "pk": 1
	"name": "skynet",
	"desc": "skynet",
	"tel": "110"
	"token": "131c0ecc77db1a6894adbaf14ca97bed"
}
```

**4\. 删除部门信息接口**
###### 接口功能
> 删除部门信息接口

###### URL
> ads.test.com/api/v1/department/

###### 支持格式
> JSON/x-www-form-urlencoded

###### HTTP请求方式
> DELETE

###### 请求参数
>
|参数|必选|类型|说明|
|:-----  |:-------|:-----|-----  |
|pk               |true  | int      |部门pk|
|token            |true  | string  |认证token|
###### 返回字段
>
|返回字段|字段类型|说明                          |
|:-----   |:------|:-----------------------------|
|code   |int    |返回结果状态                     |
|data   |json   |返回增加部门结果信息              |
|msg    |string |返回增加补充信息                  |

###### 接口示例
地址：ads.test.com/api/v1/department/
``` javascript

{
    "pk": 1
	"token": "131c0ecc77db1a6894adbaf14ca97bed"
}
```
---