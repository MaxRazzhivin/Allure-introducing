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
        s('[data-target="query-builder.input"]').send_keys("eroshenkoam/allure-example").press_enter()

    with allure.step("Переходим по ссылке репозитория"):
        s(by.link_text("eroshenkoam/allure-example")).click()

    with allure.step("Открываем таб Pull Requests"):
        s("#pull-requests-repo-tab-count").click()

    with allure.step("Проверяем наличие Pull request № 91 с текстом Fix pull request close test"):
        s('#issue_91').should(have.text('Fix pull request close test'))


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
    s('[data-target="query-builder.input"]').send_keys(repo).press_enter()


@allure.step("Переходим по ссылке репозитория {repo}")
def go_to_repository(repo):
    s(by.link_text(repo)).click()


@allure.step("Открываем таб Issues")
def open_pull_requests_tab():
    s("#pull-requests-repo-tab-count").click()


@allure.step("Проверяем наличие Pull Request с текстом {text}")
def should_see_issue_with_text(text):
    s('#issue_91').should(have.text(text))
    #s(by.partial_text('#issue_91')).should(be.visible) - альтернатива через часть текста


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
