from playwright.sync_api import expect, sync_playwright

with sync_playwright() as p:
    browser = p.chromium.launch(headless=False)
    page = browser.new_page()
    page.goto("https://practicesoftwaretesting.com/")
    page.wait_for_timeout(3000)

    # 1Click Categories Dropdown button
    page.get_by_role("button", name="Categories").click()
    page.wait_for_timeout(1000)

    page.locator('a[href^= "/category/hand-tools"]').click()
    page.wait_for_timeout(3000)

    # 2Verify that the category page is displayed
    category_title = page.locator("h2")
    expect(category_title).to_be_visible()
    print(category_title.text_content())

    # 3Verify that products are displayed
    expect(page.locator('img[alt="Combination Pliers"]')).to_be_visible()
    print("products are displayed")

    # 4Verify displayed products belong to the category
    product_names = page.locator(
        'h5[data-test="product-name"]').all_text_contents()
    for name in product_names:
        print("Product in Hand Tools:", name)

    # 5Bonus: Print the number of products displayed
    products = page.locator("a.card")
    total_count = products.count()
    print("Number of products displayed:", total_count)

    page.wait_for_timeout(5000)
    browser.close()



