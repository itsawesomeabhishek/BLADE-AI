## 2024-05-24 - React List Rendering Bottleneck
**Learning:** In a codebase dealing with potentially hundreds of items like Android packages, mapping inline components with complex styling and multiple child components inside a single `useState` array update causes severe render blocking.
**Action:** Always extract list items into separate components wrapped in `React.memo` and ensure callback references passed to them (like `toggleSelect`) are stabilized using `useCallback` and `useRef` to hold latest state without triggering re-renders of the parent function.
## 2024-05-24 - AI Package Scanning Bottleneck
**Learning:** Re-evaluating lists or compiling regexes on every package check in `_is_likely_bloatware` within the Python backend causes a significant performance overhead when scanning thousands of installed Android packages.
**Action:** Always extract static indicator arrays into class-level pre-compiled regex objects (`re.compile`) and exact-match exclusions into `frozenset` objects to achieve O(1) lookups and significantly faster substring matching.
## 2024-05-25 - Python String Parsing Overhead
**Learning:** In Python backend scripts (e.g., `adb_operations.py`), iterating over large command outputs using `str.split('\n')` and modifying strings with `.replace()` and `.split('.')` inside loops introduces measurable overhead due to intermediate list allocations.
**Action:** Always prefer `str.splitlines()` in list comprehensions combined with string slicing (e.g., `line[8:]`) and `str.find()` with slice indexing (`name[:dot_idx]`) for significantly faster string manipulation and parsing.
## 2024-05-26 - ADB Subprocess Bottleneck
**Learning:** Executing sequential Python `subprocess.run` calls to fetch individual Android device properties via `adb shell getprop` introduces significant performance overhead due to repeated adb server round-trips and process spawning (e.g., 10-15ms vs 2-3ms).
**Action:** Always batch multiple ADB shell commands into a single `subprocess.run` execution using shell separators (`;`) to minimize connection and process overhead, while ensuring outputs are safely padded and parsed.
## 2024-05-27 - React Search Filtering Bottleneck
**Learning:** In React components like `PackageList` that filter large arrays of items (like thousands of installed packages) based on user input, synchronous array operations (`toLowerCase().includes()`) block the main UI thread during rapid typing, causing noticeable input lag.
**Action:** Always wrap high-frequency search input states used in expensive filtering operations with `useDeferredValue` to yield to the browser's main thread and keep the input highly responsive, allowing the expensive re-render and calculation to occur in the background.
