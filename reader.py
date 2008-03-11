import parser

# open a file and pass it to parser.py
foo = open('test3.ds')
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

def not_checker(matdict,item):
	if item[0] == 'is':
		matdict[str(item[1].pop())] = ["is","not", str(item[2])]
	elif item[0] == 'matches':
		matdict[str(item[1].pop())] = ["matches","not", str(item[2])]
	elif item[0]== 'contains':
		matdict[str(item[1].pop())] = ["contains","not", str(item[2])]
    
def condition_checker(matdict,item):    
	if item[0] == 'is':
		matdict[str(item[1].pop())] = ["is", str(item[2])]
	elif item[0] == 'matches':
		matdict[str(item[1].pop())] = ["matches", str(item[2])]
	elif item[0]== 'contains':
		matdict[str(item[1].pop())] = ["contains", str(item[2])]
	elif item[0]== "not":
		not_checker(matdict,item[1])

if matcond[0] == "and":
	for item in matcond:
		condition_checker(matdict, item)
else:
	condition_checker(matdict, matcond)
		

if action[0] == 'begin':
	#FIXME: Handle Actions correctly.
	for i in action[1:]:
		print i
		if len(i) > 1:
			actiondict[i[0]] = i[1]
		else:
			actiondict [i[0]] = "True"
else:
    actiondict['actions'] = action[0]

print matdict
print actiondict
