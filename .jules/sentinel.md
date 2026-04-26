## 2024-04-25 - Regex Newline Command Injection
**Vulnerability:** The package name validation regex in `is_valid_package_name` used the `$` anchor, which allowed trailing newlines to bypass validation. This enabled potential command injection via appending commands after a newline, like `com.example.app\nrm -rf /`.
**Learning:** In Python's `re.match` (and many regex engines), `$` matches the end of the string OR just before a newline at the end of the string.
**Prevention:** Use `\Z` instead of `$` to strictly match the absolute end of the string, preventing trailing newline bypasses. Also, ensure there's only one source of truth for validation functions to avoid missing a fix in duplicates.
