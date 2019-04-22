import os
import random
import uuid

placeArray = {"井冈山":{"poiID":10547264, "districtId": 171, "resourceId":137657}}
for p in placeArray:
    print(p)
    print(placeArray[p])
print(uuid.uuid4())
print(os.path.abspath('.'))

#createFile('广东','广州');
#print(COOKIES[random.choice(list(COOKIES))])