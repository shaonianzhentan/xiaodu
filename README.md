# xiaodu
小度音箱云云对接

[![hacs_badge](https://img.shields.io/badge/Home-Assistant-%23049cdb)](https://www.home-assistant.io/)
[![hacs_badge](https://img.shields.io/badge/HACS-Custom-41BDF5.svg)](https://github.com/hacs/integration)
![visit](https://visitor-badge.laobi.icu/badge?page_id=shaonianzhentan.xiaodu&left_text=visit)

## 安装方式

安装完成重启HA，刷新一下页面，在集成里搜索`xiaodu`即可

[![Add Integration](https://my.home-assistant.io/badges/config_flow_start.svg)](https://my.home-assistant.io/redirect/config_flow_start?domain=xiaodu)


小度-小米空气净化器模式控制

[![导入蓝图](https://my.home-assistant.io/badges/blueprint_import.svg)](https://my.home-assistant.io/redirect/blueprint_import/?blueprint_url=https%3A%2F%2Fgithub.com%2Fshaonianzhentan%2Fxiaodu%2Fblob%2Fmain%2Fblueprints%2Fxiaodu_fan.yaml)

小度-小米飞利浦灯泡色温模式控制

[![导入蓝图](https://my.home-assistant.io/badges/blueprint_import.svg)](https://my.home-assistant.io/redirect/blueprint_import/?blueprint_url=https%3A%2F%2Fgithub.com%2Fshaonianzhentan%2Fxiaodu%2Fblob%2Fmain%2Fblueprints%2Fxiaodu_philips_light.yaml)

## 小度自定义通用属性

```yaml
# 开关类型改为插座类型
xiaodu_type: SOCKET

# script模拟电视
xiaodu_name: 电视
xiaodu_domain: media_player

# sensor传感器
xiaodu_name: 温度传感器

xiaodu_name: 湿度传感器

# 摄像头（CAMERA、WEBCAM）
xiaodu_name: 摄像头
xiaodu_type: WEBCAM
xiaodu_domain: camera

# automation场景（打开、关闭）
xiaodu_name: 音乐模式
xiaodu_domain: scene

# automation场景（打开、关闭）
xiaodu_name: 音乐模式
xiaodu_domain: scene
```

> 小度开发相关文档

- [设备类型与模式表](https://dueros.baidu.com/didp/doc/dueros-bot-platform/dbp-smart-home/protocol/control-message_markdown#%E8%AE%BE%E5%A4%87%E7%B1%BB%E5%9E%8B%E4%B8%8E%E6%A8%A1%E5%BC%8F%E8%A1%A8)

## 相关问题

- 与智能音箱对接，域名必须为https。如果没有可联系我，提供HTTP转HTTPS代理服务
- 我的设备有限，所以支持不全，如有需要，可联系我添加

## 如果这个项目对你有帮助，请我喝杯<del style="font-size: 14px;">咖啡</del>奶茶吧😘
|  |支付宝|微信|
|---|---|---|
奶茶= | <img src="https://cdn.jsdelivr.net/gh/shaonianzhentan/ha-docs@master/docs/img/alipay.png" align="left" height="160" width="160" alt="支付宝" title="支付宝">  |  <img src="https://cdn.jsdelivr.net/gh/shaonianzhentan/ha-docs@master/docs/img/wechat.png" height="160" width="160" alt="微信支付" title="微信">

## 关注我的微信订阅号，了解更多HomeAssistant相关知识
<img src="https://cdn.jsdelivr.net/gh/shaonianzhentan/ha-docs@master/docs/img/wechat-channel.png" height="160" alt="HomeAssistant家庭助理" title="HomeAssistant家庭助理">

---
**在使用的过程之中，如果遇到无法解决的问题，付费咨询请加Q`635147515`**