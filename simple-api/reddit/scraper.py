import praw
from fastapi import FastAPI
from pydantic import BaseModel
from typing import Optional
import uvicorn

app = FastAPI()

@app.get('/search')
async def search_reddit(subreddit: str, searchterm: str, time: str = 'month'):
    reddit = praw.Reddit('bot1', config_interpolation='basic')
    posts = []
    try:
        results = reddit.subreddit(subreddit).search(searchterm, time_filter=time)
    except:
        return 404
    for submission in results:
        post = {}
        post['title'] = submission.title
        post['url'] = submission.url
        cisco_comments = []
        for comment in submission.comments.list():
            if 'cisco' in comment.body.lower():
                cisco_comments.append(comment.body)
        post['comments'] = cisco_comments
        posts.append(post)
    return posts

if __name__ == "__main__":
    uvicorn.run("scraper:app", host="0.0.0.0", port=8000)