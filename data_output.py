from mathsun import *
from mathgraphic import *
import math
import json

from datetime import datetime,date,timedelta

# x - N and y - E

class data_suntime():
    def __init__(self, start, end, lat, lon,index=5):
        self.data_sun = self.set_data(start, end, lat, lon,index)
    
    def set_data(self, start, end, lat, lon,index):
        data = []
        tz = gettzinfo(lat,lon)
        start_ts = datetime.timestamp(tz.localize(datetime(start["year"], start["month"], start["day"], start["hour"], start["minute"], start["second"])))
        end_ts = datetime.timestamp(tz.localize(datetime(end["year"], end["month"], end["day"], end["hour"], end["minute"], end["second"])))
        next_day = datetime.timestamp(tz.localize(datetime(start["year"], start["month"], start["day"],0,0,0))+ timedelta(days=1))
        count_day = 1
        data = []
        def set_data(first, final, index,count_day):
            data = []
            tde = datetime.fromtimestamp(first,tz= tz)#tde - time data element
            data_element = {"year":tde.year,"month":tde.month,"day":tde.day,"hour":tde.hour,"minute":tde.minute,"second":tde.second}
            data_element.update(Sun(lat,lon,first))
            data.append(data_element)
            first = (first//(index*60)+1)*(5*60)
            while first < final:
                tde = datetime.fromtimestamp(first,tz= tz)#tde - time data element
                data_element = {"year":tde.year,"month":tde.month,"day":tde.day,"hour":tde.hour,"minute":tde.minute,"second":tde.second}
                data_element.update(Sun(lat,lon,first))
                data.append(data_element)
                first += 60*index
            tde = datetime.fromtimestamp(final,tz= tz)#tde - time data element
            data_element = {"year":tde.year,"month":tde.month,"day":tde.day,"hour":tde.hour,"minute":tde.minute,"second":tde.second}
            data_element.update(Sun(lat,lon,final))
            data.append(data_element)
            first = final
            return data
        if end_ts <= next_day:
            data.append(set_data(start_ts,end_ts,index,count_day))
        else:
            time = start_ts
            while time < end_ts:
                if next_day <= end_ts:
                    data.append(set_data(time,next_day,index,count_day))
                    count_day += 1
                else:
                    #lấy 1 phần ngày
                    data.append(set_data(time,end_ts,index,count_day))
                    count_day += 1
                time = next_day
                next_day += 86400
        return data
    

class convert_input_to_output():
    def __init__(self, data_input):
        """
        self.PV_3D_and_reflected_light = [
        {"name":"dmcs",
        "coordinat_3D":
            {"A":{"x":1,"y":1,"z":1},"B":{"x":1,"y":1,"z":1},"C":{"x":1,"y":1,"z":1},"D":{"x":1,"y":1,"z":1}},
        "reflected_light":
            [{"time":12312312,"coordinat_2D_reflected_light":
                {"A":{"x":1,"y":1,"z":1},"B":{"x":1,"y":1,"z":1},"C":{"x":1,"y":1,"z":1},"D":{"x":1,"y":1,"z":1}},
            "S":123,"P":123},{},{},{}]
        }]
        self.All_power_on_t = [{"time":12312312,"P":123},{},{},{},{},{},{}]"""
        self.data_input = data_input
        self.check_fun_PV = 0
        self.check_fun_Mirror = 0

    @property
    def coordinat_3D_PV_and_add_normalvecto(self):
        for count_PV in self.data_input["PV"]:
            count_PV["B"] = {"x":count_PV["x"] + ((count_PV["w"]**2 + count_PV["zB_zA"]**2)**0.5)*math.cos(math.radians(count_PV["az"] - 90)),\
            "y":count_PV["y"] + ((count_PV["w"]**2 + count_PV["zB_zA"]**2)**0.5)*math.sin(math.radians(count_PV["az"] - 90)),"z":count_PV["zB_zA"]-count_PV["z"]}
            count_PV["normal"] = {"x":math.cos(math.radians(count_PV["al"]))*math.cos(math.radians(count_PV["az"])),\
            "y":math.cos(math.radians(count_PV["al"]))*math.sin(math.radians(count_PV["az"])),"z":math.sin(math.radians(count_PV["al"]))}
            count_PV.update(convert_AB_to_CD({"x":count_PV["x"],"y":count_PV["y"],"z":count_PV["z"]},count_PV["B"],count_PV["h"],count_PV["normal"]))
        self.check_fun_PV = 1
        return self.data_input["PV"]

    @property
    def coordinat_3D_Mirror_and_add_normalvecto(self):
        for count_Mirror in self.data_input["Mirror"]:
            count_Mirror["B"] = {"x":count_Mirror["x"] + ((count_Mirror["w"]**2 + count_Mirror["zB_zA"]**2)**0.5)*math.cos(math.radians(count_Mirror["az"]-90)),\
            "y":count_Mirror["y"] + ((count_Mirror["w"]**2 + count_Mirror["zB_zA"]**2)**0.5)*math.sin(math.radians(count_Mirror["az"]-90)),\
            "z":count_Mirror["zB_zA"] - count_Mirror["z"]}
            count_Mirror["normal"] = {"x":math.cos(math.radians(count_Mirror["al"]))*math.cos(math.radians(count_Mirror["az"])),\
            "y":math.cos(math.radians(count_Mirror["al"]))*math.sin(math.radians(count_Mirror["az"])),"z":math.sin(math.radians(count_Mirror["al"]))}
            count_Mirror.update(convert_AB_to_CD({"x":count_Mirror["x"],"y":count_Mirror["y"],"z":count_Mirror["z"]},count_Mirror["B"],count_Mirror["h"],count_Mirror["normal"]))
        self.check_fun_Mirror = 1
        return self.data_input["Mirror"]
    
    @property
    def PV_3D(self):
        data = data_suntime(self.data_input["time"]["start"],self.data_input["time"]["end"],self.data_input["location"]["lat"],self.data_input["location"]["lon"]).data_sun
        if self.check_fun_PV == 0:
            self.data_input["PV"] = self.coordinat_3D_PV_and_add_normalvecto
        if self.check_fun_Mirror == 0:
            self.data_input["Mirror"] = self.coordinat_3D_Mirror_and_add_normalvecto
        for day in data:
            for count_time in day:
                count_time.update({"Mirror":[]})
                count_time.update({"PV":[]})
                if count_time["al_s"] > 0:
                    normal_sun = {"x":math.cos(math.radians(count_time["al_s"]))*math.cos(math.radians(count_time["az_s"])),\
                        "y":math.cos(math.radians(count_time["al_s"]))*math.sin(math.radians(count_time["az_s"])),"z":math.sin(math.radians(count_time["al_s"]))}
                    for count_Mirror in self.data_input["Mirror"]:
                        reflected_ray_1 = reflected_ray(normal_sun,count_Mirror["normal"])      
                        if reflected_ray_1 != {"x": 0.0, "y": 0.0, "z": 0.0} and reflected_ray_1 != "None":
                            count_time["Mirror"].append(count_Mirror)
                            count_time["Mirror"][-1].update({"reflected_ray" : reflected_ray_1,"I_Mirror":Irradience_on_surface(1000,count_time["az_s"],\
                                count_time["al_s"],count_Mirror["az"],count_Mirror["al"]).I_sur})
                                 
                if len(count_time["Mirror"]) !=0:
                    for count_PV in self.data_input["PV"]:        
                        count_PV.update({"from_Mirror":[]})
                        for count_Mirror in count_time["Mirror"]:
                            point = point_receiver({"x":count_Mirror["x"],"y":count_Mirror["y"],"z":count_Mirror["z"]},count_Mirror["B"],count_Mirror["C"],count_Mirror["D"],\
                                {"x":count_PV["x"],"y":count_PV["y"],"z":count_PV["z"]},count_PV["B"],count_PV["C"],count_PV["D"],count_PV["normal"],count_Mirror["reflected_ray"])
                            print(point)
                            if type(point) == list:
                                count_data = {"S":polygon_area(point),"index_Mirror":count_Mirror["index"],"E":Energy_from_Mirror_in_PV(count_Mirror["normal"],\
                                    count_Mirror["B"],count_PV["normal"],count_PV["B"],count_Mirror["reflected_ray"],1000,point),"point":point}
                                count_time["PV"].append(count_PV)
                                count_time["PV"][-1] = count_data
        return data


if __name__ == "__main__":
    A = {"Mirror":[ { "type": "Mirror","zB_zA":0, "x": 0, "y": -10, "z": 0, "w": 10, "h": 10, "az": 90, "al": 0, "index": 5 }],"PV": [ { "type": "PV", "x": 0, "y": -10, "z":0, "w": 100, "h":100, "az":90, "al":90, "index": 1,"zB_zA":0 } ],"location": { "lat": 56.49771, "lon": 84.97437 }, "time": { "start": { "year": 2022, "month": 2, "day": 7, "hour": 9, "minute": 0, "second": 0 }, "end": { "year": 2022, "month": 2, "day": 7, "hour": 17, "minute": 0, "second": 0 } }}
    B = convert_input_to_output(A)
    with open("vd5.json", 'w') as f:
        json.dump(B.PV_3D ,f, ensure_ascii=False, indent=4)