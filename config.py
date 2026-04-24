"""
配置文件
定义新闻源和推送设置
"""

# RSS 新闻源配置
# AI中文 + AI英文 + 运维中文 + 运维英文
RSS_FEEDS = {
    # AI 领域 - 中文
    "AI_CN": [
        {
            "name": "机器之心",
            "url": "https://www.jiqizhixin.com/rss",
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
    # AI 领域 - 英文
    "AI_EN": [
        {
            "name": "OpenAI Blog",
            "url": "https://openai.com/blog/rss.xml",
        },
        {
            "name": "Anthropic",
            "url": "https://www.anthropic.com/feed.xml",
        },
        {
            "name": "Hugging Face",
            "url": "https://huggingface.co/blog/feed",
        },
        {
            "name": "DeepMind",
            "url": "https://deepmind.google/blog/rss/",
        },
        {
            "name": "MIT AI",
            "url": "https://news.mit.edu/rss/topic/artificial-intelligence",
        }
    ],
    # 运维/DevOps - 中文
    "OPS_CN": [
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
            "name": "酷壳",
            "url": "https://coolshell.cn/feed",
        }
    ],
    # 运维/DevOps - 英文
    "OPS_EN": [
        {
            "name": "DevOps.com",
            "url": "https://devops.com/feed/",
        },
        {
            "name": "GitHub Blog",
            "url": "https://github.blog/feed/",
        },
        {
            "name": "Docker Blog",
            "url": "https://www.docker.com/blog/feed/",
        },
        {
            "name": "Kubernetes Blog",
            "url": "https://kubernetes.io/feed.xml",
        },
        {
            "name": "CNCF Blog",
            "url": "https://www.cncf.io/feed/",
        }
    ]
}

# 获取最近 N 天内的新闻
DAYS_BACK = 1
