# Confluence File Upload — pytest + Playwright

## Setup

```bash
python -m venv venv
source venv/bin/activate        # Windows: venv\Scripts\activate
pip install -r requirements.txt
playwright install chromium

cp .env.example .env            # fill in sandbox URL, creds, a real test page ID
```

## Run

```bash
pytest                          # headless
pytest --headed                 # watch it run
pytest -k "invalid"             # run just the rejection test
pytest -v                       # verbose, shows each parameterized case
```

First run triggers the `storage_state_path` fixture in `conftest.py` — logs
into your sandbox once and saves `auth/storageState.json`. Every test after
reuses that session (regenerated only if it's over an hour old), so each
test opens straight on the target page, already authenticated.

## Structure

```
conftest.py              # session login + storage_state reuse, page/context fixtures
pytest.ini                # tracing/screenshot/video config
tests/
  test_file_upload.py     # valid upload, invalid rejection, parameterized 3-type bonus
test-data/
  valid/sample.txt|.pdf|.png
  invalid/malicious.exe
auth/                     # storageState.json saved here after first login (gitignore this)
```

## What's covered

- Valid file upload → selection check → submit → success verification
- Invalid file type (`.exe`) → rejection verification (error shown, no success banner)
- Bonus: `@pytest.mark.parametrize` across `.txt`, `.pdf`, `.png`

## Notes for your sandbox

- Locator text in `open_upload_dialog()` (`more actions`, `Attachments`,
  `Upload files`) matches standard Confluence UI — tweak the regex if your
  version/theme uses different labels.
- Set `CONFLUENCE_TEST_PAGE_ID` in `.env` to a real page you can attach files to.
- Swap `malicious.exe` for whatever extension your sandbox's restricted list
  actually blocks, if it differs.
