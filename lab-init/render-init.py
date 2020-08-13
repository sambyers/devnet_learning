from jinja2 import Template

with open('router-init.ios', 'r') as f:
    t = f.read()
template = Template(t)
for i in range (1,11):
    r = template.render(hostname = f'R{i}')
    with open (f'configs/R{i}.ios', 'w') as f:
        f.write(r)