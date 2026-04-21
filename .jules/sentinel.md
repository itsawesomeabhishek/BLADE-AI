## YYYY-MM-DD - [Newline Injection in Regex]
**Vulnerability:** Command Injection Bypass using Newline
**Learning:** Python's `re.match` with the `$` anchor matches right before a single trailing newline. In an `adb shell` context, if a package name input contains a newline (`com.android.settings\n`), it passes validation but can potentially execute trailing commands if poorly sanitized down the line.
**Prevention:** Use the `\Z` anchor in Python regular expressions for strict end-of-string matching when validating string structures for injection prevention.
