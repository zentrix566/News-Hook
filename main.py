#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
News-Hook
每日抓取 AI 和运维新闻，推送到飞书
"""

import os
import time
import feedparser
from datetime import datetime, timedelta
from typing import List, Dict
import requests
from dotenv import load_dotenv

from config import RSS_FEEDS, DAYS_BACK


class NewsFetcher:
    """新闻抓取器"""

    @staticmethod
    def get_recent_news(feed_config: Dict) -> List[Dict]:
        """获取最近 N 天的新闻"""
        try:
            feed = feedparser.parse(feed_config["url"])
        except Exception as e:
            print(f"获取 {feed_config['name']} 失败: {e}")
            return []

        recent_news = []
        cutoff_date = datetime.now() - timedelta(days=DAYS_BACK)

        for entry in feed.entries:
            published_parsed = entry.get('published_parsed', entry.get('updated_parsed'))
            if not published_parsed:
                continue

            entry_date = datetime(*published_parsed[:6])
            if entry_date >= cutoff_date:
                recent_news.append({
                    "title": entry.title,
                    "link": entry.link,
                    "published": entry_date.strftime("%Y-%m-%d %H:%M"),
                    "source": feed_config["name"]
                })

        return recent_news

    @staticmethod
    def fetch_all_news() -> Dict[str, List[Dict]]:
        """获取所有分类的新闻"""
        result = {}
        for category, feeds in RSS_FEEDS.items():
            all_news = []
            for feed in feeds:
                news = NewsFetcher.get_recent_news(feed)
                all_news.extend(news)
            # 按时间倒序排序
            all_news.sort(key=lambda x: x["published"], reverse=True)
            result[category] = all_news
        return result


class FeishuPusher:
    """飞书推送器"""

    def __init__(self, webhook_url: str):
        self.webhook_url = webhook_url

    def format_message(self, news_by_category: Dict[str, List[Dict]]) -> Dict:
        """将新闻格式化为飞书富文本消息"""
        category_names = {
            "AI": "🤖 AI 最新资讯",
            "OPS": "🔧 运维/DevOps 资讯"
        }

        elements = []

        # 添加标题
        elements.append({
            "tag": "text",
            "text": f"📰 每日新闻推送 - {datetime.now().strftime('%Y年%m月%d日')}\n\n",
        })

        for category, news_list in news_by_category.items():
            if not news_list:
                continue

            elements.append({
                "tag": "text",
                "text": f"{category_names[category]}\n",
            })

            for i, news in enumerate(news_list, 1):
                elements.append({
                    "tag": "text",
                    "text": f"{i}. ",
                })
                elements.append({
                    "tag": "a",
                    "text": news["title"],
                    "href": news["link"],
                })
                elements.append({
                    "tag": "text",
                    "text": f"  ({news['source']})\n",
                })

            elements.append({
                "tag": "text",
                "text": "\n",
            })

        total_count = sum(len(news) for news in news_by_category.values())
        if total_count == 0:
            elements.append({
                "tag": "text",
                "text": "😴 最近两天没有新资讯",
            })

        return {
            "msg_type": "interactive",
            "card": {
                "config": {
                    "wide_screen_mode": True
                },
                "elements": [
                    {
                        "tag": "div",
                        "text": {
                            "content": "".join([e["text"] for e in elements]),
                            "tag": "lark_md"
                        }
                    }
                ]
            }
        }

    def push(self, news_by_category: Dict[str, List[Dict]]) -> bool:
        """推送到飞书"""
        if not self.webhook_url:
            print("错误: 未配置飞书 Webhook URL")
            return False

        message = self.format_message(news_by_category)

        try:
            response = requests.post(
                self.webhook_url,
                json=message,
                timeout=10
            )
            response.raise_for_status()
            result = response.json()

            if result.get("code") == 0:
                print(f"推送成功，共 {sum(len(n) for n in news_by_category.values())} 条新闻")
                return True
            else:
                print(f"推送失败: {result}")
                return False
        except Exception as e:
            print(f"推送异常: {e}")
            return False


def main():
    """主函数"""
    # 加载环境变量
    load_dotenv()

    webhook_url = os.getenv("FEISHU_INFORMATION_WEBHOOK")
    if not webhook_url:
        print("错误: 环境变量 FEISHU_INFORMATION_WEBHOOK 未设置")
        exit(1)

    print("开始抓取新闻...")
    fetcher = NewsFetcher()
    news = fetcher.fetch_all_news()

    total = sum(len(n) for n in news.values())
    print(f"抓取完成，共 {total} 条近期新闻")

    print("正在推送到飞书...")
    pusher = FeishuPusher(webhook_url)
    success = pusher.push(news)

    exit(0 if success else 1)


if __name__ == "__main__":
    main()
