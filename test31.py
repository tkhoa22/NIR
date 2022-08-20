point = [1,2,2,3,4,2,4,4,5]

center = 0
for i in range(1,len(point)-1):
    if point[0] > point[i]:
        if point[0] <= point[i+1]:
            center = 0
        else:
            if point[i] <= point[i+1]:
                center = 1
            else:
                center = 2
    elif point[0] < point[i]:
        if point[0] >= point[i+1]:
            center = 0
        else:
            if point[i] <= point[i+1]: 
                center = 1
            else:
                center = 2
    else:
        center = 0
    print(center)
    print(point[0],point[i],point[i+1])
