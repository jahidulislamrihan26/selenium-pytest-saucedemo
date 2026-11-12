# Selenium + Python (pytest): SauceDemo

[![CI](https://github.com/jahidulislamrihan26/selenium-pytest-saucedemo/actions/workflows/ci.yml/badge.svg)](https://github.com/jahidulislamrihan26/selenium-pytest-saucedemo/actions/workflows/ci.yml) Part of the [SQA portfolio](https://github.com/jahidulislamrihan26/sqa-portfolio).

A **Selenium 4** suite in **Python with pytest** for the public [SauceDemo](https://www.saucedemo.com) web shop, built with the **Page Object Model** and linked test by test to a manual test suite. It tests the same site as the [Playwright](https://github.com/jahidulislamrihan26/playwright-ui-automation-pom) and [Cypress](https://github.com/jahidulislamrihan26/cypress-e2e-saucedemo) projects, so the three tools can be compared on one application.

## Result in one look
| | |
|---|---|
| Tests | **104**, run on **Chrome and Firefox** in CI, 4 in parallel |
| Chrome | 74 pass, 30 expected failures (known defects), 0 unexpected, 98 seconds |
| Firefox | 64 pass, 30 expected failures, 0 unexpected, 10 skipped on purpose (screen-size emulation is Chrome-only), about 4 minutes |
| Manual cases automated | **80 of 87 (92%)**, each test linked with `@manual("TC-nnn")`; the [traceability table](docs/traceability.md) is generated and checked in CI |
| Known defects captured | **all 20 of 20** logged site defects, including the two that only a real keyboard test can find (the cart cannot be reached with Tab, and keyboard focus is invisible) |
| Accessibility | axe-core scan (WCAG 2.0/2.1 A and AA) of all 7 pages: no critical violations |
| Design guide | [docs/test-design.md](docs/test-design.md): layers, conventions, reliable waits, how to add a test |

## What is covered
| Area | Test file | Checks |
|---|---|---|
| Login | `test_login.py` | valid login, nine kinds of bad login (parametrized), masked password, Enter key, dismissing the error, logout, cart kept after logging in again |
| Product list | `test_inventory.py` | six products, image alt text, all four sorts, add and remove, badge counts, all six products, double-click, Reset App State, detail page |
| Cart and checkout | `test_cart_and_checkout.py` | contents and prices, full order, totals worked out in the test (3 products and all 6), each missing field, cancel, cart empty afterwards |
| Special test users | `test_personas.py` | `problem_user`, `error_user`, `performance_glitch_user`, `visual_user`: ten known defects |
| Known defects of the standard user | `test_defects.py` | empty-cart checkout, accepted bad postal codes and names, Reset App State, sort lost, order pages opened directly, Back after an order, unhelpful not-found pages |
| Security | `test_security.py` | pages need a login, forged cookie, cookie flags and lifetime, HTTP to HTTPS, security headers, script text not executed |
| Keyboard | `test_keyboard.py` | Tab order, Enter, Escape, cart reachable by Tab, visible focus, a whole purchase without a mouse |
| Accessibility | `test_accessibility.py` | axe-core scan of 7 pages, page title and language |
| Responsive | `test_responsive.py` | 5 screen sizes (Chrome device emulation) |
| Navigation | `test_navigation.py` | invalid product ids, About link, footer links |

## How it is built
- **Page Object Model** in `pages/`: one class per screen on top of a `BasePage` that holds the waiting and clicking helpers, and `flows.py` for whole journeys. Tests read as user actions and contain no locators.
- **Explicit waits only.** `WebDriverWait` with expected conditions; there is no `sleep` anywhere. Values that settle after a click (cart badge, cart rows) are waited for, not read once. Checks that something must **not** happen give it a short, bounded time to happen first.
- **Two browsers.** `BROWSER=chrome` (default) or `BROWSER=firefox`; the CI matrix runs both.
- **Parallel.** `pytest-xdist` runs 4 tests at a time; each test gets its own browser, so they cannot affect each other.
- **pytest fixtures** in `conftest.py`: the browser, `login_as("problem")` for any of the site's test users, and a logged-in product list.
- **Parametrized tests** keep the bad logins, missing fields and screen sizes in one test each, with an id per case.
- **Known defects** are written as the *correct* behaviour and marked `xfail(strict=True)`. The suite stays green while the defect exists and turns red the day it is fixed, which is the signal to close the defect.
- **Accessibility** uses axe-core (vendored in `tests/vendor/`, licence included), the same rules as the other two UI projects.
- **Failure evidence:** a screenshot of every failed test and an HTML report, kept as CI artifacts.
- **CI:** every push, and nightly because the target is a public site.

## Run it
Needs Python 3.10 or newer and Google Chrome (and Firefox for the Firefox run). Selenium finds the matching driver itself.
```bash
python -m venv .venv
.venv/Scripts/activate        # on macOS/Linux: source .venv/bin/activate
pip install -r requirements.txt
python -m pytest -n 4                  # everything, headless, 4 in parallel
python -m pytest -m smoke              # the short list
BROWSER=firefox python -m pytest -n 4  # the same on Firefox
HEADLESS=0 python -m pytest -k login   # watch the browser
python tools/trace.py                  # rebuild docs/traceability.md
```
Add `--html=reports/report.html --self-contained-html` for an HTML report.

## Related projects
[playwright-ui-automation-pom](https://github.com/jahidulislamrihan26/playwright-ui-automation-pom) (the same site in Playwright) · [cypress-e2e-saucedemo](https://github.com/jahidulislamrihan26/cypress-e2e-saucedemo) (the same site in Cypress) · [manual-testing-saucedemo](https://github.com/jahidulislamrihan26/manual-testing-saucedemo) (the 87 cases and 20 defects these tests are linked to) · [api-testing-newman-openapi](https://github.com/jahidulislamrihan26/api-testing-newman-openapi) · [k6-performance-testing](https://github.com/jahidulislamrihan26/k6-performance-testing) · [qa-templates](https://github.com/jahidulislamrihan26/qa-templates)

## License
Released under the [MIT License](LICENSE). Copyright (c) 2026 Md. Jahidul Islam Rihan.
