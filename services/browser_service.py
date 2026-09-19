from playwright.sync_api import (
    Browser,
    BrowserContext,
    Page,
    Playwright,
    sync_playwright,
)

from config.browser import BrowserConfig


class BrowserService:

    def __init__(self, config: BrowserConfig):
        self.config = config
        self.playwright: Playwright | None = None
        self.browser: Browser | None = None
        self.context: BrowserContext | None = None

    def start(self) -> Page:
        self.playwright = sync_playwright().start()

        self.browser = self.playwright.firefox.launch(
            headless=self.config.headless,
            slow_mo=self.config.slow_mo
        )

        context = self.browser.new_context()

        return context.new_page()

    def close(self) -> None:
        if self.context:
            self.context.close()

        if self.browser:
            self.browser.close()

        if self.playwright:
            self.playwright.stop()