# Test Design Guide (Selenium + pytest)

How this suite is built and the rules for adding to it. Read this before writing a test.

## 1. Layers (what goes where)
| Layer | Where | Contains | Must not contain |
|---|---|---|---|
| Tests | `tests/test_*.py` | What the shop must do, in plain steps, and the assertions | Selectors, `sleep` |
| Page objects | `pages/*_page.py` | The locators and actions of one screen, on top of `BasePage` (waits, clicks, bounded checks) | Test decisions |
| Flows | `pages/flows.py` | Whole journeys (`to_checkout_form`, `to_overview`, `place_order`) for tests that are about something else than the journey | |
| Fixtures | `conftest.py` | The browser (Chrome or Firefox), the base URL, `login_as(user)`, screenshots of failures | |
| Helpers | `tests/axe_helper.py`, `tests/vendor/` | The accessibility engine (axe-core) injected into the page | |

A change in the shop's markup should mean one change in one page object, and none in the tests.

## 2. Linking tests to the manual suite
```python
@known
@manual("TC-022")
@pytest.mark.xfail(reason="BUG-004: all products show the same placeholder image")
def test_problem_user_every_product_shows_its_own_image(login_as):
```

- **`@manual("TC-nnn")`** links a test to a case in the manual suite (inside a parametrized list: `marks=manual("TC-003")`). `python tools/trace.py` reads these and writes [traceability.md](traceability.md). CI fails if that file is out of date.
- **`BUG-nnn`** in the xfail reason links a known-defect test to its defect report in the manual-testing repository.
- **Markers** choose what to run: `smoke`, `a11y`, `keyboard`, `known_bug` (`python -m pytest -m smoke`).

## 3. Known-defect tests
A known defect is written as the **correct** behaviour and marked `xfail(strict=True)` (set once in `pytest.ini`):

- While the defect exists the test fails, which pytest reports as an **expected** failure (`XFAIL`), so CI stays green.
- When the site is fixed, the test starts to pass, and strict mode turns that into a failure ("XPASS"). That is the signal to remove the marker and close the defect.
- A new failure anywhere else turns CI red.

Never mark a test `xfail` to hide a flaky test. If you do not know why it fails, find out first.

## 4. Writing reliable tests
- **Explicit waits only.** `WebDriverWait` with expected conditions; there is no `sleep` anywhere.
- **The address changes before the page is drawn.** A test that waits for the URL and then reads the page can read the old page. Wait for an element that exists only on the new page (`CartPage.wait_until_loaded` waits for the cart list), and wait for values that settle after a click (`has_badge`, `has_count`, built on `BasePage.becomes`).
- **To prove something does NOT happen, give it time to happen first.** `BasePage.appears` and `url_becomes` wait a short, bounded time. A bare "is it there?" check passes on a page that simply has not been drawn yet, and under strict xfail that would turn CI red for the wrong reason.
- **Expected values come from the test or the data, not from the page.** The totals tests add up prices and the 8% tax themselves.
- **Each test gets a new browser.** No shared state, any order, safe to run in parallel (`-n 4`).
- **Parametrize, do not copy.** Bad logins, missing fields and screen sizes are one test each with an id per case.

## 5. Adding a test: checklist
1. Is there a manual case? Add `@manual("TC-nnn")`. A known defect? Add `@known`, and `@pytest.mark.xfail(reason="BUG-nnn: ...")`.
2. Does a page object method already do the action? Reuse it. If not, add it to the page object, not to the test.
3. Select by `data-test` (`BasePage.dt`). Avoid long CSS paths.
4. Run it three times before you push, on both browsers (`BROWSER=firefox python -m pytest -k "your test"`).
5. Run `python tools/trace.py` and commit the updated `docs/traceability.md`.

## 6. What this project deliberately does not do
- **Responsive checks on Firefox.** The tests set the screen size with Chrome's device emulation, because a desktop window cannot be made narrower than about 500 pixels. They are skipped on Firefox.
- **Visual (screenshot) comparison.** Baselines made on one machine fail on another.
- **Replace a manual screen-reader check.** Automated scans and keyboard tests catch many accessibility problems, but not all.
