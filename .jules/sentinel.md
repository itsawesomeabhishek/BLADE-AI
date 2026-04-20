## 2024-05-24 - Command Injection via Regex $ Anchor
**Vulnerability:** The package name validation regex used `$` which matches before a trailing newline, allowing command injection via strings like `com.example.app\nrm -rf /`.
**Learning:** Python's `re.match` with `$` is vulnerable to newline injection.
**Prevention:** Always use `\Z` to strictly match the absolute end of the string when validating input for shell commands.
