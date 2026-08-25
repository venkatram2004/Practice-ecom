from playwright.sync_api import sync_playwright, expect
Base_url="https://practicesoftwaretesting.com/"
products_to_search = ["Hammer", "Pliers", "Screwdriver"]

with sync_playwright() as p:
    browser = p.chromium.launch(headless=False)
    page=browser.new_page()

    for product_name in products_to_search:

        page.goto(Base_url)
        page.wait_for_timeout(2000)
        print("application opend")

        search_box=page.get_by_role("textbox",name="search")
        expect(search_box).to_be_visible()
        print("search box is visible")

        search_box.fill(product_name)
        print("entered: ",product_name)

        search_button=page.get_by_role("button",name="search")
        expect(search_button).to_be_visible()
        search_button.click()
        page.wait_for_timeout(2000)
        print("search performed")

        product_link=page.locator("a[href^='/product/']")
        product_count=product_link.count()
        print("no of result:",product_count)
        assert product_count>0,\
            "no search result"
        print("search result are displayed")

        product_names=[]

        for i in range(product_count):
            product=product_link.nth(i)
            name=product.locator("h5").inner_text()
            product_names.append(name)
        print("product found:", product_names)

        expected_product = None
        for i in range(product_count):
            product = product_link.nth(i)
            name = product.locator("h5").inner_text()
            if product_name.lower() in name.lower():
                expected_product = product
                break
        assert expected_product is not None, \
            "product was not found"
        print(product_name," appers in search")

        expect(expected_product).to_be_visible()
        expected_product.click()
        page.wait_for_timeout(2000)
        print("Product clicked")

        product_heading = page.locator("h1")
        expect(product_heading).to_be_visible()
        actual_product_name = product_heading.inner_text()
        print("Product details page:",actual_product_name)
        assert product_name.lower() in actual_product_name.lower(), \
            "Wrong product details page opened"
        print("Product name verified")

    page.wait_for_timeout(3000)
    browser.close()
