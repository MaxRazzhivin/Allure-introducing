from selene import have
from selene.support import by
from selene.support.shared import browser
from selene.support.shared.jquery_style import s


def test_github():
    browser.open("https://github.com")

    s('.search-input').click()
    s('[data-target="query-builder.input"]').send_keys("eroshenkoam/allure-example").press_enter()

    s(by.link_text("eroshenkoam/allure-example")).click()

    s("#pull-requests-repo-tab-count").click()

    s('#issue_91').should(have.text('Fix pull request close test'))
