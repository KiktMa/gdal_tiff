url = "https://www.wjx.cn/vm/Qz7I8zv.aspx#"
epochs = 18
# 题项比例，确保选项数量和数组长度一致
prob = {
    1: [43.49, 56.51],
    2: [2.7, 75.98, 14.63, 2.88, 3.81],
    3: [89.7, 8.7, 1.6],
    4: [32.5, 47.3, 10.5, 1.2, 8.5],
    5: [24.97, 60.22, 10.03, 3.41, 1.95],
    6: [20.24, 65.78, 10.39, 3.12, 2.47],
    7: [15.86, 60.28, 15.37, 7.41, 3.09],
    8: [15.78, 65.32, 15.20, 3.31, 2.19],
    9: [18.36, 62.59, 15.08, 3.23, 2.17],
    10: [22.10, 68.15, 15.39, 3.26, 2.22],
    11: [17.04, 65.68, 13.21, 3.19, 2.22],
    12: [25.28, 60.14, 10.36, 3.08, 1.95],
    13: [15.24, 64.67, 10.05, 3.24, 2.03],
    14: [29.88, 54.92, 10.11, 2.78, 2.31],
    15: [27.89, 60.19, 8.17, 2.42, 1.33],
    16: [24.97, 60.22, 10.03, 3.41, 1.95],
    17: [29.84, 54.95, 10.00, 3.38, 1.83],
    18: [26.93, 60.32, 9.97, 2.26, 0.85],
    19: [22.38, 64.62, 10.10, 1.92, 1.37],
    20: [20.84, 52.85, 21.10, 3.48, 1.93],
    21: [20.05, 65.67, 10.11, 3.16, 2.35],
    22: [17.04, 65.68, 13.21, 3.19, 2.22]
}
# 简答题题库
answerList = {
    23: ["无", "增加互动游戏和趣味挑战", "提供多样化的表演和演出", "无", "提供免费WiFi方便游客分享体验", "提供特色民俗表演和体验", "加强卫生和清洁工作确保环境整洁", "推出限定纪念品和邮票",]
}
# IP API提取链接 https://xip.ipzan.com/ 这个每周都有几百个免费的IP代理领取
api = "https://service.ipzan.com/core-extract?num=1&no=20240422330794094885&minute=1&format=txt&area=510000&pool=quality&secret=lfngq7jnjri8mso"
# User-Agent库
UA = ["Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36 Edg/121.0.0.0",
      "Mozilla/5.0 (Linux; Android 10; SEA-AL10 Build/HUAWEISEA-AL10; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/86.0.4240.99 XWEB/4313 MMWEBSDK/20220805 Mobile Safari/537.36 MMWEBID/9538 MicroMessenger/8.0.27.2220(0x28001B53) WeChat/arm64 Weixin NetType/WIFI Language/zh_CN ABI/arm64",
      "Mozilla/5.0 (Linux; Android 11; Redmi Note 8 Pro Build/RP1A.200720.011; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/89.0.4389.72 MQQBrowser/6.2 TBS/045913 Mobile Safari/537.36 V1_AND_SQ_8.8.68_2538_YYB_D A_8086800 QQ/8.8.68.7265 NetType/WIFI WebP/0.3.0 Pixel/1080 StatusBarHeight/76 SimpleUISwitch/1 QQTheme/2971 InMagicWin/0 StudyMode/0 CurrentMode/1 CurrentFontScale/1.0 GlobalDensityScale/0.9818182 AppId/537112567 Edg/98.0.4758.102",
      ]