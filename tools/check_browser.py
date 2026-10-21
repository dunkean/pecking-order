"""Optional browser acceptance checks. Install `.[browser]`, start the studio first."""

import json
import os
from pathlib import Path

from playwright.sync_api import expect, sync_playwright

root = Path(__file__).resolve().parents[1]
output = root / "output/screenshots"
output.mkdir(parents=True, exist_ok=True)
url = os.environ.get("PECKING_ORDER_URL", "http://127.0.0.1:8773")
edge = Path(os.environ.get("STUDIO_BROWSER", r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe"))

with sync_playwright() as p:
    browser = p.chromium.launch(executable_path=str(edge) if edge.exists() else None,
                                headless=True)
    page = browser.new_page(viewport={"width": 1440, "height": 1050}, device_scale_factor=1)
    errors = []
    page.on("pageerror", lambda error: errors.append(str(error)))
    page.on("console", lambda msg: errors.append(msg.text) if msg.type == "error" else None)
    page.goto(url)
    expect(page.locator(".office-title").first).to_contain_text("Kgosi")
    expect(page.locator(".translations").first).to_contain_text("Français")
    page.screenshot(path=str(output / "tswana-fr.png"), full_page=True)
    page.screenshot(path=str(output / "demo.png"))
    page.select_option("#locale", "en")
    expect(page.locator("h1")).to_contain_text("Who holds the title?")
    expect(page.locator(".office-title").first).to_contain_text("chief")
    page.select_option("#example", "1")
    expect(page.locator(".office-title").first).to_contain_text("Karta")
    page.select_option("#example", "4")
    expect(page.locator(".office-title").first).to_contain_text("Grand Council")
    assert page.locator('article[data-role="head"]').count() == 0
    page.select_option("#example", "5")
    expect(page.locator("#roles")).to_contain_text("Lieutenant General")
    page.select_option("#example", "6")
    expect(page.locator("#roles")).to_contain_text("Shogun")
    page.select_option("#example", "10")
    expect(page.locator("#roles")).to_contain_text("Raya")
    expect(page.locator("#roles")).to_contain_text("unilateral decisions")
    page.select_option("#example", "8")
    expect(page.locator("#candidates button")).to_have_count(3)
    expect(page.locator(".office")).to_have_count(0)
    page.locator("#candidates button").filter(has_text="Tswana").click()
    expect(page.locator(".office-title").first).to_contain_text("Kgosi")
    page.select_option("#example", "9")
    expect(page.locator(".office-title").first).to_have_text("King")
    with page.expect_download() as download:
        page.click("#download-query")
    path = output.parent / "browser-request.json"
    download.value.save_as(str(path))
    assert json.loads(path.read_text())["mode"] == "generic"
    page.select_option("#example", "0")
    expect(page.locator(".office-title").first).to_contain_text("Kgosi")
    page.set_input_files("#import-query", str(path))
    expect(page.locator(".office-title").first).to_have_text("King")
    page.select_option("#locale", "fr")
    expect(page.locator(".office-title").first).to_have_text("Roi")
    page.screenshot(path=str(output / "monarchy-fr.png"), full_page=True)
    page.set_viewport_size({"width": 390, "height": 844})
    expect(page.locator("h1")).to_be_visible()
    assert page.evaluate("document.documentElement.scrollWidth <= innerWidth")
    page.screenshot(path=str(output / "mobile-fr.png"), full_page=True)
    assert not errors, errors
    browser.close()
print("Browser checks passed: FR/EN, cultural examples, ambiguity, export/import, mobile, console.")
