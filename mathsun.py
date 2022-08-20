from datetime import datetime
from pytz import timezone
import math
import requests
import matplotlib.pyplot as plt

def is_Equal(dict1,n):
    for i in range(len(dict1)-1):
        if abs(dict1[0] - dict1[i]) >= 10**-n:
            return False    
    return True

def gettzinfo( lat, lon):
    url = "http://api.geonames.org/timezoneJSON?formatted=true&lat={}&lng={}&username=tkhoa22".format(lat,lon)
    r = requests.get(url) 
    timezone_1 = r.json()['timezoneId'] 
    
    return timezone(timezone_1)

def Sun(lat, lon,time_input):
    print("Sun.........loading")
    print("time = ",time_input)
    if type(time_input) is int or float:
        time = time_input
    elif type(time_input) is datetime:
        time = datetime.timestamp(gettzinfo(lat,lon).localize(time_input))
    D = (time - 946728000)/3600/24 ##the time elapsed since 1 January 2000 noon UTC
    q = (280.459 + 0.98564736 * D) - (((280.459 + 0.98564736 * D)/360//1)*360) ##the mean longitude
    g = (357.529 +  0.98560028 * D) - (((357.529 +  0.98560028 * D)/360//1)*360)  ## the mean anomaly
    l_s = q + 1.915*math.sin(math.radians(g)) + 0.020*math.sin(2*math.radians(g))  ##the latitude of the Sun 

    at = 23.429 - 0.00000036*D ##the axial tilt of the Earth

    GMST_h_demo = 18.697374558 + 24.06570982441908*D + 0.000026*(D/36525)*(D/36525) ##GMST/h before fillter

    GMST_h = GMST_h_demo - (GMST_h_demo/24//1)*24

    ph_l = GMST_h*15 + lon

    sin_ph_l = math.sin(math.radians(ph_l))
    cos_ph_l = math.cos(math.radians(ph_l))

    sin_l_s = math.sin(math.radians(l_s))
    cos_l_s = math.cos(math.radians(l_s))

    sin_at = math.sin(math.radians(at))
    cos_at = math.cos(math.radians(at))
    sin_lat = math.sin(math.radians(lat))
    cos_lat = math.cos(math.radians(lat))

    sin_lon = math.sin(math.radians(lon))
    cos_lon = math.cos(math.radians(lon))

    xi_sun = (- sin_lat*cos_ph_l*cos_l_s - (sin_lat*sin_ph_l*cos_at - cos_lat*sin_at)*sin_l_s)
    upsilon_sun = (- sin_ph_l*cos_l_s + cos_ph_l*cos_at*sin_l_s)
    zeta_sun = cos_lat*cos_ph_l*cos_l_s + (cos_lat*sin_ph_l*cos_at + sin_lat*sin_at)*sin_l_s

    tan_Azimuth_sun = upsilon_sun/xi_sun
    sin_Altitude_sun = zeta_sun

    if (xi_sun > 0):
        if (upsilon_sun > 0):
            Azimuth_sun = math.degrees(math.atan(tan_Azimuth_sun))
        else:
            Azimuth_sun = math.degrees(math.atan(tan_Azimuth_sun)) + 360
    else:
        Azimuth_sun = math.degrees(math.atan(tan_Azimuth_sun)) + 180

    Altitude_sun = math.degrees(math.asin(sin_Altitude_sun))
    print("Sun.........finish")
    return {"az_s":Azimuth_sun, "al_s": Altitude_sun,"lat_s":l_s }

def Irradience_on_surface(I_sun, Azimuth_sun, Altitude_sun, Azimuth_sur, Altitude_sur):

    sin_As = math.sin(math.radians(Azimuth_sun))
    cos_As = math.cos(math.radians(Azimuth_sun))

    sin_as = math.sin(math.radians(Altitude_sun))
    cos_as = math.cos(math.radians(Altitude_sun))        

    sin_AM= math.sin(math.radians(Azimuth_sur))
    cos_AM = math.cos(math.radians(Azimuth_sur))

    sin_aM = math.sin(math.radians(Altitude_sur))
    cos_aM = math.cos(math.radians(Altitude_sur))

    cos_n = cos_aM*cos_as*(cos_As*cos_AM + sin_As*sin_AM) + sin_aM*sin_as  ##the angle between the surface normal and the indent direction of the sunlight
    I_sur = abs(I_sun * cos_n)
    return I_sur

def Irradience_on_roof(I_sun,Azimuth_sun, Altitude_sun, Azimuth_roof, Altitude_roof, Azimuth_sur_roof, Altitude_sur_roof):
    sin_As = math.sin(math.radians(Azimuth_sun))
    cos_As = math.cos(math.radians(Azimuth_sun))
    sin_as = math.sin(math.radians(Altitude_sun))
    cos_as = math.cos(math.radians(Altitude_sun))        

    sin_AR = math.sin(math.radians(Azimuth_roof))
    cos_AR = math.cos(math.radians(Azimuth_roof))
    sin_aR = math.sin(math.radians(Altitude_roof))
    cos_aR = math.cos(math.radians(Altitude_roof))

    sin_phM = math.sin(math.radians(Azimuth_sur_roof))
    cos_phM = math.cos(math.radians(Azimuth_sur_roof))
    sin_bM = math.sin(math.radians(Altitude_sur_roof))
    cos_bM = math.cos(math.radians(Altitude_sur_roof))

    xi = -cos_AR*sin_aR*cos_bM*cos_phM + sin_AR*cos_bM*sin_phM + cos_AR*cos_aR*sin_bM
    upsilon = -sin_AR*sin_aR*cos_bM*cos_phM - cos_AR*cos_bM*sin_phM + sin_AR*cos_aR*sin_bM
    zeta = cos_aR*cos_bM*cos_phM + sin_aR*sin_bM

    tan_Azimuth_roof = upsilon/xi
    sin_Altitude_roof = zeta

    if (xi > 0):
        if (upsilon > 0):
            Azimuth_roof = math.degrees(math.atan(tan_Azimuth_roof))
        else:
            Azimuth_roof = math.degrees(math.atan(tan_Azimuth_roof)) + 360
    else:
        Azimuth_roof = math.degrees(math.atan(tan_Azimuth_roof)) + 180

    Altitude_roof = math.degrees(math.asin(sin_Altitude_roof))
        
    cos_n_1 = cos_as*(cos_As*cos_AR + sin_As*sin_AR)*(cos_aR*sin_bM - sin_aR*cos_bM*cos_phM) 
    cos_n_2 = cos_as*(sin_AR*cos_As - sin_As*cos_AR)*cos_bM*sin_phM
    cos_n_3 = sin_as*(cos_aR*cos_bM*cos_phM + sin_aR*sin_bM)

    cos_n = cos_n_1 + cos_n_2 + cos_n_3

    return {"az":Azimuth_roof, "al": Altitude_roof, "cos_n" : cos_n, "I_sur":I_sun*cos_n}


def division_angle(k,b):
    tg_B = math.tan(math.radians(b))
    if 0 < b < 90:
        tg1 = (- (k + 1) + math.sqrt((k + 1)*(k + 1)+ 4*k*tg_B*tg_B))/(2*k*tg_B)
    elif is_Equal([b,90],5) is True:
        tg1 = 1/math.sqrt(k)
    else:
        tg1 = (- (k + 1) - math.sqrt((k + 1)*(k + 1)+ 4*k*tg_B*tg_B))/(2*k*tg_B)
    a1=math.degrees(math.atan(tg1))
    return [a1,b-a1]



if __name__ == "__main__":
    print(gettzinfo(56.49771, 84.97437))
    print("***********")
    nad = datetime.timestamp(datetime(2021, 11, 29, 12, 31, 59))
    print(nad)
    b = Sun(56.49771, 84.97437,nad )
    print(b)
    print("VVVVVVVVVVVVV")
    print(b["az_s"])
    print(b["al_s"])

    a = Irradience_on_surface(1000, b["az_s"], b["al_s"], 171, 11)
    print(a)
    x = []
    y = []
    z = []
    n = 10
    while (n < 170):
        i = 0.3 
        e = division_angle(i,n)
        c = Irradience_on_roof(1000, b["az_s"], b["al_s"], 171, 11, 90, e[0])
        d = Irradience_on_roof(1000, b["az_s"], b["al_s"], 171, 11, -90, e[1])
        r1 = (i+1)*math.sin(math.radians(e[0]))
        r2 = (i+1)*math.sin(math.radians(e[1]))/i
        if r1 ==0: 
            r1=0.0000000000001
        print("          ")
        print ("d : ", d["I_sur"], "c : ", c["I_sur"])
        print("x : ",n,"Iradiance: ", (d["I_sur"]/r2 + c["I_sur"]/r1), " sun:",a)
        print("delta: ", (d["I_sur"]/r2 + c["I_sur"]/r1)/a)
        print("S1/S2: ", 1/r1 + 1/r2)
        print("e: ",e)
        x.append(n)
        y.append(((d["I_sur"] + c["I_sur"])))
        z.append(11)
        n+=1



