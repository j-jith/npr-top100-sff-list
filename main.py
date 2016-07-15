#!/usr/bin/env python3
from lxml import etree
import jinja2
import os

SCRIPT_PATH = os.path.dirname(os.path.abspath(__file__))

def get_books(url):

    parser = etree.HTMLParser()
    try:
        tree = etree.parse(url, parser)
    except etree.ParseError as e:
        print(e)

    #positions = tree.xpath("//div[@class='bucket listitem booklistitem']/div[@class='bestsellmeta']/p[@class='position']/text()")
    #titles = tree.xpath("//div[@class='bucket listitem booklistitem']/div[@class='bucketblock']/h3/a/text()")
    #authors = tree.xpath("//div[@class='bucket listitem booklistitem']/div[@class='bucketblock']/div[@class='bookMeta']/p[@class='author']/a/span/text()")
    #descriptions = tree.xpath("//div[@class='bucket listitem booklistitem']/div[@class='bucketblock']/div[@class='bucketwrap listtext']/div[@class='bucket']/p")
    #return [{'position': p, 'title': t, 'author': a, 'description': etree.tostring(d).strip().decode('utf-8')} for p, t, a, d in zip(positions, titles, authors, descriptions)]

    book_items = tree.xpath("//div[@class='bucket listitem booklistitem']")

    books = []
    for item in book_items:
        book = {}
        book['position'] = item.xpath("./div[@class='bestsellmeta']/p[@class='position']/text()")[0]
        book['title'] = item.xpath("./div[@class='bucketblock']/h3/a/text()")[0]
        book['author'] = item.xpath("./div[@class='bucketblock']/div[@class='bookMeta']/p[@class='author']/a/span/text()")[0]

        desc = item.xpath("./div[@class='bucketblock']/div[@class='bucketwrap listtext']/div[@class='bucket']/p")
        if not desc:
            desc = item.xpath("./div[@class='bucketblock']/div[@class='capsulereview']/blockquote/p")

        book['description'] = etree.tostring(desc[0]).strip().decode('utf-8')
        books.append(book)

    return books


def render_template(books):

    # jinja stuff to load template
    template_loader = jinja2.FileSystemLoader(searchpath=SCRIPT_PATH)
    template_env = jinja2.Environment(loader=template_loader)
    template_file = 'template.jinja'
    template = template_env.get_template(template_file)

    # render template and return html
    return template.render(books)    

def write_html(data, filename):

    # write data to file
    with open(filename, 'w') as f:
        f.write(data)


if __name__ == '__main__':

    npr_url = 'http://www.npr.org/2011/08/11/139085843/your-picks-top-100-science-fiction-fantasy-books'
    
    books = get_books(npr_url)

    html = render_template({'books': books})
    write_html(html, SCRIPT_PATH + '/index.html')
