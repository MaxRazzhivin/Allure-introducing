# Allure знакомство

## Установка - brew install allure

1) в файл requirements.txt - добавляем allure-pytest
2) в файл игнора .gitignore - allure-results папку, либо tests/allure-results
3) создаем файл pytest.ini - в нем пишем:


```bash
[pytest]

addopts =
    --clean-alluredir
    --alluredir=allure-results
    
```

4) запускаем тест - после этого отчеты о тестах смотрим через команду allure serve tests/allure-results

```bash
Есть два подхода к работе с аллюром: 
- динамический (офомрляем каждый шаг "на ходу" внутри функции);
- decorator_steps, похожий на PageObject (выносим аллюр логику с отдельное место)

```

```bash
Динамический:

import allure
from allure_commons.types import Severity
from selene import have
from selene.support import by
from selene.support.shared import browser
from selene.support.shared.jquery_style import s

def test_dynamic_steps():
    with allure.step("Открываем главную страницу"):
        browser.open("https://github.com")

    with allure.step("Ищем репозиторий"):
        s('.search-input').click()
        s('#query-builder-test').send_keys("eroshenkoam/allure-example").press_enter()

    with allure.step("Переходим по ссылке репозитория"):
        s(by.link_text("eroshenkoam/allure-example")).click()

    with allure.step("Открываем таб Pull Requests"):
        s("#pull-requests-repo-tab-count").click()

    with allure.step("Проверяем наличие Pull request № 91 с текстом Fix pull request close test"):
        s('#issue_91').should(have.text('Fix pull request close test'))

```

```bash
DecoratorSteps (PageObject)

def test_decorator_steps():
    open_main_page()
    search_for_repository("eroshenkoam/allure-example")
    go_to_repository("eroshenkoam/allure-example")
    open_pull_requests_tab()
    should_see_issue_with_text('Fix pull request close test')


@allure.step("Открываем главную страницу")
def open_main_page():
    browser.open("https://github.com")


@allure.step("Ищем репозиторий {repo}")
def search_for_repository(repo):
    s('.search-input').click()
    s('#query-builder-test').send_keys(repo).press_enter()


@allure.step("Переходим по ссылке репозитория {repo}")
def go_to_repository(repo):
    s(by.link_text(repo)).click()


@allure.step("Открываем таб Issues")
def open_pull_requests_tab():
    s("#pull-requests-repo-tab-count").click()


@allure.step("Проверяем наличие Pull Request с текстом {text}")
def should_see_issue_with_text(text):
    s('#issue_91').should(have.text(text))

```

## Варианты разметки в аллюр отчете:

```bash
@allure.tag("web")
@allure.label("owner", "Max Razzhivin")
@allure.feature("Ищем среди pull requests")
@allure.story("Отображается pull request с именем 'Fix pull request close test'")
@allure.link("https://github.com", "Test")
@allure.severity(Severity.CRITICAL)
def test_issue_with_all_annotations():
    open_main_page()
    search_for_repository("eroshenkoam/allure-example")
    go_to_repository("eroshenkoam/allure-example")
    open_pull_requests_tab()
    should_see_issue_with_text('Fix pull request close test')

```

## Работа с Allure attachments

```bash
Варианты аттачей из документации аллюр:

    TEXT = ("text/plain", "txt")
    CSV = ("text/csv", "csv")
    TSV = ("text/tab-separated-values", "tsv")
    URI_LIST = ("text/uri-list", "uri")

    HTML = ("text/html", "html")
    XML = ("application/xml", "xml")
    JSON = ("application/json", "json")
    YAML = ("application/yaml", "yaml")
    PCAP = ("application/vnd.tcpdump.pcap", "pcap")

    PNG = ("image/png", "png")
    JPG = ("image/jpg", "jpg")
    SVG = ("image/svg+xml", "svg")
    GIF = ("image/gif", "gif")
    BMP = ("image/bmp", "bmp")
    TIFF = ("image/tiff", "tiff")

    MP4 = ("video/mp4", "mp4")
    OGG = ("video/ogg", "ogg")
    WEBM = ("video/webm", "webm")

    PDF = ("application/pdf", "pdf")

```

```bash
Полезные примеры:

Обычно внутри корня проекта создается папка utils -> attach.py

Внутри нее (видео для селеноида иуказано - надо править для локального теста): 

import allure
from allure_commons.types import AttachmentType

def add_screenshot(browser):
    png = browser.driver.get_screenshot_as_png()
    allure.attach(body=png, name='screenshot', attachment_type=AttachmentType.PNG, extension='.png')


def add_logs(browser):
    log = "".join(f'{text}\n' for text in browser.driver.get_log(log_type='browser'))
    allure.attach(log, 'browser_logs', AttachmentType.TEXT, '.log')


def add_html(browser):
    html = browser.driver.page_source
    allure.attach(html, 'page_source', AttachmentType.HTML, '.html')


def add_video(browser):
    video_url = "https://selenoid.autotests.cloud/video/" + browser.driver.session_id + ".mp4"
    html = "<html><body><video width='100%' height='100%' controls autoplay><source src='" \
           + video_url \
           + "' type='video/mp4'></video></body></html>"
    allure.attach(html, 'video_' + browser.driver.session_id, AttachmentType.HTML, '.html')
```