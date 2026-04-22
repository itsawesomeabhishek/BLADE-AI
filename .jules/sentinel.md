## 2024-05-24 - [Strict regex matching]
**Vulnerability:** Command injection / Bypass validation using trailing newline due to `$` regex anchor.
**Learning:** `$` in Python's `re.match` matches the end of the string OR the position just before a trailing newline (`\n`). This allows inputs with trailing newlines to bypass strict format validation and inject commands if used in shells or cause issues.
**Prevention:** Use `\Z` instead of `$` for matching the absolute end of strings in strict validation.
