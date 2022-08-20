import math
def cross_product(A,B):
    ###Перекрестный продукт A.B
    return {"x": A["y"]*B["z"] - A["z"]*B["y"], "y": A["z"]*B["x"] - A["x"]*B["z"], "z": A["x"]*B["y"] - A["y"]*B["x"]}

def is_Equal(list1,n):
    # so sáng số và dict (tạo độ hoặc các dict đơn giản tương tự ) 
    if type(list1[0]) is not dict:
        for i in range(len(list1)):
            if abs(list1[0] - list1[i]) >= 10**-n:
                return False    
    else:
        key = list1[0].keys()
        for i in range(len(list1)):
            if key != list1[i].keys():
                return False
            else:
                for j in key:
                    if abs(list1[0][j] - list1[i][j]) >= 10**-n:
                        return False
    return True
def line(input1):
    #расположить вершины по сторонам 
    result = []
    for i in range(len(input1)):
        if i != len(input1) - 1:
            result.append([input1[i],input1[i+1]])
        else:
            result.append([input1[i],input1[0]])
    return result

def check_out_or_in_polygon (X,normal_plane,polygon):
    def sum_dict_key(input1,key):
        sum1 = 0
        for i in range(len(input1)):
            sum1+=input1[i][key]
        return sum1

    if normal_plane["z"]!=0:
        center = {"x":sum_dict_key(polygon,"x")/len(polygon),"y":sum_dict_key(polygon,"y")/len(polygon)}
        def check_side_GH (E,F,G,H):
            check = ((G["y"] - H["y"])*(E["x"] - G["x"]) + (H["x"] - G["x"])*(E["y"] - G["y"]))*((G["y"] - H["y"])*(F["x"] - G["x"]) + (H["x"] - G["x"])*(F["y"] - G["y"]))
            if  check >= 0:
                return 1
            else:
                return 0
    else:
        if normal_plane["x"]!=0:
            center = {"y":sum_dict_key(polygon,"y")/len(polygon),"z":sum_dict_key(polygon,"z")/len(polygon)}
            def check_side_GH (E,F,G,H):
                check = ((G["y"] - H["y"])*(E["z"] - G["z"]) + (H["z"] - G["z"])*(E["y"] - G["y"]))*((G["y"] - H["y"])*(F["z"] - G["z"]) + (H["z"] - G["z"])*(F["y"] - G["y"]))
                if  check >= 0:
                    return 1
                else:
                    return 0
        else:
            center = {"x":sum_dict_key(polygon,"x")/len(polygon),"z":sum_dict_key(polygon,"z")/len(polygon)}
            def check_side_GH (E,F,G,H):
                check = ((G["x"] - H["x"])*(E["z"] - G["z"]) + (H["z"] - G["z"])*(E["x"] - G["x"]))*((G["x"] - H["x"])*(F["z"] - G["z"]) + (H["z"] - G["z"])*(F["x"] - G["x"]))
                if  check >= 0:
                    return 1
                else:
                    return 0

    line1 = line(polygon)
    i = 0
    a = 1
    while i < len(polygon) and a!=0 :
        a = check_side_GH(X,center,line1[i][0],line1[i][1])
        i+=1
    if a == 1:
        return "in"
    else:
        return "out"


def lineAB_lineCD(A,B,C,D):
    ###точка пересечения двух прямых лилии на плоскости

    def coincide():
        point = []
        if (A["x"]-D["x"])*(A["x"]-C["x"])<=0:
            point.append(A)
        if (B["x"]-D["x"])*(B["x"]-C["x"])<=0:
            point.append(B)
        if (C["x"]-A["x"])*(C["x"]-B["x"])<0:
            point.append(C)
        if (D["x"]-A["x"])*(D["x"]-B["x"])<0:
            point.append(D)
        return point

    u_AB = {"x":B["x"] - A["x"],"y":B["y"] - A["y"],"z":B["z"] - A["z"]}
    u_CD = {"x":D["x"] - C["x"],"y":D["y"] - C["y"],"z":D["z"] - C["z"]}
    u_AC = {"x":C["x"] - A["x"],"y":C["y"] - A["y"],"z":C["z"] - A["z"]}

    if is_Equal([cross_product(u_AB,u_CD),{"x":0,"y":0,"z":0}],5) is True :
        if is_Equal([cross_product(u_AB,u_AC),{"x":0,"y":0,"z":0}],5) is True :
            #trùng nhau
            return coincide()
        else:   
            #song song
            return {"x": "un", "y": "un", "z": "un"}
    else:
        #cắt nhau
        if is_Equal([0,u_AB["x"],u_CD["x"]],5) is True:
            t = (- u_CD["y"]*u_AC["z"] + u_CD["z"]*u_AC["y"])/(- u_AB["z"]*u_CD["y"] + u_CD["z"]*u_AB["y"])
        else:
            if is_Equal([0,u_AB["y"],u_CD["y"]],5) is False:
                t = (- u_CD["y"]*u_AC["x"] + u_CD["x"]*u_AC["y"])/(- u_AB["x"]*u_CD["y"] + u_CD["x"]*u_AB["y"])
            else:
                t = (- u_CD["z"]*u_AC["x"] + u_CD["x"]*u_AC["z"])/(- u_AB["x"]*u_CD["z"] + u_CD["x"]*u_AB["z"])

    point = {"x": A["x"] + t*u_AB["x"],"y": A["y"] + t*u_AB["y"],"z":A["z"] + t*u_AB["z"]}
    if (point["x"]-A["x"])*(point["x"]-B["x"])>0 or (point["y"]-A["y"])*(point["y"]-B["y"])>0:
        return {"x": "un", "y": "un", "z": "un"}
    if (point["x"]-C["x"])*(point["x"]-D["x"])>0 or (point["y"]-C["y"])*(point["y"]-D["y"])>0:
        return {"x": "un", "y": "un", "z": "un"}
    return point

def filter_point(Zp,P,normal_plane):
    #найти общий многоугольник двух многоугольников
    print("filter_point.........loading")
    print("Z:",Zp,"P:",P)

    
    line_Zp = line(Zp)#khi line_1
    line_P = line(P)# khi line_2
    points = [] # các điểm cắt
    del_point = [] # các điểm trùng tong điểm cắt sẽ   

    def add_del_point(point):
        if len(del_point) > 0: # khi del_point có số thì kiểm tra xem có trùng
            i = 0
            while i < len(del_point) and point != del_point[i][1]:
                i+=1
            if i == 0 and is_Equal([point,del_point[0][1]],5) is False or i == len(del_point): # chưa tồn tại thì thêm vào del_point
                del_point.append([0,point])
        else: # thêm vào del_point do ko có del_point chưa có số nào
            del_point.append([0,point]) 
    

    #Шаг 1
    for i in range(len(line_Zp)):
        note_point = [0] #пересечение на отрезке множества Zp
        for j in range(len(line_P)):
            point = lineAB_lineCD(line_Zp[i][0],line_Zp[i][1],line_P[j][0],line_P[j][1])
            if point != {"x": "un", "y": "un", "z": "un"}: # True - две линии пересекаются, false - две линии не пересекаются
                if type(point) == dict: # Одно пересечение или Нет пересечения
                    if len(note_point) >= 2: # Если есть предыдущее пересечение, совпадает ли оно с этой точкой?
                        if is_Equal([note_point[1]["x"],point["x"]],5) is False or is_Equal([note_point[1]["y"],point["y"]],5) is False or is_Equal([note_point[1]["z"],point["z"]],5) is False: #  Одно пересечение 1
                            note_point.append(point)
                            note_point[0]+=1
                    else: 
                        note_point.append(point)
                        note_point[0]+=1
                    # Проверить, является ли пересечение вершиной двух вершин многоугольника Zp
                    if is_Equal([point,line_Zp[i][0]],5) is True or is_Equal([point,line_Zp[i][1]],5) is True: #ngăn trường hợp tứ giác 1 có điểm chung 
                        add_del_point(point)
                else: # Два пересечения
                    note_point = [0]
                    note_point.append(point[0])
                    note_point.append(point[1])
                    add_del_point(point[0])
                    add_del_point(point[1])
                    note_point[0]+=2
                    break
            if note_point[0] == 2:# Если есть две точки пересечения многоугольника P
                break
        points.append(note_point)
    print(points)
    #Шаг 2
    check_cut = 1
    index = 0
    while index < len(points):
        if points[index][0] != 0:
            check_cut = 0
            break
        index +=1
    if check_cut == 1:
        if check_out_or_in_polygon (Zp[0],normal_plane,P) == "in":
            print("filter_point.........finish")
            Zp.append({"status":"uncut"})
            return Zp
        elif check_out_or_in_polygon (P[0],normal_plane,Zp) == "in":
            print("filter_point.........finish")
            P.append({"status":"uncut"})
            return P
        else:
            print("filter_point.........finish") 
            return"đm có cái loz mà chiếu sáng được bố màysiu1"
    #Шаг 3
    cut = {"status":"uncut","i":0,"j":0}
    # i и j для определения вершины стороны многоугольника O
    index_cut = 0
    result = []
    for i in range(len(line_Zp)):
        if points[i][0] == 1:
            if len(points[i])>1:
                result.append(points[i][1])
            if check_out_or_in_polygon (line_Zp[i][1],normal_plane,P) == "in":
                result.append(line_Zp[i][1])
                if i < len(points) - 1:
                    points[i+1][0] += 1
                if index_cut == 0:
                    cut["status"] = "cut"
                    cut["i"]  = len(result) - 2
                    cut["j"]  = len(result) - 1
                    index_cut+= 1
        elif points[i][0] == 2:
            result.append(points[i][1])
            if len(points[i])>2:
                result.append(points[i][2])
            if index_cut == 0:
                cut["status"] = "cut"
                cut["i"] = len(result) - 2
                cut["j"] = len(result) - 1
                index_cut+= 1

    # Шаг 4
    for count in P:
        if check_out_or_in_polygon (count,normal_plane,Zp) == "in":
            result.append(count)
    # Шаг 5
    if len(del_point) >0:
        del_note =[]        
        for i in range(len(result)):
            for j in range(len(del_point)):
                if is_Equal([result[i],del_point[j][1]],5) is True:
                    if del_point[j][0]==0:
                        del_point[j][0]+=1
                    else:
                        del_note.append(i)
        for i in range(len(del_note)):
            result.pop(del_note[i] - i)
    #ending
    if len(result) < 3:
        print("filter_point.........finish")
        return "ko co diem trung"
    else:
        result.append(cut)
        print("filter_point.........finish")
        return result


def reorganize(point,normal_plane):
    #расположить точки обратно в последовательном порядке
    if type(point) == str:
        return "ko co diem trung"
    if point[-1]["status"] == "uncut":
        point.pop(len(point)-1)
        return point
    if normal_plane["z"]!=0:
        def check_side_GH (E,F,G,H):
            check = ((G["y"] - H["y"])*(E["x"] - G["x"]) + (H["x"] - G["x"])*(E["y"] - G["y"]))*((G["y"] - H["y"])*(F["x"] - G["x"]) + (H["x"] - G["x"])*(F["y"] - G["y"]))
            if  check >= 0:
                return 1
            else:
                return 0
    else:
        if normal_plane["x"]!=0:
            def check_side_GH (E,F,G,H):
                check = ((G["y"] - H["y"])*(E["z"] - G["z"]) + (H["z"] - G["z"])*(E["y"] - G["y"]))*((G["y"] - H["y"])*(F["z"] - G["z"]) + (H["z"] - G["z"])*(F["y"] - G["y"]))
                if  check >= 0:
                    return 1
                else:
                    return 0
        else:
            def check_side_GH (E,F,G,H):
                check = ((G["x"] - H["x"])*(E["z"] - G["z"]) + (H["z"] - G["z"])*(E["x"] - G["x"]))*((G["x"] - H["x"])*(F["z"] - G["z"]) + (H["z"] - G["z"])*(F["x"] - G["x"]))
                if  check >= 0:
                    return 1
                else:
                    return 0
    i = point[-1]["i"]
    j = point[-1]["j"]  
    A = point[i]
    B = point[j]
    index_new = []
    result = list(range(len(point)-1))
    sum1 = 0 # сумма порядка result (например, есть 5 ребер, затем 1,2,3,4,5, его сумма равна -2 -1 + 0 + 1 + 2)
    sum2 = 0 # сумма порядка result минус конечная точка от
    for x in range(len(point)-2):
        a = 0
        if x == i:
            index_new.append(-2)
            sum2-=2
        elif x == j:
            index_new.append(-1)
            sum2-=1
        else:
            for y in result:
                if y != x and y != i and y != j:
                    check = check_side_GH(B,point[y],A,point[x])
                    a += check
            index_new.append(a)
            sum2 += a
    for i in range(-2,len(point)-3):
        sum1 +=i
    index_new.append(sum1 - sum2)
    for x in range(len(point)-1):
        result[index_new[x] + 2]=point[x]
    return result

def polygon_area(points):
    #рассчитать площадь выпуклой многоугольной двери
    print("polygon_area..........loading")
    print("points:", points)
    if type(points) == str:
        return 0
    def triangle_area(A,B,C):
        c = math.sqrt((B["x"]-A["x"])*(B["x"]-A["x"]) + (B["y"]-A["y"])*(B["y"]-A["y"]) + (B["z"]-A["z"])*(B["z"]-A["z"]))
        a = math.sqrt((B["x"]-C["x"])*(B["x"]-C["x"]) + (B["y"]-C["y"])*(B["y"]-C["y"]) + (B["z"]-C["z"])*(B["z"]-C["z"]))
        b = math.sqrt((C["x"]-A["x"])*(C["x"]-A["x"]) + (C["y"]-A["y"])*(C["y"]-A["y"]) + (C["z"]-A["z"])*(C["z"]-A["z"]))
        p = (a + b + c)/2
        return math.sqrt(p*(p-a)*(p-b)*(p-c))
    area = 0
    for i in range(1,len(points)-1):
        area += triangle_area(points[0],points[i],points[i+1])
    return area
    print("polygon_area..........finish")



def line_and_sphere(A,u_1,radius):
    ###  пересечения линии и сферы
    if u_1 == {"x":0,"y":0,"z":0}:
        return {"x":0,"y":0,"z":0}
    t = math.sqrt((radius**2)/(u_1["x"]**2 + u_1["y"]**2 + u_1["z"]**2))
    return  {"x":A["x"]+u_1["x"]*t, "y":A["y"]+u_1["y"]*t, "z":A["z"]+u_1["z"]*t}   

def line_and_plane(point,u_1,normal_plane, point_plane):
    ###точка пересечения прямой и плоскости
    d1 = point_plane["x"]*normal_plane["x"] + point_plane["y"]*normal_plane["y"] + point_plane["z"]*normal_plane["z"]
    u_1xnormal = u_1["x"]*normal_plane["x"] + u_1["y"]*normal_plane["y"] + u_1["z"]*normal_plane["z"]
    d2 = point["x"]*normal_plane["x"] + point["y"]*normal_plane["y"] + point["z"]*normal_plane["z"]
    if is_Equal([u_1xnormal,0],5) is True :
        if is_Equal([d2,d1]) is True:
            return {"x":"8rolate90", "y":"8rolate90", "z":"8rolate90"}
        else:
            return {"x":"un", "y":"un", "z":"un"}
    t = (d1 - d2)/u_1xnormal
    x2 = u_1["x"]*t + point["x"]
    y2 = u_1["y"]*t + point["y"]
    z2 = u_1["z"]*t + point["z"]

    return {"x":x2, "y":y2, "z":z2}

def reflected_ray(incident_ray ,normal,n,n_1 = 0,n_2 = 0): 
    ###вектор направления отраженного луча солнечного света
    print ("reflected_ray..........loading")
    print("input = ", incident_ray,normal)
    if incident_ray["x"]*normal["x"] + incident_ray["y"]*normal["y"] + incident_ray["z"]*normal["z"] >=0 and n == 1:
        print ("reflected_ray..........finish")
        return {"reflected_ray": {"x": 0, "y": 0, "z": 0},"refracted_ray":{"x": 0, "y": 0, "z": 0}}
    e_1 = cross_product(incident_ray,normal) #произведение 2 векторов
    e_2 = cross_product(e_1,normal) 
    a = math.acos((incident_ray["x"]*normal["x"]+incident_ray["y"]*normal["y"]+incident_ray["z"]*normal["z"])/\
        ((incident_ray["x"]**2+incident_ray["y"]**2+incident_ray["z"]**2)*(normal["x"]**2+normal["y"]**2+normal["z"]**2)))
    tan_a = math.tan(a - 1.57079)
    k = (normal["x"]**2+normal["y"]**2+normal["z"]**2)*tan_a/(e_2["x"]**2+e_2["y"]**2+e_2["z"]**2)
    reflect = {"x": normal["x"]+k*e_2["x"], "y": normal["y"]+k*e_2["y"], "z": normal["z"]+k*e_2["z"]}
    if n == 1:
        print ("reflected_ray..........finish")
        return {"reflected_ray": reflect,"refracted_ray":{"x": 0, "y": 0, "z": 0}}
    if n == 2:
        sin_b = n_1*math.sin(a)/n_2
        if sin_b > 1 or sin_b < -1:
            print ("reflected_ray..........finish")
            return {"reflected_ray": reflect,"refracted_ray":{"x": 0, "y": 0, "z": 0}}
        b = math.asin(n_1*math.sin(a)/n_2)
        tan_b = math.tan(b)
        k = (normal["x"]**2+normal["y"]**2+normal["z"]**2)*tan_b/(e_2["x"]**2+e_2["y"]**2+e_2["z"]**2)
        refract = {"x": -normal["x"]+k*e_2["x"], "y": -normal["y"]+k*e_2["y"], "z": -normal["z"]+k*e_2["z"]}
        print ("reflected_ray..........finish")
        return {"reflected_ray": reflect,"refracted_ray":refract}


def convert_AB_to_CD(A,B,height,normal): #quen
    ###{A,B,height,normal} to {координаты 4 прямоугольных точек}
    n = {"x": B["x"] - A["x"], "y": B["y"] - A["y"], "z": B["z"] - A["z"]}
    u = cross_product(n,normal)
    print(u)
    D = line_and_sphere(A,u,height)
    C = line_and_sphere(B,u,height)
    print("C: ", C, "D: ", D)
    return {"C": C, "D": D}

def point_receiver(deliverer,receiver,normal_receiver,reflected_ray):
    ###световой проекции в плоскости
    print("point_receiver..........loading")
    print("de:", deliverer)
    print("re:",receiver)
    print("ray:",reflected_ray)
    check = reflected_ray["x"]*normal_receiver["x"] + reflected_ray["y"]*normal_receiver["y"] + reflected_ray["z"]*normal_receiver["z"]
    if check>= 0:
        return 0 
    
    a = reflected_ray["x"]*normal_receiver["x"] + reflected_ray["y"]*normal_receiver["y"] + reflected_ray["z"]*normal_receiver["z"] 
    b = math.sqrt(reflected_ray["x"]*reflected_ray["x"] + reflected_ray["y"]*reflected_ray["y"] + reflected_ray["z"]*reflected_ray["z"])
    c = math.sqrt(normal_receiver["x"]*normal_receiver["x"] + normal_receiver["y"]*normal_receiver["y"] + normal_receiver["z"]*normal_receiver["z"])
    n = a/(b*c)
    Zp = []
    
    for i in deliverer:
        Zp.append(line_and_plane(i,reflected_ray,normal_receiver,receiver[0]))

    t = filter_point(Zp,receiver,normal_receiver)
    if type(t) != str:
        print("point_receiver..........finish")
        return reorganize(t,normal_receiver)
    else:
        print("point_receiver..........finish")
        return t


def rotation_of_axes(point,normal_plane,point_O,point_in_Ox):
    #преобразовать координаты точки Oxyz ->Oxy(cần test)
    if normal_plane["x"] == normal_plane["z"] == 0:
        cos_a_xz = 1
        sin_a_xz = 0
    else:
        cos_a_xz = normal_plane["z"]/(math.sqrt(normal_plane["x"]*normal_plane["x"] + normal_plane["z"]*normal_plane["z"]))
        sin_a_xz = normal_plane["x"]/(math.sqrt(normal_plane["x"]*normal_plane["x"] + normal_plane["z"]*normal_plane["z"]))
    
    y2_np = normal_plane["y"]
    z2_np = -sin_a_xz*normal_plane["x"] + cos_a_xz*normal_plane["z"]
    x2_point_in_Ox = cos_a_xz*point_in_Ox["x"] + sin_a_xz*point_in_Ox["z"]
    y2_point_in_Ox = point_in_Ox["y"]
    z2_point_in_Ox = -sin_a_xz*point_in_Ox["x"] + cos_a_xz*point_in_Ox["z"]

    if  y2_np == z2_np == 0:
        cos_a_y2z2 = 1
        sin_a_y2z2 = 0
    else:
        cos_a_y2z2 = y2_np/(math.sqrt(y2_np*y2_np + z2_np*z2_np))
        sin_a_y2z2 = y2_np/(math.sqrt(y2_np*y2_np + z2_np*z2_np))
    
    x3_point_in_Ox = x2_point_in_Ox
    y3_point_in_Ox = sin_a_y2z2*y2_point_in_Ox + cos_a_y2z2*z2_point_in_Ox
    
    cos_2D = x3_point_in_Ox/(math.sqrt(x3_point_in_Ox*x3_point_in_Ox + y3_point_in_Ox*y3_point_in_Ox))
    sin_2D = y3_point_in_Ox/(math.sqrt(x3_point_in_Ox*x3_point_in_Ox + y3_point_in_Ox*y3_point_in_Ox))
    
    for i in range(len(point)):
        x2 = cos_a_xz*point[i]["x"] + sin_a_xz*point[i]["z"]
        y2 = y 
        z2 = -sin_a_xz*point[i]["x"] + cos_a_xz*point[i]["z"]

        x3 = x2
        y3 = cos_a_y2z2*y2 - sin_a_y2z2*z2
        z3 = sin_a_y2z2*y2 + cos_a_y2z2*z2

        x4 = x3 - point["x"]
        y4 = y3 - point["y"]

        x5 = cos_2D*x4 + sin_2D*y4
        y5 = -sin_2D*x4 + cos_2D*y4
        point_2.append({"x": x5,"y": y5})
    return point_2

def Energy_from_Mirror_in_PV(normal_Mirror,point_Mirror,normal_PV,point_PV ,refected_ray,I_Mirror,points):
    cos_n = (math.abs(refected_ray["x"]*normal_PV["x"]+refected_ray["y"]*normal_PV["y"]+refected_ray["z"]*normal_PV["z"]))/\
    (((refected_ray["x"]**2 + refected_ray["y"]**2 + refected_ray["z"]**2)**0.5)*((normal_PV["x"]**2 + normal_PV["y"]**2 + normal_PV["z"]**2)**0.5))

    A = (I_Mirror*cos_n*((refected_ray["x"]*normal_Mirror["x"]+refected_ray["y"]*normal_Mirror["y"]+refected_ray["z"]*normal_Mirror["z"])**2))/\
    (refected_ray["x"]**2 + refected_ray["y"]**2 + refected_ray["x"]**2)

    C = normal_Mirror["x"]*point_Mirror["x"] + normal_Mirror["y"]*point_Mirror["y"] + normal_Mirror["z"]*point_Mirror["z"]
    
    C_PV = normal_PV["x"]*point_PV["x"] + normal_PV["y"]*point_PV["y"] + normal_PV["z"]*point_PV["z"]
    
    E = 0

    if normal_PV["z"] != 0:
        # lấy x và y 
        B = (1 + normal_PV["x"]**2 + normal_PV["y"]**2)**0.5
        X_1 = normal_Mirror["x"] - normal_Mirror["z"]*normal_PV["x"]/normal_PV["z"]
        Y_1 = normal_Mirror["y"] - normal_Mirror["z"]*normal_PV["y"]/normal_PV["z"]
        C_1 = - C + normal_Mirror["z"]*C_PV/normal_PV["z"]
        def double_intergral_of_3point(start,end,a1,b1,a2,b2,type_1 = "y"):
            if start == end: 
                return 0
            def function_final(y,a,b):
                return (1/X_1)*(1/(X_1*a+Y_1))*(math.log(abs((X_1*a+Y_1)*y + X_1*b + C_1)))
            return -function_final(end,a2,b2) + function_final(start,a2,b2) + function_final(end,a1,b1) - function_final(start,a1,b1)

        def get_a(x_A,y_A,x_B,y_B):
            return (x_B - x_A)/(y_B - y_A)

        def get_b(x_A,y_A,x_B,y_B):
            return y_A*(x_A - x_B)/(y_B - y_A) + x_A

        for i in range(1,len(points)-1):
            #point[0],point[i],point[i+1]
            center = 0
            if points[0] > points[i]:
                if points[0] <= points[i+1]:
                    center = 0
                else:
                    if points[i] <= points[i+1]:
                        center = i
                    else:
                        center = i+1
            elif points[0] < points[i]:
                if points[0] >= points[i+1]:
                    center = 0
                else:
                    if points[i] <= points[i+1]: 
                        center = i
                    else:
                        center = i+1
            else:
                center = 0
            if center == 0:
                E += A*B*(abs(double_intergral_of_3points(points[0]["y"],points[i]["y"],get_a(points[0]["x"],points[0]["y"],points[i]["x"],points[i]["y"]),\
                    get_b(points[0]["x"],points[0]["y"],points[i]["x"],points[i]["y"]),get_a(points[i+1]["x"],points[i+1]["y"],points[i]["x"],points[i]["y"]),\
                    get_b(points[i+1]["x"],points[i+1]["y"],points[i]["x"],points[i]["y"]))) + abs(double_intergral_of_3points(points[0]["y"],points[i+1]["y"],\
                    get_a(points[0]["x"],points[0]["y"],points[i+1]["x"],points[i+1]["y"]),\
                    get_b(points[0]["x"],points[0]["y"],points[i+1]["x"],points[i+1]["y"]),\
                    get_a(points[i+1]["x"],points[i+1]["y"],points[i]["x"],points[i]["y"]),\
                    get_b(points[i+1]["x"],points[i+1]["y"],points[i]["x"],points[i]["y"]))))
            elif center == i:
                E += A*B*(abs(double_intergral_of_3points(points[0]["y"],points[i]["y"],get_a(points[0]["x"],points[0]["y"],points[i]["x"],points[i]["y"]),\
                    get_b(points[0]["x"],points[0]["y"],points[i]["x"],points[i]["y"]),get_a(points[i+1]["x"],points[i+1]["y"],points[i]["x"],points[i]["y"]),\
                    get_b(points[i+1]["x"],points[i+1]["y"],points[i]["x"],points[i]["y"]))) + abs(double_intergral_of_3points(points[i]["y"],points[i+1]["y"],\
                    get_a(points[i]["x"],points[i]["y"],points[i+1]["x"],points[i+1]["y"]),\
                    get_b(points[i]["x"],points[i]["y"],points[i+1]["x"],points[i+1]["y"]),\
                    get_a(points[i+1]["x"],points[i+1]["y"],points[i]["x"],points[i]["y"]),\
                    get_b(points[i+1]["x"],points[i+1]["y"],points[i]["x"],points[i]["y"]))))
            else:
                E += A*B*(abs(double_intergral_of_3points(points[0]["y"],points[i+1]["y"],get_a(points[0]["x"],points[0]["y"],points[i+1]["x"],points[i+1]["y"]),\
                    get_b(points[0]["x"],points[0]["y"],points[i+1]["x"],points[i+1]["y"]),get_a(points[i+1]["x"],points[i+1]["y"],points[i]["x"],points[i]["y"]),\
                    get_b(points[i+1]["x"],points[i+1]["y"],points[i]["x"],points[i]["y"]))) + abs(double_intergral_of_3points(points[i]["y"],points[i+1]["y"],\
                    get_a(points[i]["x"],points[i]["y"],points[i+1]["x"],points[i+1]["y"]),\
                    get_b(points[i]["x"],points[i]["y"],points[i+1]["x"],points[i+1]["y"]),\
                    get_a(points[i+1]["x"],points[i+1]["y"],points[i]["x"],points[i]["y"]),\
                    get_b(points[i+1]["x"],points[i+1]["y"],points[i]["x"],points[i]["y"]))))
        return E

def Irradience_on_surface( I_sun, Area, Azimuth_sun_and_ray , Altitude_sun_and_normal, Azimuth_sur = 0, Altitude_sur = 0,coor = 0):
    # 0 - декартова ,1 - горизонтальная
    print("Irradience_on_surface..........loading")
    if coor == 0:
        Azimuth_sun = Azimuth_sun_and_ray
        Altitude_sun = Altitude_sun_and_normal
        sin_As = math.sin(math.radians(Azimuth_sun))
        cos_As = math.cos(math.radians(Azimuth_sun))

        sin_as = math.sin(math.radians(Altitude_sun))
        cos_as = math.cos(math.radians(Altitude_sun))        

        sin_AM= math.sin(math.radians(Azimuth_sur))
        cos_AM = math.cos(math.radians(Azimuth_sur))

        sin_aM = math.sin(math.radians(Altitude_sur))
        cos_aM = math.cos(math.radians(Altitude_sur))

        cos_n = cos_aM*cos_as*(cos_As*cos_AM + sin_As*sin_AM) + sin_aM*sin_as  ##the angle between the surface normal and the indent direction of the sunlight
        if cos_n <= 0:
            print("Irradience_on_surface..........finish")
            return 0
        P_sur = abs(I_sun * cos_n* Area)
        print("Irradience_on_surface..........finish")
        return P_sur
    elif coor == 1:
        ray = Azimuth_sun_and_ray
        normal = Altitude_sun_and_normal
        check = ray["x"]*normal["x"] + ray["y"]*normal["y"] + ray["z"]*normal["z"]
        if check >=0:
            print("Irradience_on_surface..........finish")
            return 0
        cos_n = -check/((math.sqrt(ray["x"]**2+ray["y"]**2+ray["z"]**2))*(math.sqrt(normal["x"]**2+normal["y"]**2+normal["z"]**2)))
        P_sur = abs(I_sun * cos_n* Area)
        print("Irradience_on_surface..........finish")
        return P_sur
    else:
        raise KeyError('coor wrong')
            


#if __name__ == "__main__":
    #print(check_out_or_in_polygon({"x":6,"y":2,"z":0},{"x":0,"y":0,"z":1},[{"x":2,"y":-1,"z":0},{"x":2,"y"  :2,"z":0},{"x":5,"y":5,"z":0},{"x":9,"y":6,"z":0},{"x":11,"y":3,"z":0},{"x":8,"y":-2,"z":0}]))
    #print(check_out_or_in_polygon({"x":6,"y":6,"z":0},{"x":0,"y":0,"z":1},[{"x":2,"y":-1,"z":0},{"x":2,"y"  :2,"z":0},{"x":5,"y":5,"z":0},{"x":9,"y":6,"z":0},{"x":11,"y":3,"z":0},{"x":8,"y":-2,"z":0}]))
    #print(line([{"x":2,"y":-1,"z":0},{"x":2,"y" :2,"z":0},{"x":5,"y":5,"z":0},{"x":9,"y":6,"z":0},{"x":11,"y":3,"z":0},{"x":8,"y":-2,"z":0}]))
    #print(line([{"x":2,"y":-1,"z":0},{"x":2,"y":2,"z":0},{"x":5,"y":5,"z":0},{"x":9,"y":6,"z":0},{"x":11,"y":3,"z":0},{"x":8,"y":-2,"z":0}]))
    #print(lineAB_lineCD({"x":2,"y" :2,"z":0},{"x":5,"y":5,"z":0},{"x":2,"y":4,"z":0},{"x":10,"y":5,"z":0}))
    #t = line_and_plane({"x":2,"y":-1,"z":1},{"x":2,"y":3,"z":5},{"x":2,"y":1,"z":1},{"x":0,"y":0,"z":8}) #point,u_1,normal_plane, point_plane
    #t = filter_point ([{"x":2,"y":-1,"z":0},{"x":2,"y"  :2,"z":0},{"x":5,"y":5,"z":0},{"x":9,"y":6,"z":0},{"x":11,"y":3,"z":0},{"x":8,"y":-2,"z":0}],[{"x":1,"y":1,"z":0},{"x":2,"y":4,"z":0},{"x":10,"y":4,"z":0},{"x":11,"y":2,"z":0},{"x":10,"y":-1,"z":0},{"x":6,"y":-3,"z":0}],{"x":0,"y":0,"z":1})
    #giữ t
    #print(t)
    #t = reorganize(t,{"x":0,"y":0,"z":1})
    #print("re:",t)
    #print (t)
    #a = polygon_area(t)
    #print(polygon_area(t))
    #print(point_receiver([{"x":2,"y":-1,"z":0},{"x":2,"y" :2,"z":0},{"x":5,"y":5,"z":0},{"x":9,"y":6,"z":0},{"x":11,"y":3,"z":0},{"x":8,"y":-2,"z":0}],[{"x":0,"y":0,"z":0},{"x":0,"y":0,"z":10},{"x":0,"y":10,"z":10},{"x":0,"y":10,"z":10}],{"x":1,"y":0,"z":0},{"x":-1,"y":0,"z":1}))
    #print(Irradience_on_surface(1000,10,171.36,11.6,130,20,0))
    #print(Irradience_on_surface(1000,12,{"x":2,"y" :-2,"z":-4},{"x":0,"y" :0,"z":1},0,0,1))