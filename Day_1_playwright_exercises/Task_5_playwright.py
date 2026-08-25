from playwright.sync_api import sync_playwright, expect


BASE_URL = "https://practicesoftwaretesting.com/"


with sync_playwright() as p:

    browser = p.chromium.launch(headless=False)
    page = browser.new_page()


    page.goto(BASE_URL)
    page.wait_for_timeout(2000)
    print("Application opened")

    sign_in = page.locator('a[href="/auth/login"]')

    expect(sign_in).to_be_visible()

    sign_in.click()

    page.wait_for_timeout(1500)

    print("Login page opened")


    email = page.locator("[data-test='email']")
    password = page.locator(
        "[data-test='password']"
    )

    expect(email).to_be_visible()
    expect(password).to_be_visible()

    print("Email and password fields are visible")


    print("\n--- TEST 1: VALID CREDENTIALS ---")

    email.fill("vivek.np@matodata.com")
    password.fill("Viveknp@2108")

    login_button = page.get_by_role(
        "button",
        name="Login"
    )

    expect(login_button).to_be_visible()

    login_button.click()

    page.wait_for_timeout(2000)


    # Verify login succeeded

    expect(page).not_to_have_url(
        "https://practicesoftwaretesting.com/auth/login"
    )

    print("Valid credentials accepted")
    print("VALID LOGIN TEST PASSED")



    print("\n--- TEST 2: INVALID PASSWORD ---")

    page.goto(
        BASE_URL + "auth/login"
    )

    page.wait_for_timeout(1500)

    email = page.locator(
        "[data-test='email']"
    )

    password = page.locator(
        "[data-test='password']"
    )

    email.fill("vnpviveknp@gmail.com")

    password.fill("WrongPassword123")

    login_button = page.get_by_role(
        "button",
        name="Login"
    )

    login_button.click()

    page.wait_for_timeout(2000)


    # Verify login failed

    expect(page).to_have_url(
        "https://practicesoftwaretesting.com/auth/login"
    )

    print("Login failed with invalid password")
    print("INVALID PASSWORD TEST PASSED")



    print("\n--- TEST 3: INVALID EMAIL ---")

    page.goto(
        BASE_URL + "auth/login"
    )

    page.wait_for_timeout(1500)

    email = page.locator(
        "[data-test='email']"
    )

    password = page.locator(
        "[data-test='password']"
    )

    email.fill("invaliduser@example.com")

    password.fill("SomePassword123")

    login_button = page.get_by_role(
        "button",
        name="Login"
    )

    login_button.click()

    page.wait_for_timeout(2000)


    # Verify login failed

    expect(page).to_have_url(
        "https://practicesoftwaretesting.com/auth/login"
    )

    print("Login failed with invalid email")
    print("INVALID EMAIL TEST PASSED")



    print("\n--- TEST 4: EMPTY CREDENTIALS ---")

    page.goto(
        BASE_URL + "auth/login"
    )

    page.wait_for_timeout(1500)

    email = page.locator(
        "[data-test='email']"
    )

    password = page.locator(
        "[data-test='password']"
    )

    # Leave fields empty

    login_button = page.get_by_role(
        "button",
        name="Login"
    )

    login_button.click()

    page.wait_for_timeout(1000)


    # Verify validation

    expect(
        page.get_by_text("Email is required")
    ).to_be_visible()

    expect(
        page.get_by_text("Password is required")
    ).to_be_visible()

    print("Validation messages displayed")
    print("EMPTY CREDENTIALS TEST PASSED")


    page.wait_for_timeout(5000)

    browser.close()
