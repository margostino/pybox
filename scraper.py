import requests
import yaml
from urllib.parse import urlparse
from bs4 import BeautifulSoup
from jinja2 import FileSystemLoader, Environment as Jinja2Environment


def parse(url: str) -> BeautifulSoup:
    html = requests.get(url).content
    return BeautifulSoup(html, 'html.parser')


BASE_URL = "https://www.earthdata.nasa.gov"
topics_url = f"{BASE_URL}/topics"

topics_html = parse(topics_url)
# print(soup.title)

env = Jinja2Environment(loader=FileSystemLoader("templates"))
topics_template = env.get_template("topics.yml.j2")

topics_list = [topic.contents[0] for topic in topics_html.find_all('div', attrs={'class': lambda e: e.startswith('landing-section-title') if e else False})]


def parse_topic(topic, topic_element):
    topic_url = f"{BASE_URL}{topic_element['href']}"
    path = urlparse(topic_url).path
    topic_html = parse(topic_url)
    headline_element = [el.text for el in topic_html.find_all('div', attrs={'class': 'hero-description'})]
    headline = headline_element[0] if len(headline_element) > 0 else None
    description_element = [el.text for el in topic_html.find_all('div', attrs={'class': 'clearfix text-formatted field field--name-field-text-content field--type-text-long field--label-hidden field__item'})]
    description = description_element[0] if len(description_element) > 0 else topic_html.find_all('div', class_="pt-3 pb-5")[0].text

    topic['name'] = topic_element.text
    topic['url'] = topic_url
    topic['description'] = f"{headline}\n{description}" if headline is not None else f"{description}"

    # topic['subtopics'] = parse()

    subtopics_list = [link for link in topic_html.find_all('a', href=True) if f"{path}/" in link["href"]]

    for subtopic_element in subtopics_list:
        subtopic = {
            'subtopics': []
        }
        topic['subtopics'].append(parse_topic(subtopic, subtopic_element))
        print()

    return topic


for topic_element in topics_list:
    topic = {
        'subtopics': []
    }
    parse_topic(topic, topic_element)
    print()
    # # role_absolute_path = os.path.join(local_cache_path, iam_policies_repo, environment.role_file_path)
    # a = topics_template.render(
    #     topics_url=topic_url,
    #     topics_rss=topic_url,
    #     topics_description=description,
    # )

    # view-mode-full ds-1col clearfix

    print()

links = soup.find_all('a', href=True)

topic_links = [link for link in links if "/topics/" in link["href"]]

for link in links:
    if "atmosphere" in link:
        print("")

