import re
import os

def clean_inline_styles():
    file_path = "doctors.html"
    if not os.path.exists(file_path):
        return
        
    with open(file_path, "r", encoding="utf-8") as f:
        content = f.read()
    
    # Remove style="background-color: ...;" from card-header and img-wrapper
    new_content = re.sub(r'(class="(?:card-header|img-wrapper)".*?)style="background-color:.*?"', r'\1', content)
    # Also handle the other order
    new_content = re.sub(r'style="background-color:.*?"(.*?class="(?:card-header|img-wrapper)")', r'\1', new_content)

    with open(file_path, "w", encoding="utf-8") as f:
        f.write(new_content)
    print("Cleaned inline styles from doctors.html.")

if __name__ == "__main__":
    clean_inline_styles()
