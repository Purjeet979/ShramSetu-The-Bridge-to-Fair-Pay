import os, re

backend_dir = r'e:\WageVerificationSystem\templates'
frontend_dir = r'D:\Downloads\frontened'
files = [f for f in os.listdir(backend_dir) if f.endswith('.html')]

broken = []
for f in files:
    with open(os.path.join(backend_dir, f), 'r', encoding='utf-8') as cb:
        back_data = cb.read()
    with open(os.path.join(frontend_dir, f), 'r', encoding='utf-8') as cf:
        front_data = cf.read()
    
    # Check Jinja logic {%, {{
    back_jinja = re.findall(r'(\{%[^%]+%\}|\{\{[^}]+\}\})', back_data)
    front_jinja = re.findall(r'(\{%[^%]+%\}|\{\{[^}]+\}\})', front_data)
    
    # Check form inputs
    back_inputs = re.findall(r'name=[\"\\']([a-zA-Z0-9_]+)[\"\\']', back_data)
    front_inputs = re.findall(r'name=[\"\\']([a-zA-Z0-9_]+)[\"\\']', front_data)
    
    if set(back_jinja) != set(front_jinja):
        broken.append(f + ' (jinja)')
    if set(back_inputs) != set(front_inputs):
        broken.append(f + ' (inputs)')

if broken:
    print('Broken Backend Contracts:', broken)
else:
    print('All Backend Contracts Preserved perfectly by teammate!')
