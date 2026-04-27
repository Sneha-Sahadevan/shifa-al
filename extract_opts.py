import re
import json

with open('store.html', 'r', encoding='utf-8') as f:
    text = f.read()

unique_texts = set()
for m in re.finditer(r'<div class="custom-(?:select|option)[^"]*"[^>]*>([^<]+)<img', text):
    content = m.group(1).strip()
    if content:
        unique_texts.add(content)

print(json.dumps(list(unique_texts), indent=2))
