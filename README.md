# Mattermost Test Suite

Playwright automation tests for Mattermost community server.

## Quick Start
1. Install: `pip install playwright && playwright install`
2. Update `EMAIL` and `PASSWORD` in test files
3. Run: `python test_auth.py`

## Tests
- **TC-01-05**: Authentication (login/logout/password validation)
- **TC-06-08**: Channel management (create/join channels)
- **TC-09-12**: Messaging (send/edit/delete/DM)
- **TC-13-18**: Non-functional (upload/search/performance/API)

> Note: Demo server limitations may affect some test cases (e.g., public channel creation).
