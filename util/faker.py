from faker import Faker
import json
f=Faker()
words = []
for i in range(35):
    words.append(f.word())
t = []
for ik in range(10):
    res = {}
    for i in range(35):
        key = words[i]
        value = f.random_int()
        res[key] = value
    t.append(res)

with open("/Users/lac/PycharmProjects/algorithm_file_server/data/data1","w") as f:
    f.write(json.dumps(t))