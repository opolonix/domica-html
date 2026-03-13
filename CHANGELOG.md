# Changelog

## 0.1.4 - 2026-03-13

- Finalized the synchronous `0.1.x` line before planned async work in `0.2.0`.
- Restored Python 3.9-compatible type syntax in the codebase.
- Fixed `ContextVar` stack initialization for node parenting.
- Fixed `unpin_from_parent()` to return the previous parent correctly.
- Escaped HTML attribute values during rendering.
- Expanded the package public exports and corrected `__all__`.
- Added regression tests for rendering, context handling, and public API exports.
