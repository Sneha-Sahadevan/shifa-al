with open('doctors.html', 'r', encoding='utf-8') as f:
    lines = f.readlines()
    for i, line in enumerate(lines):
        if 'dept-title' in line or 'dept-arabic' in line:
            # Only print lines that contain 'DERMATOLOGY' (case insensitive)
            if 'DERMATOLOGY' in line.upper() or 'الجلدية' in line:
                 print(f"{i+1}: {line.strip().encode('ascii', 'ignore').decode()}")
