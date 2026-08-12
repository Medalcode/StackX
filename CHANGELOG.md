# Changelog

All notable changes to the **StackX** project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [1.1.0] - 2026-08-12

### Security
- Replaced direct string comparison in admin token validation with `secrets.compare_digest()` to eliminate timing attack vulnerabilities (`routes/admin.py`).

### Added
- Created `RecommendationService` (`backend/app/services/recommendation_service.py`) to encapsulate recommendation logic, AI justification generation, and team structure defaults.
- Added comprehensive unit tests for `RecommendationService` (`tests/test_recommendation_service.py`).
- Added unit tests for Sanity sync module (`tests/test_sanity_sync.py`).
- Added integration tests for paginated GET `/recommend-stack/` endpoint and admin token header variations (`tests/test_api.py`).
- Added pytest markers (`smoke`, `integration`) in `pyproject.toml`.
- Added Knowledge Graph generation support with `graphify`.

### Changed
- Refactored `routes/recommend.py` to act as a lightweight controller delegating to `RecommendationService`.
- Updated GitHub Actions CI workflow to lint and test both `backend/` and `tests/` directories.
- Updated `.gitignore` to exclude test coverage reports, pytest cache, and graphify output artifacts.

### Fixed
- Optimized `calculate_score_for_tech()` in `recommender.py` to short-circuit when `total_weights <= 0`.
- Removed redundant `load_all_skills()` call on module import in `ai_client.py`.
- Fixed missing project ID guard in `sanity_sync.py` to prevent background task crashes when `SANITY_PROJECT_ID` is unset.

---

## [1.0.0] - 2026-06-22

### Added
- Initial release of StackX full-stack recommendation engine.
- FastAPI backend with SQLAlchemy ORM and SQLite/PostgreSQL support.
- Next.js frontend with Tailwind CSS styling and slider inputs.
- AI Justification engine with Ollama fallback and Skill registry.
- Initial test suite and Docker Compose setup.
