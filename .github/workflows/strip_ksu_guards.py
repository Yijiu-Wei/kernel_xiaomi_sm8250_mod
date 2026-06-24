#!/usr/bin/env python3
"""Remove #ifdef CONFIG_KSU ... #endif blocks from kernel source files.
Safely handles multiple blocks, indentation, and does NOT match CONFIG_KSU_SUSFS."""
import re, sys

path = sys.argv[1]
with open(path, 'r') as f:
    content = f.read()

# Remove #ifdef CONFIG_KSU ... #endif blocks
# Must NOT match #ifdef CONFIG_KSU_SUSFS, #ifdef CONFIG_KSU_DEBUG etc.
# Uses negative lookahead to ensure line starts with #ifdef CONFIG_KSU (exact)
# and handles possible indentation
lines = content.split('\n')
result = []
in_block = False
removed = 0

for line in lines:
    stripped = line.strip()
    if re.match(r'^#ifdef\s+CONFIG_KSU$', stripped) and not re.match(r'^#ifdef\s+CONFIG_KSU_SUSFS', stripped):
        in_block = True
        removed += 1
        continue
    if in_block and re.match(r'^#endif', stripped):
        in_block = False
        continue
    if not in_block:
        result.append(line)

# Also remove blocks where #ifdef is indented (inside functions)
content = '\n'.join(result)

# Try regex for remaining inline blocks
content = re.sub(
    r'[ \t]+#ifdef\s+CONFIG_KSU\s*\n'
    r'(?:(?!#ifdef)[^\n]*\n)*?'
    r'[ \t]*#endif[ \t]*\n?',
    '', content, flags=re.MULTILINE
)

# Clean up excessive blank lines
content = re.sub(r'\n{3,}', '\n\n', content)

with open(path, 'w') as f:
    f.write(content)

print(f"Removed {removed} KSU guard block(s) from {path}")
