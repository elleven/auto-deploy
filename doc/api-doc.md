目录
> 符合标准的django-rest-framework 接口风格；
> version : v1

一\. 登陆/认证接口
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
|:-----|:-------|:-----|-----|
|username    |true |string|用户名 |
|password    |true |string|用户密码|

###### 返回字段
>
|返回字段|字段类型|说明|
|-----|:------|:-----------------------------|
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


二\. 部门信息增删改查接口
---

**1\. 获取部门信息接口**
###### 接口功能
> 获取部门信息

###### URL
> ads.test.com/api/v1/department/?P<pk>\d+/?token=xxxx

###### 支持格式
> JSON/x-www-form-urlencoded

###### HTTP请求方式
> GET

###### 请求参数
>
|参数|必选|类型|说明|
|:-----  |:-------|:-----|-----  |
|token    |true |string|认证token|

###### 返回字段
>
|返回字段|字段类型|说明                              |
|:-----   |:------|:-----------------------------   |
|status   |int    |返回结果状态                      |
|data  |json |返回查询部门结果信息                |                        |

###### 接口示例
地址：172.28.1.105:8000/api/v1/department/2/?token=27208c4dae42eae5699a058da5c5d6d6
``` javascript
{
    "pk": 2,
    "name": "北京大数据",
    "tel": "222",
    "desc": "this human is too lazy to write it ",
    "update_time": "2018-07-20T15:09:49.541065+08:00"
}
```
---

**2\. 创建部门信息接口**
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
|status   |int    |返回结果状态                     |
|data   |json   |返回增加部门结果信息              |                |

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
|status   |int    |返回结果状态                     |
|data   |json   |返回增加部门结果信息              |

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
|status   |int    |返回结果状态                     |
|data   |json   |返回增加部门结果信息              |

###### 接口示例
地址：ads.test.com/api/v1/department/
``` javascript

{
    "pk": 1
	"token": "131c0ecc77db1a6894adbaf14ca97bed"
}
```

三\. 用户信息只读查询接口
---


**1\. 用户信息查询接口**
###### 接口功能
> 查询用户信息（只读）

###### URL
> ads.test.com/api/v1/user/(?P<pk>/d+)

###### 支持格式
> JSON/x-www-form-urlencoded

###### HTTP请求方式
> GET

###### 请求参数
>
|参数|必选|类型|说明|
|:-----  |:-------|:-----|-----  |
|pk               |false  | int      |pk|
|token            |true  | string  |认证token|
###### 返回字段
>
|返回字段|字段类型|说明                          |
|:-----   |:------|:-----------------------------|
|status   |int    |返回结果状态                     |
|data   |json   |返回用户信息              |

###### 接口示例
地址：ads.test.com/api/v1/user/
``` javascript
[
    {
        "username": "test",
        "tel": null,
        "email": "test@test.com",
        "department": {
            "id": 1,
            "name": "北京-运维部",
            "tel": null,
            "desc": null,
            "create_time": "2018-07-20T15:04:31.883458+08:00",
            "update_time": "2018-07-20T15:04:31.883090+08:00"
        }
    }
]
```

四\. 服务元数据信息增删改查接口
---

**1\. 服务元数据信息查询**
###### 接口功能
> 查询服务相关信息

###### URL
> ads.test.com/api/v1/service/(?P<pk>/d+)

###### 支持格式
> JSON/x-www-form-urlencoded

###### HTTP请求方式
> GET

###### 请求参数
>
|参数|必选|类型|说明|
|:-----  |:-------|:-----|-----  |
|pk               |false  | int      |pk|
|token            |true  | string  |认证token|
###### 返回字段
>
|返回字段|字段类型|说明                          |
|:-----   |:------|:-----------------------------|
|status   |int    |返回结果状态                     |
|data   |json   |返回用户信息              |

###### 接口示例
地址：ads.test.com/api/v1/service/1/?token=27208c4dae42eae5699a058da5c5d6d6
``` javascript
{
    "id": 1,
    "is_lock": false,
    "users": [
        "test"
    ],
    "name": "test",
    "address": "test",
    "language": 3,
    "program_path": "test",
    "loom_id": "test",
    "service_type": 1,
    "port": null,
    "desc": "test",
    "pre_version_count": 0,
    "test_version_count": 0,
    "pro_version_count": 0,
    "update_time": "2018-07-20T16:13:02.987913+08:00",
    "department": {
        "id": 2,
        "name": "北京大数据",
        "tel": "222",
        "desc": "this human is too lazy to write it ",
        "create_time": "2018-07-20T15:09:49.541832+08:00",
        "update_time": "2018-07-20T15:09:49.541065+08:00"
    }
}
```

**2\. 创建新服务/修改服务**
###### 接口功能
> 创建新的服务

###### URL
> ads.test.com/api/v1/service/(?P<pk>/d+)/

###### 支持格式
> JSON/x-www-form-urlencoded

###### HTTP请求方式
> POST/PUT

###### 请求参数
>
|参数|必选|类型|说明|
|:-----  |:-------|:-----|-----  |
|name              |True  | string      |服务名字|
|loom_id           |True  | string      |服务注册名字|
|address             |True  | string      |git地址|
|program_path              |True  | string      |项目路径|
|service_type              |True  | int      |服务类型|
|language              |True  | int      |服务语言类型|
|department_id              |True  | string      |部门名称|
|user_id              |True  | list      |服务归属作者|
|token            |true  | string  |认证token|
###### 返回字段
>
|返回字段|字段类型|说明                          |
|:-----   |:------|:-----------------------------|
|status   |int    |返回结果状态                     |
|data   |json   |返回服务信息              |

###### 接口示例
地址：172.28.1.105:8000/api/v1/service/?token=27208c4dae42eae5699a058da5c5d6d6
``` javascript
{
	"name":"test",
	"loom_id":"test",
	"department_id":"北京大数据",
	"program_path":"test",
	"address":"test",
	"service_type":1,
	"language":3,
	"desc":"test",
	"user_id":["test"]
}
```

**3\. 删除服务**
###### 接口功能
> 删除服务(删除服务时候，顺序 先删除附属配置信息，在删除服务信息)

###### URL
> ads.test.com/api/v1/service/(?P<pk>/d+)/

###### 支持格式
> JSON/x-www-form-urlencoded

###### HTTP请求方式
> DELETE

###### 请求参数
>
|参数|必选|类型|说明|
|:-----  |:-------|:-----|-----  |
|pk              |True  | int     |pk|
|token            |true  | string  |认证token|
###### 返回字段
>
|返回字段|字段类型|说明                          |
|:-----   |:------|:-----------------------------|
|status   |int    |返回结果状态                     |
|data   |json   |返回服务信息              |

###### 接口示例
地址：172.28.1.105:8000/api/v1/service/1/?token=27208c4dae42eae5699a058da5c5d6d6
``` javascript

```
