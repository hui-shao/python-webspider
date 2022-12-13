### 猫耳FM音频下载

这并不能算是个爬虫，这只是个 json 解析、下载器，所以首先你得获取到 json：

（以下内容可能具有时效性）

点进用户主页，对查看所有音频的页面抓包。具体一点，抓取的 url 是 `https://app.missevan,com/person/get-user-sound`

抓包软件比如手机端 HttpCanary，需配合 LSPosed 模块 TrustMeAlready 解除 SSL Pining。

然后你就可以把获取到的 json 丢到 py 文件所在目录下，接着运行程序了。

json 文件示例：

```json
{
  "success": true,
  "code": 0,
  "info": {
    "Datas": [
      {
        "id": 5582287,
        "create_time": 1656010901,
        "duration": 966112,
        "user_id": 4979253,
        "username": "xxx",
        "downtimes": 11,
        "comment_count": 0,
        "soundurl_64": "https://sound-ks1-cdn-cn.maoercdn.com/aod/202206/24/_cfc7ed6f87d6248xxxxxx.m4a",
        "comments_count": 38,
        "sub_comments_count": 9,
        "uptimes": 134,
        "view_count": 22122,
        "point": 416,
        "pay_type": 0,
        "checked": 1,
        "soundstr": "【3D】标题",
        "cover_image": "202206/24/8cb492b2ce613b19414114225bf38930141.jpg",
        "intro": "<p>bgm：xxx 一些简介</p>",
        "download": 0,
        "soundurl": "https://sound-ks1-cdn-cn.maoercdn.com/aod/202206/24/_cfc7ed6f87d6248d626e13axxxxxx.m4a",
        "all_comments": 47,
        "comments_num": 47,
        "front_cover": "https://static.maoercdn.com/coversmini/202206/24/8cb492b2ce613b19e257406daf257ac5030141.jpg",
        "liked": 0,
        "collected": 0,
        "followed": 0,
        "authenticated": 0,
        "confirm": 0,
        "iconurl": "https://static.maoercdn.com/profile/icon01.png",
        "video": false,
        "need_pay": 0,
        "price": 0
      }
    ],
    "pagination": {
      "p": 2,
      "maxpage": 3,
      "count": 80,
      "pagesize": 30
    }
  }
}
```
