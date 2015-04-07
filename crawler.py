from model import db, Author, News
from xml.dom.minidom import parse, parseString
import urllib
import re
import lxml
from lxml.html.clean import Cleaner
import unicodedata
import datetime

class Craww:
    def craw(self):

        tech_rss_url = "http://feeds.feedburner.com/TechCrunch/"

        tech = urllib.urlopen(tech_rss_url)
        tech_content = tech.read()

        tech_dom = parseString(tech_content)

        news_dom = tech_dom.getElementsByTagName('feedburner:origLink')

        for n in news_dom:
            url = n.firstChild.nodeValue

            if(isinstance(self.findNewsByUrl(url), News) == False):
                self.crawNews(url)


        return

    def crawNews(self, url):
        cleaner = Cleaner()
        cleaner.javascript = True
        cleaner.style = True
        cleaner.comments = True

        tech_content = lxml.html.parse(url)
        tech_content = (lxml.html.tostring(tech_content))

        re_title = re.compile(r'<h1.*>(.*)</h1', re.S)
        re_content = re.compile(r'<!-- Begin: Wordpress Article Content -->(.*)<!-- End: Wordpress Article Content -->', re.S)
        re_published = re.compile(r'name="sailthru.date"\scontent="(.*?)"')
        re_author = re.compile(r'<a\shref="(.*?)"\stitle.*?rel="author">(.*?)<\/a>.*?rel="external">(.*?)<\/a>')

        match_title = re.search(re_title, tech_content)
        match_content = re.search(re_content, tech_content)
        match_date = re.search(re_published, tech_content)
        match_author = re.search(re_author, tech_content)

        author_url = "http://techcrunch.com" + match_author.group(1)
        author_name = match_author.group(2)
        author_twitter = match_author.group(3)

        title = re.sub(r'<[^>]*?>', '', cleaner.clean_html(match_title.group(1)))
        title = re.sub(r'\s+', ' ', title)
        title = title.decode('utf-8').strip()
        content = re.sub(r'<[^>]*?>', '', cleaner.clean_html(match_content.group(1)))
        content = re.sub(r'\s+', ' ', content)
        content = content.decode('utf-8').strip()
        content = content.strip('\n')
        published_on = datetime.datetime.strptime(match_date.group(1), '%Y-%m-%d %H:%M:%S')

        news = self.save_news(url, title, content, published_on)

        author = self.findAuthorByUrl(author_url)
        if (isinstance(author, Author) == False):
            author = self.save_author(author_url, author_name, author_twitter, '')

        self.newsAuthor(news, author)

    def findAuthorByUrl(self, url):
        return Author.query.filter(Author.url == url).first()

    def findNewsByUrl(self, url):
        return News.query.filter(News.url == url).first()

    def newsAuthor(self, news, author):
        aauthor = author.query.filter(Author.news.any(id=news.id)).first()

        if (isinstance(aauthor, Author) == False):
            news.author.append(author)
            db.session.commit()
            db.session.refresh(news)

        return news

    def save_news(self, url, title, content, published_on):
        news = News.query.filter(News.title == title).first()
        if (isinstance(news, News) == False):
            news = News()
            news.url = url
            news.title = title
            news.content = content
            news.published_on = published_on

            db.session.add(news)
            db.session.commit()
            db.session.refresh(news)

        return news

    def save_author(self, author_url, author_name, author_twitter, author_bio):
        author = Author.query.filter(Author.url == author_url).first()
        if (isinstance(author, Author) == False):
            author = Author()
            author.url = author_url
            author.name = author_name
            author.twitter = author_twitter
            author.bio = author_bio

            db.session.add(author)
            db.session.commit()
            db.session.refresh(author)

        return author

if __name__ == '__main__':
    craww = Craww()
    craww.craw()