#!/usr/bin/env python3
"""Remove #ifdef CONFIG_KSU ... #endif blocks from kernel source files."""
import re, sys

path = sys.argv[1]
with open(path, 'r') as f:
    content = f.read()

# Remove all #ifdef CONFIG_KSU ... #endif blocks (handles tabs/spaces)
# Must NOT match #ifdef CONFIG_KSU_SUSFS or similar
content = re.sub(
    r'[ \t]*#ifdef\s+CONFIG_KSU\s*\n'
    r'(?:(?!#ifdef\s+CONFIG_KSU)[^\n]*\n)*?'
    r'[ \t]*#endif\s*\n?',
    '', content, flags=re.MULTILINE
)

# Clean up excessive blank lines
content = re.sub(r'\n{3,}', '\n\n', content)

with open(path, 'w') as f:
    f.write(content)

print(f"Stripped KSU guards from {path}")
