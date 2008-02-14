import parser

foo = open('test.ds')
z = parser.parse_file(foo)
rule = z[0]

ruledict = {}

if rule[0] == 'if':
    matcond = z[0][1]
    action = z[0][2]

print matcond
print action

for item in matcond:
    if item[0] == 'is':
        ruledict[str(item[1])] = str(item[2])


if action[0] == 'begin':
    ruledict['actions'] = action[1:]
else:
    ruledict['actions'] = action[0]

print ruledict
