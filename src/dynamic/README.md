# PoliGuard-Crawler

## 简介

项目名为`PoliGuard-Crawler`，通过对人类行为进行模拟来触发小程序中的各种功能等，并对小程序页面进行动态的解析，以达到UI自动化测试的目的。可以单独使用来动态获取小程序意思政策、页面转移图等信息。

也可以做为PoliGuard的子模块，为项目整体提供自动点击等能力。

## 原理

### 隐私政策的获取

首先根据“隐私政策”设定引导词，例如：“隐私”、“政策”、“协议”等。在每一次小程序页面发生变动后，通过CV，与页面解析，在页面中搜索引导词来指引我们的点击搜索，如果没有相关内容便进行页面回溯，继续寻找。最后综合页面上字数与引导词匹配状态等信息判断当前页面是不是隐私政策。如果是的话，通过页面解析，链接分析，OCR识别等方法获取隐私政策。

### 页面转移图的获取

由于微信小程序是通过xweb引擎渲染的，所有我们可以通过webview对小程序的页面进行解析。解析小程序界面之后，查找所有的跳转标签，我们对其进行触发，然后达到页面遍历的目的。

### 自动点击能力

使用Appium框架对人的行为进行模拟点击。
