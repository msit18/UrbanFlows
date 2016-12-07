with open('480p_3fps_FR90.txt') as f:
	content = f.readlines()

content = [x.strip('.jpg\n') for x in content]

print content

print type(content[0]) is int
print type(content[0]) is str
print type(content) is list

thing = sorted(content)

print thing

# file = open("newFile.txt", 'w')
# for x in range(len(thing)):
# 	file.write("{0}\n".format(thing[x]))


array = []
for x in range(len(thing)-1):
	diff = int(thing[x+1])-int(thing[x])
	array.append(diff)

print array