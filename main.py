#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
News-Hook
每日抓取各类新闻，分多次推送到飞书
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
        self.category_names = {
            "AI_CN": "🤖 AI 资讯 - 中文",
            "AI_EN": "🤖 AI 资讯 - 英文",
            "OPS_CN": "🔧 运维/DevOps - 中文",
            "OPS_EN": "🔧 运维/DevOps - 英文",
            "WORLD_EN": "🌍 国际新闻 - 英文",
            "CHINA_CN": "🇨🇳 国内新闻 - 中文"
        }

    def format_message(self, category: str, news_list: List[Dict]) -> Dict:
        """将单个分类的新闻格式化为飞书消息"""
        category_name = self.category_names.get(category, category)

        content = f"📰 每日新闻推送 - {datetime.now().strftime('%Y年%m月%d日')}\n\n"
        content += f"**{category_name}**\n\n"

        if not news_list:
            content += "😴 今天没有新资讯"
        else:
            for i, news in enumerate(news_list, 1):
                content += f"{i}. [{news['title']}]({news['link']})  ({news['source']})\n"

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
                            "content": content,
                            "tag": "lark_md"
                        }
                    }
                ]
            }
        }

    def push_single(self, category: str, news_list: List[Dict]) -> bool:
        """推送单个分类"""
        if not self.webhook_url:
            print("错误: 未配置飞书 Webhook URL")
            return False

        message = self.format_message(category, news_list)

        try:
            response = requests.post(
                self.webhook_url,
                json=message,
                timeout=10
            )
            response.raise_for_status()
            result = response.json()

            if result.get("code") == 0:
                print(f"[{self.category_names[category]}] 推送成功，{len(news_list)} 条新闻")
                return True
            else:
                print(f"[{self.category_names[category]}] 推送失败: {result}")
                return False
        except Exception as e:
            print(f"[{self.category_names[category]}] 推送异常: {e}")
            return False

    def push_all(self, news_by_category: Dict[str, List[Dict]]) -> int:
        """分多次推送所有分类，每个分类单独一条消息"""
        success_count = 0
        for category, news_list in news_by_category.items():
            if news_list:  # 只推送有新闻的分类
                if self.push_single(category, news_list):
                    success_count += 1
                time.sleep(1)  # 间隔一下，避免请求过快
            else:
                print(f"[{self.category_names[category]}] 无新闻，跳过")
        return success_count


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

    print("开始分批次推送到飞书...\n")
    pusher = FeishuPusher(webhook_url)
    success_count = pusher.push_all(news)

    total_categories = sum(1 for n in news.values() if len(n) > 0)
    print(f"\n推送完成: {success_count}/{total_categories} 个分类成功")

    exit(0 if success_count == total_categories else 1)


if __name__ == "__main__":
    main()
