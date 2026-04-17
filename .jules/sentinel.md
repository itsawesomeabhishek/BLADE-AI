## 2026-04-17 - [Command Injection via Regex `$`]
**Vulnerability:** Command injection in `is_valid_package_name` function using regex `$` instead of `\Z` to denote the end of string.
**Learning:** `re.match` with `$` matches just before the final newline, allowing command injection via `\n`.
**Prevention:** Use `\Z` to strictly enforce matching until the absolute end of the string when validating input.
