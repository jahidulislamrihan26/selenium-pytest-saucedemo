# Selenium + Python (pytest): SauceDemo

[![CI](https://github.com/jahidulislamrihan26/selenium-pytest-saucedemo/actions/workflows/ci.yml/badge.svg)](https://github.com/jahidulislamrihan26/selenium-pytest-saucedemo/actions/workflows/ci.yml) Part of the [SQA portfolio](https://github.com/jahidulislamrihan26/sqa-portfolio).

A **Selenium 4** suite in **Python with pytest** for the public [SauceDemo](https://www.saucedemo.com) web shop, built with the **Page Object Model**. It tests the same site as the [Playwright](https://github.com/jahidulislamrihan26/playwright-ui-automation-pom) and [Cypress](https://github.com/jahidulislamrihan26/cypress-e2e-saucedemo) suites, so the three tools can be compared on one application.

**Result in CI (headless Chrome): 29 tests, 28 pass and 1 expected failure** (the known login bypass), in about 40 seconds.

## What is covered
| Area | Checks |
|---|---|
| Login | valid login, five kinds of bad login (parametrized), masked password, logout closes the session |
| Product list | six products, sort by price and name, cart badge, product detail page |
| Cart and checkout | cart contents and prices, remove, continue shopping, full order, summary adds up, each missing field reported, cancel |
| Access control | inner pages need a login, script typed into the form is not executed, and the known **forged-cookie login bypass** (BUG-013) |

## How it is built
- **Page Object Model** in `pages/`: one class per screen on top of a `BasePage` that holds the waiting and clicking helpers. Tests read as user actions and contain no locators.
- **Explicit waits only.** `WebDriverWait` with expected conditions; there is no `sleep` anywhere.
- **pytest fixtures** in `conftest.py`: a fresh headless Chrome per test (tests cannot affect each other), a logged-in product list, and a cart ready for checkout.
- **Parametrized tests** keep the five bad logins and three missing-field cases in one test each.
- **Known defects** are written as the *correct* behaviour and marked `xfail(strict=True)`. The suite stays green while the defect exists and turns red the day it is fixed, which is the signal to close the defect.
- **Failure evidence:** a screenshot of every failed test and an HTML report, kept as CI artifacts.
- **CI:** every push, and nightly because the target is a public site.

## Run it
Needs Python 3.10 or newer and Google Chrome (Selenium finds the matching driver itself).
```bash
python -m venv .venv
.venv/Scripts/activate        # on macOS/Linux: source .venv/bin/activate
pip install -r requirements.txt
python -m pytest                       # everything, headless
python -m pytest -m smoke              # the short list
HEADLESS=0 python -m pytest -k login   # watch the browser
```
The HTML report is written to `reports/report.html`.

## Related projects
[playwright-ui-automation-pom](https://github.com/jahidulislamrihan26/playwright-ui-automation-pom) · [cypress-e2e-saucedemo](https://github.com/jahidulislamrihan26/cypress-e2e-saucedemo) · [manual-testing-saucedemo](https://github.com/jahidulislamrihan26/manual-testing-saucedemo) · [api-testing-newman-openapi](https://github.com/jahidulislamrihan26/api-testing-newman-openapi) · [k6-performance-testing](https://github.com/jahidulislamrihan26/k6-performance-testing) · [qa-templates](https://github.com/jahidulislamrihan26/qa-templates)

## License
Released under the [MIT License](LICENSE). Copyright (c) 2026 Md. Jahidul Islam Rihan.
