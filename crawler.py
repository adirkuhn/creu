from model import db, Author, News, db_session

class Craww:
    def craw(self):
        
        author_name = "John Last"
        author_bio = "some somethign about some shit"
        author = self.save_author(author_name, author_bio)

        news_title = 'Materia legal'
        news_content = 'sdkajsdkasd asdakjdas asjdkasjdkas aksjdkajsdkas aksjdkasd'
        news = self.save_news(news_title, news_content)

        n = self.newsAuthor(news, author)

        print vars(n)

    def newsAuthor(self, news, author):
        aauthor = author.query.filter(Author.news.any(id=news.id)).first()

        if (isinstance(aauthor, Author) == False):
            news.author.append(author)
            db_session.commit()
            db_session.refresh(news)

        return news

    def save_news(self, title, content):
        news = News.query.filter(News.title == title).first()
        if (isinstance(news, News) == False):
            news = News()
            news.title = title
            news.content = content

            db_session.add(news)
            db_session.commit()
            db_session.refresh(news)

        return news

    def save_author(self, author_name, bio):
        author = Author.query.filter(Author.name == author_name).first()
        if (isinstance(author, Author) == False):
            author = Author()
            author.name = author_name
            author.bio = bio

            db_session.add(author)
            db_session.commit()
            db_session.refresh(author)

        return author

if __name__ == '__main__':
    craww = Craww()
    craww.craw()