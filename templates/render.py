from jinja2 import Template

html = open("header.html").read()

template = Template(html)

print(template.render())