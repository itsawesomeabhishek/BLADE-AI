## 2024-05-15 - Icon Button Accessibility

**Learning:** The application extensively uses `react-icons` wrapped in `<button>` and `<motion.button>` elements without explicit text content. While `title` attributes were present for tooltips, they do not sufficiently act as accessible names for screen readers in all contexts, making these critical actions (like copying, exporting, and sending) inaccessible to visually impaired users.

**Action:** Ensure that all future icon-only interactive elements in `ChatBot.tsx`, `FloatingChat.tsx`, and similar components explicitly include an `aria-label` attribute that matches or expands upon the `title` attribute.
