import re

html_path = r'c:\Users\SNEHA SAHADEVAN\OneDrive\Desktop\shifa al\doctors.html'
with open(html_path, 'r', encoding='utf-8') as f:
    html = f.read()

timing_updates = {
    "Dr. Kazmeen Afroz": "FROM 3 PM TO 11 AM",
    "Dr. Hanadi Dolani": "FROM 4 PM TO 12 PM",
    "Dr. Fathima Patel": "FROM 4 PM TO 12 PM",
    "Dr. Arshiya Tabasssum": "FROM 8 AM TO 4 PM",
    "Dr. Rehab Ghunaim": "FROM 8 AM TO 4 PM",
    "Dr. Sumayya Attar": "FROM 8 AM TO 4 PM",
    "Dr. Khaleed Baqeel": "FROM 8 AM TO 4 PM",
    "Dr. Dina Harbi": "FROM 4 PM TO 12 PM",
    "Dr. Rimas Alhibb": "FROM 4 PM TO 12 PM",
    "Dr. Mohamed Mustafa": "FROM 4 PM TO 12 PM",
    "Dr. Thahseen Shah": "FROM 3 PM TO 11 AM",
    "Dr. Nabila Faisal": "FROM 9 AM TO 12 PM &amp; FROM 5 PM TO 10 PM",
    "Dr. Murhaf Alaskari": "FROM 9 AM TO 12 PM &amp; FROM 5 PM TO 10 PM",
    "Dr. Sabri Mohammed": "FROM 9 AM TO 12 PM &amp; FROM 5 PM TO 10 PM",
    "Dr. Mohamed Tariq": "FROM 9 AM TO 12 PM &amp; FROM 4:30 PM TO 9:30 PM",
    "Dr. Mohammed Taha": "FROM 9 AM TO 12 PM &amp; FROM 5 PM TO 10 PM",
    "Dr. Zainul Abedeen": "FROM 9 AM TO 1 PM &amp; FROM 5 PM TO 9 PM",
    "Dr. Hina Usman": "FROM 4 PM TO 12 AM",
    "Dr. Mohamed Abubaker": "FROM 9 AM TO 12 PM &amp; FROM 5 PM TO 10 PM",
    "Dr. Eman Elsaid": "FROM 10 AM TO 12 PM &amp; FROM 5 PM TO 11 PM",
    "Dr. Khidir Elhadi Babiker": "FROM 9 AM TO 12 PM &amp; FROM 5 PM TO 10 PM",
    "Dr. Arif Nazeer": "FROM 8 AM TO 9 PM",
    "Dr. Shaikh Eklakh": "FROM 4 PM TO 12 PM",
    "Dr. Ejaz Ahmed": "FROM 4 PM TO 12 PM",
    "Dr. Sherin Hameed": "FROM 8 AM TO 4 PM",
    "Dr. Wamiq Akhtar": "FROM 9 AM TO 12 PM &amp; FROM 5 PM TO 10 PM",
    "Dr. Irshad Ahmed": "FROM 12 AM TO 8 AM"
}

for name, timing in timing_updates.items():
    pattern = re.compile(rf'(<h3 class="practitioner-name">\s*{re.escape(name)}\s*</h3>.*?<div class="practitioner-schedule">).*?(</div>)', flags=re.IGNORECASE | re.DOTALL)
    html, count = pattern.subn(rf'\g<1>{timing}\g<2>', html)

with open(html_path, 'w', encoding='utf-8') as f:
    f.write(html)
print("Updated timings successfully")
