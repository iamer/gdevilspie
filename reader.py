import parser

# open a file and pass it to parser.py
foo = open('test.ds')
z = parser.parse_file(foo)
# clean some of the parser crap
rule = z[0]

#the dicts we will use
matdict = {}
actiondict = {}

#the reader part...
if rule[0] == 'if':
    matcond = z[0][1]
    action = z[0][2]

print matcond
print action

for item in matcond:
    if item[0] == 'is':
        matdict[str(item[1].pop())] = str(item[2])


if action[0] == 'begin':
    actiondict['actions'] = action[1:]
else:
    actiondict['actions'] = action[0]

print matdict
print actiondict
