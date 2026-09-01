import pytest
from playwright.sync_api import Page, expect, Locator

URL = "https://the-internet.herokuapp.com/hovers"


def hover_and_validate(
    page: Page,
    target_element: Locator,
    revealed_element: Locator
):
    expect(revealed_element).not_to_be_visible()

    target_element.hover()
    expect(revealed_element).to_be_visible()

    page.mouse.move(0, 0)
    expect(revealed_element).not_to_be_visible()


def test_hover_product_interaction(page: Page):
    page.goto(URL)

    figure = page.locator(".figure").first
    caption = figure.locator(".figcaption")
    profile_link = caption.locator("a")

    expect(caption).not_to_be_visible()

    figure.hover()

    expect(caption).to_be_visible()
    expect(caption.locator("h5")).to_have_text("name: user1")
    expect(profile_link).to_be_visible()

    profile_link.click()

    expect(page).to_have_url("https://the-internet.herokuapp.com/users/1")

    page.go_back()
    figure = page.locator(".figure").first
    caption = figure.locator(".figcaption")

    figure.hover()
    expect(caption).to_be_visible()

    page.mouse.move(0, 0)

    expect(caption).not_to_be_visible()


@pytest.mark.parametrize(
    "index, expected_user",
    [
        (0, "name: user1"),
        (1, "name: user2"),
        (2, "name: user3"),
    ],
)
def test_multiple_elements_hover_with_helper(page: Page, index: int, expected_user: str):
    page.goto(URL)

    figure = page.locator(".figure").nth(index)
    caption = figure.locator(".figcaption")

    hover_and_validate(page, target_element=figure, revealed_element=caption)

    figure.hover()
    expect(caption.locator("h5")).to_have_text(expected_user)
