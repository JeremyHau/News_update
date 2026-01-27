import feedparser
import json
from datetime import datetime
import os

def load_config():
    """Load configuration from config.json"""
    try:
        with open('config.json', 'r', encoding='utf-8') as f:
            return json.load(f)
    except Exception as e:
        print(f"Error loading config: {e}")
        return {"categories": [], "keywords": []}

def fetch_articles():
    """Fetch articles from all enabled sources"""
    config = load_config()
    categories = config.get('categories', [])
    keywords = config.get('keywords', ['ai', 'agent', 'llm'])
    
    all_articles = []
    
    for category in categories:
        category_id = category.get('id')
        category_name = category.get('name')
        sources = category.get('sources', [])
        
        for source in sources:
            if not source.get('enabled', True):
                continue
                
            source_id = source.get('id')
            source_name = source.get('name')
            source_url = source.get('url')
            
            print(f"Fetching from {source_name} ({source_url})...")
            
            try:
                feed = feedparser.parse(source_url)
                
                for entry in feed.entries[:20]:  # Get top 20 entries
                    title = entry.get('title', 'No title')
                    link = entry.get('link', '')
                    
                    # Filter by keywords (case-insensitive)
                    title_lower = title.lower()
                    if any(keyword.lower() in title_lower for keyword in keywords):
                        # Get published date
                        pub_date = entry.get('published_parsed') or entry.get('updated_parsed')
                        if pub_date:
                            date_str = datetime(*pub_date[:6]).isoformat()
                        else:
                            date_str = datetime.now().isoformat()
                        
                        article = {
                            'id': hash(link),  # Use link hash as unique ID
                            'title': title,
                            'link': link,
                            'source': source_name,
                            'category': category_id,
                            'date': date_str,
                            'saved': False
                        }
                        
                        all_articles.append(article)
                        
                print(f"  Found {len([a for a in all_articles if a['source'] == source_name])} articles")
                
            except Exception as e:
                print(f"  Error fetching {source_name}: {e}")
    
    # Remove duplicates based on link
    seen_links = set()
    unique_articles = []
    for article in all_articles:
        if article['link'] not in seen_links:
            seen_links.add(article['link'])
            unique_articles.append(article)
    
    # Sort by date (newest first)
    unique_articles.sort(key=lambda x: x['date'], reverse=True)
    
    # Keep only the latest 50 articles
    unique_articles = unique_articles[:50]
    
    return unique_articles

def save_articles(articles):
    """Save articles to data/articles.json"""
    os.makedirs('data', exist_ok=True)
    
    with open('data/articles.json', 'w', encoding='utf-8') as f:
        json.dump(articles, f, ensure_ascii=False, indent=2)
    
    print(f"\nSuccessfully saved {len(articles)} articles to data/articles.json")

def main():
    print("Starting article fetch...")
    print("-" * 50)
    
    articles = fetch_articles()
    
    print("-" * 50)
    print(f"Total unique articles found: {len(articles)}")
    
    if articles:
        save_articles(articles)
        
        # Print summary by category
        print("\nArticles by category:")
        categories = {}
        for article in articles:
            cat = article['category']
            categories[cat] = categories.get(cat, 0) + 1
        
        for cat, count in categories.items():
            print(f"  {cat}: {count} articles")
    else:
        print("No articles found matching the keywords.")

if __name__ == '__main__':
    main()
