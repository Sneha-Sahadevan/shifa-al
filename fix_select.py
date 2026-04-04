import re

with open('store.html', 'r', encoding='utf-8') as f:
    html = f.read()

def replace_select(match):
    options_text = match.group(1)
    opts = re.findall(r'<option>(.*?)</option>', options_text)
    
    if not opts: return match.group(0)
    
    img_tag = '<img src="assets/sar.jpeg" alt="SAR" style="height: 1em; width: auto; vertical-align: middle; margin-left: 3px; mix-blend-mode: multiply;">'
    
    def process_text(txt):
        return txt.replace(' SAR', img_tag).replace('SAR', img_tag)
    
    res = '<div class="custom-select-wrapper">\n'
    res += f'    <div class="custom-select">{process_text(opts[0])}</div>\n'
    res += '    <div class="custom-options">\n'
    for i, opt in enumerate(opts):
        selected = ' selected' if i == 0 else ''
        res += f'        <div class="custom-option{selected}">{process_text(opt)}</div>\n'
    res += '    </div>\n'
    res += '</div>'
    
    return res

new_html = re.sub(r'<select class="price-select">(.*?)</select>', replace_select, html, flags=re.DOTALL)

with open('store.html', 'w', encoding='utf-8') as f:
    f.write(new_html)
