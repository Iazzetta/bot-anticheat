from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import re

ROTES = {
    "pb-section":"http://www.webcheats.com.br/forums/477/",
    "login":"http://www.webcheats.com.br/login",
    "thread":"http://www.webcheats.com.br/threads/%s",
}
USUARIO = "XXXXXX"
SENHA = "XXXXXXX"

browser = webdriver.PhantomJS()

# E necessario fazer login, para ver todos os links, inclusive os em HIDE POST
print("~> Fazendo login no forum.")
browser.get(ROTES["login"])
login = browser.find_element_by_css_selector('#ctrl_pageLogin_login')
senha = browser.find_element_by_css_selector('#ctrl_pageLogin_password')
login.send_keys(USUARIO)
senha.send_keys(SENHA)
senha.send_keys(Keys.RETURN)

print("~> Bem vindo %s, iniciando BOT." % USUARIO)

#PB Section
print("~> Acessando PointBlank Cheats.")
list_posts_to_analyse = []
browser.get(ROTES["pb-section"])
topicos = browser.find_elements_by_css_selector("li.discussionListItem")
for t in topicos:
    target = t.get_attribute("id").replace("thread-", "")
    link_topico = ROTES["thread"] % target
    author_url = t.find_element_by_css_selector('a.username').get_attribute('href')
    topic_obj = {
        "author": author_url,
        "topic": link_topico,
    }
    list_posts_to_analyse.append(topic_obj)
    
print("~> Varrer posts e obter todos links para analisar.")
for pa in list_posts_to_analyse:
    print("Analisar: %s" % pa['topic'])
    browser.get(pa['topic'])
    primary_post = browser.find_element_by_css_selector(".primaryContent")
    message_content = primary_post.find_element_by_css_selector(".messageContent")
    content_without_anonym = message_content.text.replace("anonym.to/", "")
    list_urls = re.findall('http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+', content_without_anonym)
    print("Links encontrados: %s" % list_urls)
        
    