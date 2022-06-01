import json

async def read(filename):
  with open(filename,'r') as file:
    return json.load(file)

async def write(filename,value):
  with open(filename,'w') as file:
    json.dump(value,file,indent=4)