import feedparser
import json
from datetime import datetime
import os

def fetch_ai_agent_news():
    """抓取 AI Agent 相關新聞"""
    sources = [
        'https://news.ycombinator.com/rss',
        'https://www.reddit.com/r/MachineLearning/.rss',
    ]
    
    articles = []
    keywords = ['agent', 'ai agent', 'autonomous', 'llm']
    
    for source in sources:
        try:
            feed = feedparser.parse(source)
            for entry in feed.entries[:20]:  # 取前20條
                title_lower = entry.title.lower()
                # 關鍵詞過濾
                if any(keyword in title_lower for keyword in keywords):
                    articles.append({
                        'title': entry.title,
                        'link': entry.link,
                        'date': datetime.now().isoformat(),
                        'source': source
                    })
        except Exception as e:
            print(f"Error fetching {source}: {e}")
    
    # 按日期排序，取最新30條
    articles = sorted(articles, key=lambda x: x['date'], reverse=True)[:30]
    
    # 確保目錄存在
    os.makedirs('data', exist_ok=True)
    
    # 保存到 JSON
    with open('data/articles.json', 'w', encoding='utf-8') as f:
        json.dump(articles, f, ensure_ascii=False, indent=2)
    
    print(f"Successfully fetched {len(articles)} articles")

if __name__ == '__main__':
    fetch_ai_agent_news()
```

**requirements.txt**：
```
feedparser==6.0.10