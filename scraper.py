from urllib.parse import urlparse

import requests
import yaml
from bs4 import BeautifulSoup
from jinja2 import FileSystemLoader, Environment as Jinja2Environment

BASE_URL = "https://www.earthdata.nasa.gov"
topics_url = f"{BASE_URL}/topics"


# env = Jinja2Environment(loader=FileSystemLoader("templates"))
# topics_template = env.get_template("topics.yml.j2")
#
# topics = [
#     {
#         "name": "topic1",
#         "url": "topic1.com",
#         "rss": "topic1-rss.com",
#         "description": "this is topic1"
#     },
#     {
#         "name": "topic2",
#         "url": "topic2.com",
#         "rss": "topic2-rss.com",
#         "description": "this is topic2"
#     }
# ]
#
# content = topics_template.render(
#     topics_url="dummy.com",
#     topics_rss="rss.com",
#     topics_description="just testing",
#     topics=topics,
# )
# with open('topics.yml', 'w') as file:
#     file.write(content)


def parse(url: str) -> BeautifulSoup:
    html = requests.get(url).content
    return BeautifulSoup(html, 'html.parser')


def new_topic():
    return {
        "name": None,
        "url": None,
        "rss": None,
        "description": None,
        "subtopics": []
    }


def parse_topic(topic, topic_element):
    topic_url = f"{BASE_URL}{topic_element['href']}"
    path = urlparse(topic_url).path
    topic_html = parse(topic_url)

    rss_href = topic_html.find_all('a', href=lambda x: x is not None and "/topics/rss/" in x)[0]['href']
    topic_rss = f"{BASE_URL}{rss_href}"

    headline_element = [el.text for el in topic_html.find_all('div', attrs={'class': 'hero-description'})]
    headline = headline_element[0] if len(headline_element) > 0 else None
    description_element = [el.text for el in
                           topic_html.find_all('div', attrs={'class': 'clearfix text-formatted field field--name-field-text-content field--type-text-long field--label-hidden field__item'})]
    description = description_element[0] if len(description_element) > 0 else topic_html.find_all('div', class_="pt-3 pb-5")[0].text
    description = description.replace("\n", " ").strip()
    full_description = f"{headline}\n{description}" if headline is not None else f"{description}"

    full_description = full_description.strip().replace("\n", "").replace("\\", "").replace("'", "").replace("\'", "")
    full_description = " ".join(full_description.split())

    topic['name'] = topic_element.text
    topic['url'] = topic_url
    topic['rss'] = topic_rss
    topic['description'] = full_description

    # topic['subtopics'] = parse()

    subtopics_list = [link for link in topic_html.find_all('a', href=True) if f"{path}/" in link["href"]]

    for subtopic_element in subtopics_list:
        subtopic = new_topic()
        topic['subtopics'].append(parse_topic(subtopic, subtopic_element))
        print()

    return topic


topics_html = parse(topics_url)
# print(soup.title)

topics_list = [topic.contents[0] for topic in topics_html.find_all('div', attrs={'class': lambda e: e.startswith('landing-section-title') if e else False})]

topics = []

for topic_element in topics_list:
    topic = new_topic()
    parse_topic(topic, topic_element)
    topics.append(topic)
    # # role_absolute_path = os.path.join(local_cache_path, iam_policies_repo, environment.role_file_path)
    # a = topics_template.render(
    #     topics_url=topic_url,
    #     topics_rss=topic_url,
    #     topics_description=description,
    # )

with open('topics.yml', 'w') as file:
    yml_dump = yaml.dump(topics, file, indent=4, sort_keys=False, default_flow_style=False, allow_unicode=True, encoding=None)
    print(yml_dump)
