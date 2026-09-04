from playwright.sync_api import Page

def user_auth(page: Page):
    page.goto("https://www.saucedemo.com")

    page.get_by_role("textbox", name="Username").fill("standard_user")
    page.get_by_role("textbox", name="Password").fill("secret_sauce")
    page.get_by_role("button", name="Login").click()
