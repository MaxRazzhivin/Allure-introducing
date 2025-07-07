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