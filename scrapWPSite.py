import requests
import sys
import json
import smtplib

#print(len(sys.argv))
url = 'http://kaniyam.com'
from_range = '2021-04-01T00:00:00'
to_range = '2021-04-22T00:00:00'
#email = sys.argv[4]
url_to_hit = url + '/wp-json/wp/v2/posts?after=' + from_range + '&before=' + to_range + '&per_page=100'
r  = requests.get(url_to_hit)
print(r.status_code)
data = r.text
#print(data)

print('***************************************')
print('Query Range:'+sys.argv[2]+' , '+sys.argv[3])
print('***************************************')
json_obj = json.loads(data)
post_count = len(json_obj)

#parse authors
author_set = set()
post_titles = set()
authors = set()
author_posts = {}
for i in json_obj:
    author_href = i['_links']['author'][0]['href']
    author_set.add(author_href)

    r1 = requests.get(author_href)
    author_name = r1.json()['name']
    authors.add(author_name)
    
    if author_name in author_posts:
        count = author_posts.get(author_name)
        author_posts[author_name] = count + 1
    else:
        author_posts[author_name] = 1
    
    post_titles.add(i['title']['rendered'] +' by ' +author_name)
#print(author_set)

#author_names
authors = set()
for i in author_set:
    r1 = requests.get(i)
    #print(r1.json()['name'])
    authors.add(r1.json()['name'])
print('PostCount:'+str(post_count))
print('***************************************')
print('Post Titles')

print('-----------')
for i in post_titles:
    print(i)
print('\n')
print('***************************************')
print('AuthorNames')
print('-----------')
for i in authors:
    print(i)
print('***************************************')
print('AuthorsCount:' + str(len(authors)))
print('***************************************')
print('Author and Posts count:')
print(author_posts)
print('***************************************')
