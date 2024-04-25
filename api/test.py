import re

example = 
pattern = r"`python(.*?)`"
match = re.findall(pattern, example, re.DOTALL)

print(match)