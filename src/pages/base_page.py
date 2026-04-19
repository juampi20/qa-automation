# Archivo que contiene todas las acciones (clicks, mover, ...)

from playwright.sync_api import Page

class BasePage:
    def __init__(self, page: Page, timeout: int = 10000):
        self.page = page
        self.timeout = timeout
