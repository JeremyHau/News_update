import feedparser
import json
from datetime import datetime
import os

def fetch_ai_agent_news():
    """抓取 AI Agent 相關新聞"""
    sources = [
    # 科技新聞聚合
    'https://news.ycombinator.com/rss',
    
    # Reddit 社群
    'https://www.reddit.com/r/MachineLearning/.rss',
    'https://www.reddit.com/r/artificial/.rss',
    'https://www.reddit.com/r/LocalLLaMA/.rss',
    
    # 學術論文
    'http://export.arxiv.org/rss/cs.AI',  # AI 論文
    'http://export.arxiv.org/rss/cs.CL',  # 計算語言學/NLP
    
    # 科技媒體
    'https://www.theverge.com/rss/index.xml',
    'https://techcrunch.com/feed/',
        
    # AI 公司官方博客
    'https://openai.com/blog/rss/',
    'https://www.anthropic.com/news/rss.xml',
    'https://blog.google/technology/ai/rss/',
    ]
    
    articles = []
    keywords = ['agent', 'ai agent', 'autonomous', 'llm']
    
    for source in sources:
        try:
            feed = feedparser.parse(source)
            for entry in feed.entries[:20]:
                title_lower = entry.title.lower()
                if any(keyword in title_lower for keyword in keywords):
                    articles.append({
                        'title': entry.title,
                        'link': entry.link,
                        'date': datetime.now().isoformat(),
                        'source': source
                    })
        except Exception as e:
            print(f"Error fetching {source}: {e}")
    
    articles = sorted(articles, key=lambda x: x['date'], reverse=True)[:30]
    
    os.makedirs('data', exist_ok=True)
    
    with open('data/articles.json', 'w', encoding='utf-8') as f:
        json.dump(articles, f, ensure_ascii=False, indent=2)
    
    print(f"Successfully fetched {len(articles)} articles")

if __name__ == '__main__':
    fetch_ai_agent_news()
