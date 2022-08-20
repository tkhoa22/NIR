# làm chuyển điểm (https://en.wikipedia.org/wiki/Rotation_of_axes)
import math
def cross_product(A,B):
    ###Перекрестный продукт A.B
    return {"x": A["y"]*B["z"] - A["z"]*B["y"], "y": A["z"]*B["x"] - A["x"]*B["z"], "z": A["x"]*B["y"] - A["y"]*B["x"]}
def rotation_of_axes(point,normal_plane,point_O,point_in_Ox["x"]):
    #преобразовать координаты точки Oxyz ->Oxy(cần test)
    if normal_plane["x"] == normal_plane["z"] == :
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
