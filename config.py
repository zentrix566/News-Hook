"""
配置文件
定义新闻源和推送设置
"""

# RSS 新闻源配置
# AI 相关新闻源 + 运维/DevOps 相关新闻源（中文）
RSS_FEEDS = {
    # AI 领域新闻（中文）
    "AI": [
        {
            "name": "机器之心",
            "url": "https://www.jiqizhixin.com/rss",
        },
        {
            "name": "AI科技评论",
            "url": "https://www.jiqinews.cn/feed",
        },
        {
            "name": "量子位",
            "url": "https://www.qbitai.com/feed",
        },
        {
            "name": "雷锋网",
            "url": "https://www.leiphone.com/feed",
        },
        {
            "name": "InfoQ AI",
            "url": "https://www.infoq.cn/topic/ai.xml",
        }
    ],
    # 运维/DevOps 领域新闻（中文）
    "OPS": [
        {
            "name": "InfoQ 架构",
            "url": "https://www.infoq.cn/topic/architecture.xml",
        },
        {
            "name": "开源中国",
            "url": "https://www.oschina.net/news/rss",
        },
        {
            "name": "Linux 中国",
            "url": "https://linux.cn/rss.xml",
        },
        {
            "name": "云原生社区",
            "url": "https://cloudnative.to/feed.xml",
        },
        {
            "name": "Go 语言中文网",
            "url": "https://studygolang.com/feed",
        },
        {
            "name": "酷壳",
            "url": "https://coolshell.cn/feed",
        }
    ]
}

# 获取最近 N 天内的新闻
DAYS_BACK = 2
