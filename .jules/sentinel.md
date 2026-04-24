## 2026-04-24 - [Command Injection via Regex newline in package names]
**Vulnerability:** The `is_valid_package_name` validation in `adb_operations.py` uses `$` in regex matching instead of `\Z`.
**Learning:** In Python's `re.match`, `$` matches the end of the string OR just before a newline at the end. This allows an attacker to append `
<malicious_command>` to a valid package name, which `re.match` will accept, leading to command injection when the string is later used in shell commands.
**Prevention:** Use `\Z` instead of `$` to strictly enforce matching until the absolute end of the string, which refuses the trailing newline.
