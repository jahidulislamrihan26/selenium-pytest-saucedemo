"""Runs the axe-core accessibility engine (WCAG 2.0/2.1 A and AA rules, including colour contrast) in the page under test."""
from pathlib import Path

AXE_SOURCE = (Path(__file__).parent / "vendor" / "axe.min.js").read_text(encoding="utf-8")
TAGS = ["wcag2a", "wcag2aa", "wcag21a", "wcag21aa"]

_RUN = """
const done = arguments[arguments.length - 1];
axe.run(document, { runOnly: { type: 'tag', values: arguments[0] } })
  .then((r) => done(r.violations.map((v) => ({ id: v.id, impact: v.impact, help: v.help, nodes: v.nodes.length }))))
  .catch((e) => done([{ id: 'axe-error', impact: 'critical', help: String(e), nodes: 0 }]));
"""


def violations(driver) -> list[dict]:
    """All axe violations on the current page."""
    driver.execute_script(AXE_SOURCE)
    driver.set_script_timeout(30)
    return driver.execute_async_script(_RUN, TAGS)


def critical(driver) -> list[dict]:
    """Violations of impact 'critical', the level the project's rule applies to."""
    return [v for v in violations(driver) if v["impact"] == "critical"]
