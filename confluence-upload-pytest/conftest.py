"""
Shared pytest fixtures for the Confluence file-upload test suite.

Handles ONE-TIME login to the local/test Confluence sandbox and reuses
that authenticated session (storage_state) across every test — so
individual tests never need to log in themselves, they land straight
on the target page.

Env vars required (see .env.example):
    CONFLUENCE_BASE_URL
    CONFLUENCE_USERNAME
    CONFLUENCE_PASSWORD
    CONFLUENCE_TEST_PAGE_ID
"""
import os
import time
import pytest
from pathlib import Path
from dotenv import load_dotenv
from playwright.sync_api import sync_playwright

load_dotenv()

BASE_URL = os.environ.get("CONFLUENCE_BASE_URL", "http://localhost:8090")
USERNAME = os.environ.get("CONFLUENCE_USERNAME")
PASSWORD = os.environ.get("CONFLUENCE_PASSWORD")
PAGE_ID = os.environ.get("CONFLUENCE_TEST_PAGE_ID", "1")

AUTH_DIR = Path(__file__).parent / "auth"
STORAGE_STATE_PATH = AUTH_DIR / "storageState.json"
TEST_DATA_DIR = Path(__file__).parent / "test-data"

MAX_SESSION_AGE_SECONDS = 60 * 60  # 1 hour — avoid re-login on every local run


@pytest.fixture(scope="session")
def base_url():
    return BASE_URL


@pytest.fixture(scope="session")
def page_id():
    return PAGE_ID


@pytest.fixture(scope="session")
def valid_files():
    return {
        "txt": TEST_DATA_DIR / "valid" / "sample.txt",
        "pdf": TEST_DATA_DIR / "valid" / "sample.pdf",
        "png": TEST_DATA_DIR / "valid" / "sample.png",
    }


@pytest.fixture(scope="session")
def invalid_file():
    return TEST_DATA_DIR / "invalid" / "malicious.exe"


@pytest.fixture(scope="session")
def storage_state_path():
    """
    Logs into the sandbox ONCE per test session and saves the authenticated
    session to auth/storageState.json. Reused (not regenerated) if the file
    already exists and is under an hour old — speeds up repeated local runs.
    """
    AUTH_DIR.mkdir(exist_ok=True)

    if STORAGE_STATE_PATH.exists():
        age = time.time() - STORAGE_STATE_PATH.stat().st_mtime
        if age < MAX_SESSION_AGE_SECONDS:
            return str(STORAGE_STATE_PATH)

    if not USERNAME or not PASSWORD:
        raise RuntimeError(
            "Missing CONFLUENCE_USERNAME / CONFLUENCE_PASSWORD env vars. "
            "Set them (see .env.example) before running tests."
        )

    with sync_playwright() as p:
        browser = p.chromium.launch()
        page = browser.new_page()
        page.goto(f"{BASE_URL}/login.action")

        # Standard Confluence login form field ids — adjust if your sandbox theme differs.
        page.fill("#os_username", USERNAME)
        page.fill("#os_password", PASSWORD)
        page.click("#loginButton")

        # Wait for a reliable post-login element (dashboard header / profile menu).
        page.wait_for_selector(
            "#header-menu, [data-testid='ProfileMenu'], #app-header",
            timeout=15_000,
        )

        page.context.storage_state(path=str(STORAGE_STATE_PATH))
        browser.close()

    return str(STORAGE_STATE_PATH)


@pytest.fixture
def context(browser, storage_state_path):
    """
    Overrides pytest-playwright's default `context` fixture to load the
    saved session — every test gets an already-logged-in browser context.
    """
    ctx = browser.new_context(storage_state=storage_state_path)
    yield ctx
    ctx.close()


@pytest.fixture
def page(context, base_url, page_id):
    """
    Overrides the default `page` fixture: opens straight on the target
    Confluence page, already authenticated via the reused session.
    """
    pg = context.new_page()
    pg.goto(f"{base_url}/pages/viewpage.action?pageId={page_id}")
    yield pg
    pg.close()
