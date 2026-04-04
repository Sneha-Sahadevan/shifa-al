bad_string = '<img src="assets/sar.jpeg" alt="<img src="assets/sar.jpeg" alt="SAR" style="height: 1em; width: auto; vertical-align: middle; margin-left: 3px; mix-blend-mode: multiply;">" style="height: 1em; width: auto; vertical-align: middle; margin-left: 3px; mix-blend-mode: multiply;">'
good_string = '<img src="assets/sar.jpeg" alt="SAR" style="height: 1em; width: auto; vertical-align: middle; margin-left: 3px; mix-blend-mode: multiply;">'

# Also need to fix nested img tags inside custom-select and custom-options
import re

with open("store.html", "r", encoding="utf-8") as f:
    content = f.read()

# I am replacing exactly the bad string with good string
content = content.replace(bad_string, good_string)

with open("store.html", "w", encoding="utf-8") as f:
    f.write(content)
