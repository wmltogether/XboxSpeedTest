# XboxSpeedTest
Simple &amp; Fast SpeedTester for Xbox Download CDN

Xbox下载CDN优选

## 介绍

中国的Xbox玩家越来越难混下去了，微软把国内的CDN中非国行游戏下载资源给做了下架，这真是国行的悲剧。很多DNS返回的节点不是Edgecast的污染节点就是Akamai的龟速节点，为了高速下载我们只能不择手段，这个CDN优选工具就是来临时解决这个状况。

Xbox（包括PC版）游戏下载的国际通用域名是

```
assets1.xboxlive.com
assets2.xboxlive.com
dlassets.xboxlive.com
```

中国Xbox游戏下载的域名则是

```
assets1.xboxlive.cn
assets2.xboxlive.cn
dlassets.xboxlive.cn
```

根据我的实践，**他们是不通用的**，没错，不要把他们混用！不要像某DNS一样把.com的域名302到.cn上，这样很多游戏会下载暂停或者锁到100KB/s！冷门游戏和大部分360游戏依然是龟速的。看了一些大佬的帖子，目前最好的方案是根据个人的网络环境在本地重新测速指派CDN。

## 实践

从某个全球多地PING的网站上，我们获取了xbox全球海外服务器的IP（不包括国内，因为国内的CDN镜像是有问题的），利用模拟http下载的方式，返回结果进行排序，最后写入到本地的域名解析上（可以是路由的DNSMASQ，可以是smartdns，如果你只用PC版，直接写入hosts）



工具原料：

1.Windows & Python 2.7（不是python3）

2.一台能刷写（LEDE，梅林，padavan）等第三方系统的路由器

3.DNSMASQ 或者SMARTDNS


我们写了一个简易的脚本来快速完成地址筛选测速的结果。

打开```./configs/cdn.list```把XBOX下载服务器的IP列表添加进去。这里我已经预先放好了，如果你找到了更好的列表，可以自行修改。

在cmd下运行XboxSpeedTest.py，等待十分钟，优选测速完毕后会提示最佳服务器，并写入结果。

```
python XboxSpeedTest.py
```
康康结果：
```
[LOG]All CDN Test complete. Have fun!
[LOG]Your Best CDN is 203.69.138.26, 7388KB/s!
```

结果 hosts_best_output.txt 对应hosts，dnsmasq_best_output.txt 对应dnsmasq，smartdns_best_output.txt对应smartdns，把以上结果复制到路由或者hosts中，重启xbox试试下载吧。

