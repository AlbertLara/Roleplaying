import json
envfile = '../configuration/.env.dev'

file = open(envfile)
data = file.read().splitlines()
file.close()
obj = {}
for row in data:
    row_line = row.split("=")
    key = row_line[0]
    value = row_line[1]
    obj[key] = value

print(obj)

outfile = open('./services/web/project/config/settings.json','w')
json.dump(obj,outfile)
outfile.close()