import os
import random

placeArray = [{"poiID":10547264, "districtId": 171, "resourceId":137657, "name":"井冈山"}]
print(placeArray[0]['poiID'])
placeArray[0]['poiID'] = 1111111
print(placeArray)

print(os.path.abspath('.'))
#createFile('广东','广州');
#print(COOKIES[random.choice(list(COOKIES))])