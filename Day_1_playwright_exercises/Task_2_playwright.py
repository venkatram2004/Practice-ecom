from playwright.sync_api import sync_playwright, expect


BASE_URL = "https://practicesoftwaretesting.com/"


with sync_playwright() as p:

    browser = p.chromium.launch(headless=False)
    page = browser.new_page()

    page.goto(BASE_URL)
    page.wait_for_timeout(2000)

    search_box = page.get_by_role("textbox", name="Search")
    expect(search_box).to_be_visible()
    print("Search box is visible")


    search_box.fill("Hammer")
    print("Entered: Hammer")


    search_button = page.get_by_role("button",name="Search")
    expect(search_button).to_be_visible()
    search_button.click()
    page.wait_for_timeout(2000)
    print("Search button clicked")


    products = page.locator("a[href^='/product/']")
    product_count = products.count()
    print("Number of search results:", product_count)
    assert product_count > 0, \
        "No search results were displayed"
    print("Search results are displayed")


    hammer = page.get_by_role("heading",name="Hammer",exact=True)
    expect(hammer).to_be_visible()
    print("Hammer appears in search results")
    print("VALID SEARCH TEST PASSED")




    page.goto(BASE_URL)
    page.wait_for_timeout(2000)
    search_box = page.get_by_role("textbox",name="Search")
    expect(search_box).to_be_visible()


    search_box.fill("Bottel ")
    print("Entered invalid product")


    search_button = page.get_by_role("button",name="Search")
    search_button.click()
    page.wait_for_timeout(2000)
    print("Search button clicked")


    products = page.locator("a[href^='/product/']")
    product_count = products.count()
    print("Number of search results:", product_count)
    assert product_count == 0, \
        "Products were displayed for an invalid search"
    print("No products found")
    print("INVALID SEARCH TEST PASSED")


    page.wait_for_timeout(5000)

    browser.close()
