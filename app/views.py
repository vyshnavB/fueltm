from io import BytesIO
import random
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render,redirect
from datetime import datetime, timedelta

import hashlib

from FuelTM import settings
# Create your views here.

from . models import *

from datetime import datetime

import json
import requests

from django.contrib import messages

from django.utils import timezone
import calendar


today = timezone.now()

import datetime

from datetime import date
from dateutil.relativedelta import relativedelta

from django.template.loader import get_template
from xhtml2pdf import pisa
from . models import*

from io import BytesIO
import os
from django.template.loader import render_to_string

from django.contrib.auth.models import User,auth

import math

# from django.contrib.auth.views import logout

from django.core.mail import send_mail


def Home(request):
    current_time = datetime.datetime.now().time() 

    
    if 'User_Id' in request.session:
        request.session['Custom']=""
        request.session['fill_fuel_mode']=""
        request.session['Fuel_Date']= ""
        
        user=request.session['User_Id']

        type = request.session["Type"]

       

        Power_Access = 0
        Purchase_Access = 0
        Service_Access = 0
        Fill_Access = 0
        Generator_Access = 0
        Report_Access = 0
        Device_Access = 0

        data1={
                'user_id':user
            } 

        


        if request.method == 'POST':
            request.session["Gen_Id"]=""



            generator = request.POST['genId']

            request.session["Gen_Id"] = generator



            piechart = requests.post('https://www.fishguard.in/Fuel/index.php/Fuel_Controller/fetchCurrentHeight',data=data1).json()

           

            loadCurrent=piechart['loadCurrent']

            # print(loadCurrent)


            
            currentvolume=0
            volume=0.0
            for i in loadCurrent:

                if generator == i['genId']:
                    
                    volume=float(i['volume'])
                    number =volume/1000
                    vol =round(number,1)
                    print(vol)
                    currentvolume=float(i['volume'])/1000




            fetchGen=requests.post('https://www.fishguard.in/Fuel/index.php/Fuel_Controller/fetchGen',data=data1).json()
            
            beanGenerator= fetchGen['beanGenerator']
            
             


            Gen=""
            if type == '2':

                genType=fetchGen['genType']
                print(genType)

                facility=fetchGen['facility']
                print(facility)

                Gen =genType.split('_')
                access=facility.split('_')

                print(Gen)
                print(access)
                Power_Access =access[0]
                Purchase_Access =access[1]
                Service_Access =access[2]
                Fill_Access =access[3]
                Generator_Access =access[4]
                Report_Access =access[5]
                Device_Access =access[6]

            request.session['Generator_Access'] =Generator_Access 

            request.session['Purchase_Access'] = Purchase_Access

            request.session['Service_Access'] = Service_Access
    
            # print(beanGenerator)
             
            consumption=0
            totalFuel=0
            
            for i in  beanGenerator:
                if generator == i['genId']:
                    
                    totalFuel=float(i['totalFuel'])

                    deviceId=i['deviceId']
                    print(deviceId)
                   
                    consumption0=float(i['valueZero'])
                    consumption25=float(i['value25'])
                    consumption50=float(i['value50'])
                    consumption75=float(i['value75'])
                    consumption100=float(i['value100'])

            # print(deviceId) 

            request.session['Device_Id'] =  deviceId

            # print(request.session['Device_Id'])        

            data={
                'deviceId':deviceId,
            }
            device = requests.post('https://www.fishguard.in/Fuel/index.php/Fuel_Controller/fetchDeviceData',data=data).json()
            
            
            responseCode=device['responseCode']

            print(responseCode)      
            
           

            if consumption0 == 0 :
                Approx_hour0 = 0.0
            else:
                Approx_hour0 = currentvolume/consumption0
                    
                
            if consumption25 == 0 :
                Approx_hour25 = 0.0
            else:
                Approx_hour25 = currentvolume/consumption25


            if  consumption50 == 0 :
                Approx_hour50 = 0.0
            else:
                Approx_hour50 = currentvolume/consumption50


            if consumption75 == 0 :
                Approx_hour75 = 0.0
            else:
                Approx_hour75 = currentvolume/consumption75


            if consumption100 == 0 :
                Approx_hour100 = 0.0
            else:
                Approx_hour100 = currentvolume/consumption100


                


            

            

            # print("consumption")

            # print(consumption)


            three_months_ago = date.today() + relativedelta(months=-3)

        
            last_day_of_month = datetime.datetime.now().date()

            

            data4={
                'genId':generator,
                'timeAgo':three_months_ago,
                'timeAfter':last_day_of_month,
            }


            fetchFillManual = requests.post('https://www.fishguard.in/Fuel/index.php/Fuel_Controller/fetchFillManual',data=data4).json()

            responseCode=fetchFillManual['responseCode']



            fillManualArray=""
            fill_time=""
            if responseCode == 1:

                fillManualArray = fetchFillManual['fillManualArray']

                for i in fillManualArray:
                    if i == fillManualArray[0]:

                        # print(i)

                       
                    
                        fill_time=int(i['timestamp'])

                        print(fill_time)


                print("fillManualArray")
                print(fillManualArray)


            # data5={
            #     'userId':user,
            # }
            # totalConsumption=requests.post('https://www.fishguard.in/Fuel/index.php/Fuel_Controller/totalConsumption',data=data5).json()

            # print(totalConsumption)
            # loadSumConsumption=""

            # responseCode=totalConsumption['responseCode']
            # if responseCode == 1:
            #     loadSumConsumption = totalConsumption['loadSumConsumption']

                # print(loadSumConsumption)

            

            data6={
                'userId':user,
            }
            loadAlert=""
            fetch_alert = requests.post('https://www.fishguard.in/Fuel/index.php/Fuel_Controller/fetchAlert',data=data6).json()

            responseCode = fetch_alert['responseCode']

            count=0
            if responseCode == 1:
                loadAlert = fetch_alert['loadAlert']
                for i in loadAlert:
                    count = count+1
            


            gener_type =""

            gen_radious=""
            gen_length=""
            gen_width=""
            

            for i in beanGenerator:
                if i['genId'] == generator:
                    Generator_Type = [i]
                    print(Generator_Type )

                    
                    if i['shape'] == "Rectangle":
                        gener_type="Rectangle"

                        Gen_volume = (float(i['length'])* float(i['width']) * float(i['height']))/1000

                        gen_length=i['length']
                        gen_width=i['width']
                        

                        print(Gen_volume) 

                    if i['shape'] == "VCylinder":
                        gener_type="VCylinder"

                        Gen_volume = (3.14 * float(i['radious'])* float(i['radious']) * float(i['height']))/1000
                        gen_radious = i['radious']

                        print(Gen_volume)

                    if i['shape'] == "HCylinder":
                        gener_type="HCylinder"

                        r=float(i['radious'])
                        
                        l=float(i['length'])

                        gen_radious = i['radious']
                        gen_length = i['length']

                        Gen_volume = 3.14 *r*r*l

                        print(Gen_volume)  
            parameters ={
                'userId':user,
            }


            fetchConsumptionMonth = requests.post('https://www.fishguard.in/Fuel/index.php/Fuel_Controller/fetchConsumptionMonth',data=parameters).json()

            # print(fetchConsumptionMonth)

            responseCode = fetchConsumptionMonth['responseCode']
            fuel_ConsumptionMonth =""
            monthlist=[]
            timeDiffrence=[]
            heightDiffrence=[]
            if responseCode == 1:
                loadConsumptionMonth = fetchConsumptionMonth['loadConsumptionMonth']
                # print(loadConsumptionMonth)

                
                fuel_ConsumptionMonth = list(filter(lambda data: data.get('genId') == generator, loadConsumptionMonth))

                # print(fuel_ConsumptionMonth)

                    
                for i in fuel_ConsumptionMonth:
                    mo=datetime.datetime.fromtimestamp(int(i['monthYear'])).month
                    month_abbr = calendar.month_abbr[mo]
                    monthlist.append(month_abbr)
                    # print(month_abbr)
                    timeDiffrence.append(round(float(i['timeDiffrence']), 1))

                    if gener_type == "Rectangle":
                        Gen_volume = (float(gen_length)* float(gen_width) * float(i['heightDiffrence']))/1000

                        heightDiffrence.append(round(Gen_volume, 1))

                    if gener_type == "VCylinder":
                        Gen_volume = (3.14 * float(gen_radious)* float(gen_radious) * float(i['heightDiffrence']))/1000

                        dayheightDiffrence.append(round(Gen_volume, 1))    

                    if gener_type == "HCylinder":
                       

                        r=float(gen_radious)
                        h=float(i['heightDiffrence'])
                        l=float(gen_length)

                        if h <= r:
                            area = math.acos((r - h) / r) * r**2 - (r - h) * math.sqrt(2*r*h - h**2)
                        else:
                            area = 0
                        # area = math.acos((r - h) / r) * (r ** 2 - (r - h) * math.sqrt(2 * r * h - h ** 2))

                        Gen_volume = area*l

                        heightDiffrence.append(round(Gen_volume, 1))

                # print(monthlist)
                # print(timeDiffrence)

                print(heightDiffrence)

                
            # print(beanGenerator)


            parameters2 ={
                'userId':user,
            }


            fetchConsumptionday = requests.post('https://www.fishguard.in/Fuel/index.php/Fuel_Controller/fetchConsumptionday',data=parameters2).json()

            responseCode = fetchConsumptionday['responseCode']

            print(fetchConsumptionday)
            fuel_Consumptionday =""
            daylist=[]
            daytimeDiffrence=[]
            dayheightDiffrence=[]
            if responseCode == 1:
                loadConsumptionDay = fetchConsumptionday['loadConsumptionDay']
                # print(loadConsumptionDay)

                fuel_Consumptionday = list(filter(lambda data: data.get('genId') == generator, loadConsumptionDay))

                # print(fuel_Consumptionday)

                    
                for i in fuel_Consumptionday:
                    da=datetime.datetime.fromtimestamp(int(i['day']))
                    formatted_date = da.strftime('%d %b')
                
                    daylist.append(formatted_date)

                    
                
                    daytimeDiffrence.append(round(float(i['timeDiffrence']), 1))

                    if gener_type == "Rectangle":
                        Gen_volume = (float(gen_length)* float(gen_width) * float(i['heightDiffrence']))/1000

                        dayheightDiffrence.append(round(Gen_volume, 1))
                        
                    if gener_type == "VCylinder":
                        Gen_volume = (3.14 * float(gen_radious)* float(gen_radious) * float(i['heightDiffrence']))/1000

                        dayheightDiffrence.append(round(Gen_volume, 1))
                # print(monthlist)
                # print(daytimeDiffrence)
                # print(daylist)





            pra2 ={
                'genid':generator,
            }

            fetch_slider = requests.post('https://www.fishguard.in/Fuel/index.php/Fuel_Controller/fetchAllConsumption',data=pra2).json()

            print(fetch_slider)

            fetch_slider_responseCode = fetch_slider['responseCode']
            loadslider = ""
            if fetch_slider_responseCode == 1 :
                loadslider = fetch_slider['loadslider']


            



            context = {
    
                'current_time':current_time,
               
                'beanGenerator':beanGenerator,
                
                'status':'Yes',
                'volume':vol,
                'totalFuel':totalFuel,
                'generator':generator,
                'deviceId':deviceId,
                
                'fillManualArray':fillManualArray,
                
                'type':type,
                'Gen':Gen,
                'Power_Access':Power_Access,
                'Purchase_Access':Purchase_Access,
                'Service_Access':Service_Access,
                'Fill_Access':Fill_Access,
                'Generator_Access':Generator_Access,
                'Report_Access':Report_Access,
                'Device_Access':Device_Access,
                'fill_time':fill_time,
                # 'loadSumConsumption':loadSumConsumption,
                'loadAlert':loadAlert,
                'monthlist':monthlist,
                'timeDiffrence':timeDiffrence,
                'daylist':daylist,
                'daytimeDiffrence':daytimeDiffrence,
                'heightDiffrence':heightDiffrence,
                'dayheightDiffrence':dayheightDiffrence,
                'user':user,
                'count':count,
                'Approx_hour0':Approx_hour0,
                'Approx_hour25':Approx_hour25,
                'Approx_hour50':Approx_hour50,
                'Approx_hour75':Approx_hour75,
                'Approx_hour100':Approx_hour100,
                'fetch_slider_responseCode':fetch_slider_responseCode,
                'loadslider':loadslider,
               
                



                }
            
            return render(request,'index.html',context)

        elif 'Gen_Id' in request.session:

            generator = request.session['Gen_Id']

           

            piechart = requests.post('https://www.fishguard.in/Fuel/index.php/Fuel_Controller/fetchCurrentHeight',data=data1).json()
            loadCurrent=piechart['loadCurrent']
            
            currentvolume=0
            volume=0.0
            for i in loadCurrent:

                if generator == i['genId']:
                    
                    volume=float(i['volume'])
                    number =volume/1000
                    vol =round(number,1)
                    print(vol)
                    currentvolume=float(i['volume'])/1000

            fetchGen=requests.post('https://www.fishguard.in/Fuel/index.php/Fuel_Controller/fetchGen',data=data1).json()
            
            beanGenerator= fetchGen['beanGenerator'] 
            print(beanGenerator)
            Gen=""
            if type == '2':

                genType=fetchGen['genType']
                print(genType)

                facility=fetchGen['facility']
                print(facility)

                Gen =genType.split('_')
                access=facility.split('_')

                print(Gen)
                print(access)
                Power_Access =access[0]
                Purchase_Access =access[1]
                Service_Access =access[2]
                Fill_Access =access[3]
                Generator_Access =access[4]
                Report_Access =access[5]
                Device_Access =access[6]

                
            request.session['Generator_Access'] =Generator_Access 

            request.session['Purchase_Access'] = Purchase_Access

            request.session['Service_Access'] = Service_Access 


            consumption=0
            totalFuel=0
            for i in  beanGenerator:
                if generator == i['genId']:
                    
                    totalFuel=float(i['totalFuel'])

                    deviceId=i['deviceId']
                    print(deviceId)
                   
                    consumption0=float(i['valueZero'])
                    consumption25=float(i['value25'])
                    consumption50=float(i['value50'])
                    consumption75=float(i['value75'])
                    consumption100=float(i['value100'])
                   

            request.session['Device_Id'] =  deviceId 
                    
            data={
                'deviceId':deviceId,
            }
            device = requests.post('https://www.fishguard.in/Fuel/index.php/Fuel_Controller/fetchDeviceData',data=data).json()
            

            responseCode=device['responseCode']

            print(responseCode)
            if consumption0 == 0 :
                Approx_hour0 = 0.0
            else:
                Approx_hour0 = currentvolume/consumption0
                    
                
            if consumption25 == 0 :
                Approx_hour25 = 0.0
            else:
                Approx_hour25 = currentvolume/consumption25


            if  consumption50 == 0 :
                Approx_hour50 = 0.0
            else:
                Approx_hour50 = currentvolume/consumption50


            if consumption75 == 0 :
                Approx_hour75 = 0.0
            else:
                Approx_hour75 = currentvolume/consumption75


            if consumption100 == 0 :
                Approx_hour100 = 0.0
            else:
                Approx_hour100 = currentvolume/consumption100





            three_months_ago = date.today() + relativedelta(months=-3)

        
            last_day_of_month = datetime.datetime.now().date()

            

            data4={
                'genId':generator,
                'timeAgo':three_months_ago,
                'timeAfter':last_day_of_month,
            }


            fetchFillManual = requests.post('https://www.fishguard.in/Fuel/index.php/Fuel_Controller/fetchFillManual',data=data4).json()

            responseCode=fetchFillManual['responseCode']

            fillManualArray=""
            fill_time=""
            if responseCode == 1:

                fillManualArray = fetchFillManual['fillManualArray']

                for i in fillManualArray:
                    if i == fillManualArray[0]:
                    
                        fill_time=int(i['timestamp'])

                # print(fillManualArray)

            # data5={
            #     'userId':user,
            # }
            # totalConsumption=requests.post('https://www.fishguard.in/Fuel/index.php/Fuel_Controller/totalConsumption',data=data5).json()

            # print(totalConsumption)
            # loadSumConsumption=""
            # responseCode = totalConsumption['responseCode']

            # if responseCode == 1:
            #     loadSumConsumption = totalConsumption['loadSumConsumption']


            data6={
                'userId':user,
            }
            loadAlert=""
            fetch_alert = requests.post('https://www.fishguard.in/Fuel/index.php/Fuel_Controller/fetchAlert',data=data6).json()

            responseCode = fetch_alert['responseCode']
            count=0
            if responseCode == 1:
                loadAlert = fetch_alert['loadAlert']
                for i in loadAlert:
                    count = count+1
                    

            
            # print(loadAlert)


            gener_type =""

            gen_radious=""
            gen_length=""
            gen_width=""
            

            for i in beanGenerator:
                if i['genId'] == generator:
                    Generator_Type = [i]
                    # print(Generator_Type )

                    
                    if i['shape'] == "Rectangle":
                        gener_type="Rectangle"

                        Gen_volume = (float(i['length'])* float(i['width']) * float(i['height']))/1000

                        gen_length=i['length']
                        gen_width=i['width']
                        

                        # print(Gen_volume) 

                    if i['shape'] == "VCylinder":
                        gener_type="VCylinder"

                        Gen_volume = (3.14 * float(i['radious'])* float(i['radious']) * float(i['height']))/1000
                        gen_radious = i['radious']

                        print(Gen_volume)

                    if i['shape'] == "HCylinder":
                        gener_type="HCylinder"

                        r=float(i['radious'])
                        
                        l=float(i['length'])

                        gen_radious = i['radious']
                        gen_length = i['length']

                        Gen_volume = 3.14 *r*r*l

                        # print(Gen_volume)  
            parameters ={
                'userId':user,
            }


            fetchConsumptionMonth = requests.post('https://www.fishguard.in/Fuel/index.php/Fuel_Controller/fetchConsumptionMonth',data=parameters).json()

            # print(fetchConsumptionMonth)

            responseCode = fetchConsumptionMonth['responseCode']
            fuel_ConsumptionMonth =""
            monthlist=[]
            timeDiffrence=[]
            heightDiffrence=[]
            if responseCode == 1:
                loadConsumptionMonth = fetchConsumptionMonth['loadConsumptionMonth']
                # print(loadConsumptionMonth)

                
                fuel_ConsumptionMonth = list(filter(lambda data: data.get('genId') == generator, loadConsumptionMonth))

                # print(fuel_ConsumptionMonth)

                    
                for i in fuel_ConsumptionMonth:
                    mo=datetime.datetime.fromtimestamp(int(i['monthYear'])).month
                    month_abbr = calendar.month_abbr[mo]
                    monthlist.append(month_abbr)
                    # print(month_abbr)
                    timeDiffrence.append(round(float(i['timeDiffrence']), 1))

                    if gener_type == "Rectangle":
                        Gen_volume = (float(gen_length)* float(gen_width) * float(i['heightDiffrence']))/1000

                        heightDiffrence.append(round(Gen_volume, 1))

                    if gener_type == "VCylinder":
                        Gen_volume = (3.14 * float(gen_radious)* float(gen_radious) * float(i['heightDiffrence']))/1000

                        dayheightDiffrence.append(round(Gen_volume, 1))    

                    if gener_type == "HCylinder":
                       

                        r=float(gen_radious)
                        h=float(i['heightDiffrence'])
                        l=float(gen_length)

                        if h <= r:
                            area = math.acos((r - h) / r) * r**2 - (r - h) * math.sqrt(2*r*h - h**2)
                        else:
                            area = 0
                        # area = math.acos((r - h) / r) * (r ** 2 - (r - h) * math.sqrt(2 * r * h - h ** 2))

                        Gen_volume = area*l

                        heightDiffrence.append(round(Gen_volume, 1))

                # print(monthlist)
                # print(timeDiffrence)

                # print(heightDiffrence)

                
            # print(beanGenerator)


            parameters2 ={
                'userId':user,
            }


            fetchConsumptionday = requests.post('https://www.fishguard.in/Fuel/index.php/Fuel_Controller/fetchConsumptionday',data=parameters2).json()

            responseCode = fetchConsumptionday['responseCode']

            # print(fetchConsumptionday)
            fuel_Consumptionday =""
            daylist=[]
            daytimeDiffrence=[]
            dayheightDiffrence=[]
            if responseCode == 1:
                loadConsumptionDay = fetchConsumptionday['loadConsumptionDay']
                # print(loadConsumptionDay)

                fuel_Consumptionday = list(filter(lambda data: data.get('genId') == generator, loadConsumptionDay))

                # print(fuel_Consumptionday)

                    
                for i in fuel_Consumptionday:
                    da=datetime.datetime.fromtimestamp(int(i['day']))
                    formatted_date = da.strftime('%d %b')
                
                    daylist.append(formatted_date)

                    
                
                    daytimeDiffrence.append(round(float(i['timeDiffrence']), 1))

                    if gener_type == "Rectangle":
                        Gen_volume = (float(gen_length)* float(gen_width) * float(i['heightDiffrence']))/1000

                        dayheightDiffrence.append(round(Gen_volume, 1))
                        
                    if gener_type == "VCylinder":
                        Gen_volume = (3.14 * float(gen_radious)* float(gen_radious) * float(i['heightDiffrence']))/1000

                        dayheightDiffrence.append(round(Gen_volume, 1))
                # print(monthlist)
                # print(daytimeDiffrence)
                # print(daylist)







            pra2 ={
                'genid':generator,
            }

            fetch_slider = requests.post('https://www.fishguard.in/Fuel/index.php/Fuel_Controller/fetchAllConsumption',data=pra2).json()

            print(fetch_slider)

            fetch_slider_responseCode = fetch_slider['responseCode']
            loadslider = ""
            if fetch_slider_responseCode == 1 :
                loadslider = fetch_slider['loadslider']


            context = {
    
                'current_time':current_time,
               
                'beanGenerator':beanGenerator,
                
                'status':'Yes',
                'volume':vol,
                'totalFuel':totalFuel,
                'generator':generator,
                'deviceId':deviceId,
                
                'fillManualArray':fillManualArray,
                
                'type':type,
                'Gen':Gen,
                'Power_Access':Power_Access,
                'Purchase_Access':Purchase_Access,
                'Service_Access':Service_Access,
                'Fill_Access':Fill_Access,
                'Generator_Access':Generator_Access,
                'Report_Access':Report_Access,
                'Device_Access':Device_Access,
                'fill_time':fill_time,
                # 'loadSumConsumption':loadSumConsumption,
                'loadAlert':loadAlert,
                'monthlist':monthlist,
                'timeDiffrence':timeDiffrence,
                'daylist':daylist,
                'daytimeDiffrence':daytimeDiffrence,
                'heightDiffrence':heightDiffrence,
                'dayheightDiffrence':dayheightDiffrence,
                'user':user,
                'count':count,
                'Approx_hour0':Approx_hour0,
                'Approx_hour25':Approx_hour25,
                'Approx_hour50':Approx_hour50,
                'Approx_hour75':Approx_hour75,
                'Approx_hour100':Approx_hour100,
                'fetch_slider_responseCode':fetch_slider_responseCode,
                'loadslider':loadslider,
               
               
                



                }
            
            return render(request,'index.html',context)
            
        else: 
            deviceId=0
            fetchGen=requests.post('https://www.fishguard.in/Fuel/index.php/Fuel_Controller/fetchGen',data=data1).json()

            print(fetchGen)


            Gen=""
            if type == '2':

                genType=fetchGen['genType']
                print(genType)

                facility=fetchGen['facility']
                print(facility)

                Gen =genType.split('_')
                access=facility.split('_')

                print(Gen)
                print(access)
                Power_Access =access[0]
                Purchase_Access =access[1]
                Service_Access =access[2]
                Fill_Access =access[3]
                Generator_Access =access[4]
                Report_Access =access[5]
                Device_Access =access[6]








            type = request.session["Type"]
            phone = request.session["Phone"]
            print(phone)
            Gen=""
            if phone == '0':
                return redirect('Verifications')

            
            else:
                if fetchGen['responseCode']==0:
                    return redirect('Add_Application')
                else:    
                
                    beanGenerator= fetchGen['beanGenerator']

                    if type == '2':

                        genType=fetchGen['genType']
                        print(genType)

                        facility=fetchGen['facility']
                        print(facility)

                        Gen =genType.split('_')
                        access=facility.split('_')

                        print(Gen)
                        print(access)

                        
                    
                    
                    context = {
                        'current_time':current_time,
                        # 'loadDeviceDetails':loadDeviceDetails,
                        'beanGenerator':beanGenerator,
                        'volume':0.0,
                        'generator':0,
                        'totalFuel':0.0,
                        'Approx_hour':0.0,
                        # 'generator_name':generator_name,
                        'deviceId':deviceId,
                        'type':type,
                        'Gen':Gen,
                        'user':user,
                        'count':0,
                        'Power_Access':Power_Access,
                        'Purchase_Access':Purchase_Access,
                        'Service_Access':Service_Access,
                        'Fill_Access':Fill_Access,
                        'Generator_Access':Generator_Access,
                        'Report_Access':Report_Access,
                        'Device_Access':Device_Access,
                    }
                    return render(request,'index.html',context)
            
    return redirect('Login')    

def Add_Application(request):
    if 'User_Id' in request.session:
        request.session['Custom']=""
        request.session['fill_fuel_mode']=""
        request.session['Fuel_Date']=""

        user=request.session['User_Id']
        
        type = request.session["Type"]
        
        if 'Gen_Id' in request.session:
            generator = request.session["Gen_Id"]
        else:
            generator = 0
            



         


        Purchase_Access=""
        Service_Access=""
        if type == "2":
            Purchase_Access = request.session['Purchase_Access']  

            Service_Access = request.session['Service_Access'] 

        if request.method=='POST':
            user=request.session['User_Id']
           
            name=request.POST['name']

            shape=request.POST['shape']
            totalFuel= request.POST['totalFuel']

            consumption=0

            rectanklength=request.POST['rectanklength']
            rectankwidth=request.POST['rectankwidth']
            rectankheight=request.POST['rectankheight']
            rectankslope=request.POST['rectankslope']
            vctankheight=request.POST['vctankheight']
            htanklenght=request.POST['htanklenght']
            vc_h_tankslope=request.POST['vc_h_tankslope']
            vc_h_tankradious=request.POST['vc_h_tankradious']


            enginmake=request.POST['engine_make']

            ratinginkw = request.POST['rating_kw']

            application_type =request.POST['application']

            ratingInHp=0

            if application_type == 'Fire Engine':

                ratingInHp=request.POST['hp']


            


            phase=request.POST['phase']


            valueZero = 0
            value25 = 0
            value50 = 0
            value75 = 0
            value100 = 0
            engineMakename=""
            if enginmake == "Others":
                valueZero = request.POST['valueZero']
                value25 = request.POST['value25']
                value50 = request.POST['value50']
                value75 = request.POST['value75']
                value100 = request.POST['value100']

                engineMakename = request.POST['other_enginmake']

            ratingInKWname=""
            
            if ratinginkw == "Others":

                ratingInKWname = request.POST['other_Kw']


            length=0
            width=0
            height=0
            radious=0
            slope=0
            volume=0
            if 'Rectangle' == shape:
                length=rectanklength
                width=rectankwidth
                height=rectankheight
                slope=rectankslope

                
                volume=float(length)*float(width)*float(height)/1000
                


            if 'Vertical' == shape:
                height=vctankheight
                slope=vc_h_tankslope
                radious=vc_h_tankradious

                volume=3.14*float(radious)*float(radious)*float(height)/1000


            if 'Horizontal' == shape:
                length=htanklenght
                slope=vc_h_tankslope
                radious=vc_h_tankradious

                volume=3.14*float(radious)*float(radious)*float(length)/1000
    
            print(totalFuel)
            print(volume)
            if ((volume >=float(totalFuel) ) and (volume <= float(totalFuel) + 1)):
                
                
                data1={
                    'userId':user,
                    'name':name,
                    'shape':shape,
                    'totalFuel':totalFuel,
                    'length':length,
                    'width':width,
                    'height':height,
                    'radious':radious,
                    'slope':slope,
                    'consumption':consumption,
                    'engineMake':enginmake,
                    'ratingInKW':ratinginkw,
                    'ratingInHp':ratingInHp,
                    'phase':phase,
                    'application':application_type,
                    'valueZero':valueZero,
                    'value25':value25,
                    'value50':value50,
                    'value75':value75,
                    'value100':value100,
                    'engineMakename':engineMakename,
                    'ratingInKWname':ratingInKWname,




                }

                Add_Gen=requests.post('https://www.fishguard.in/Fuel/index.php/Fuel_Controller/addGen',data=data1).json()
                
                print(Add_Gen)

                response=Add_Gen['responseCode']

                if response==1:
                    Generator = Add_Gen['genId']
                    request.session["Gen_Id"] = Generator
                    print(Generator)
                else:
                    messages.info(request, 'Generator name already exists')
                    return redirect('Add_Application')

                return redirect('Add_Device')

            else:
                    
                messages.info(request, 'Check Tank Dimensions')

                return redirect('Add_Application')



        
        fetchEnginMake = requests.post('https://www.fishguard.in/Fuel/index.php/Fuel_Controller/listEngineMake').json()

        # print(fetchEnginMake)

        listEngineMake = fetchEnginMake['listEngineMake']

        # for item in my_list :
        #      if forloop.first :
        #    item 
      
        print(listEngineMake)

        first_engine_make='Cummins'
        for engine in listEngineMake:
            first_engine_make = engine['engineMake']
            print(first_engine_make)
            break

        pra={
            'enginMake':first_engine_make,
        }

        fetchKw = requests.post('https://www.fishguard.in/Fuel/index.php/Fuel_Controller/listKW',data=pra).json()

        listKw=fetchKw['listKw']
        # print(fetchKw)



        context={
            'user':user,
            'listEngineMake':listEngineMake,
            'listKw':listKw,
            'Purchase_Access':Purchase_Access,
            'Service_Access':Service_Access,
            'type':type,
            'generator':generator,
            
        }


        return render(request,'add_generator.html',context)
        
    return redirect('Login')
    

def Users(request):
    if 'User_Id' in request.session:
        request.session['Custom']=""
        request.session['fill_fuel_mode']=""


        user = request.session['User_Id']

        data1={
            'ownerId':user,
        }

        Fetch_Operators=requests.post('https://www.fishguard.in/Fuel/index.php/Fuel_Controller/fetchEmployee',data=data1).json()

        # print(Fetch_Operators)

        responseCode = Fetch_Operators['responseCode']
        loadEmployee=""
        if responseCode == 1:

            loadEmployee = Fetch_Operators['loadEmployee']

            print(loadEmployee)
 

        context={
            'loadEmployee':loadEmployee,
            'user':user,
        }


        return render(request,'operators.html',context)
        
    return redirect('Login')
    

def Hotspot(request):
    if 'User_Id' in request.session:
        request.session['Custom']=""
        request.session['fill_fuel_mode']=""
        request.session['Fuel_Date']=""

        return render(request,'hotspot.html') 
        
    return redirect('Login')
    
       

def Notification_Delay(request):
    type = request.session["Type"]
    Generator_Access = ""
    if type == "2":


        Generator_Access = request.session['Generator_Access'] 
    if 'User_Id' in request.session:
        request.session['Custom']=""
        request.session['fill_fuel_mode']=""
        request.session['Fuel_Date']=""

        user = request.session['User_Id']

        if request.method == "POST":

            dela = int(request.POST['delay'])
            
            delay = dela * 60
            print(delay)
            
            data1 = {
                'userId':user,
                'delay':delay
                

            }
            delayUpdation = requests.post('https://www.fishguard.in/Fuel/index.php/Fuel_Controller/delayUpdation',data=data1).json()

            print(delayUpdation)

            return redirect('Notification_Delay')

        data2={
            'userId':user,
        }    

        fetchdelay = requests.post('https://www.fishguard.in/Fuel/index.php/Fuel_Controller/fetchDelay',data=data2).json()

        print(fetchdelay)

        responseCode=fetchdelay['responseCode']
        delay2 =0
        if responseCode == 1:

            dela2 = float(fetchdelay['delay'])

            delay2 =dela2/60

        context={
            'delay2':delay2,
            'type':type,
            'Generator_Access':Generator_Access,
            'user':user,
            
        }



        return render(request,'notification_delay.html',context)
        
    return redirect('Login')

    


def Add_Users(request):
    if 'User_Id' in request.session:

        user = request.session['User_Id']



        if request.method=="POST":

            name=request.POST['name']
            email = request.POST['email']
            password = request.POST['password']
            GeneratorS ="_".join(request.POST.getlist('GeneratorS'))

            temp = request.POST.getlist('Access')

            Power_Access=0
            Purchase_Access=0
            Service_Access=0
            Fill_Access=0
            Generator_Access=0
            Report_Access=0
            Device_Access=0



            for i in temp:
                if i =='Power Access':
                    Power_Access=1
                if i =='Purchase Access':
                    Purchase_Access=1    
                if i =='Service Access':
                    Service_Access=1
                if i =='Fill Access':
                    Fill_Access=1  
                if i =='Generator Access':
                    Generator_Access=1    
                if i =='Report Access':
                    Report_Access=1
                if i =='Report Access':
                    Device_Access=1    
    

            Access_list=[str(Power_Access),str(Purchase_Access),str(Service_Access),str(Fill_Access),str(Generator_Access),str(Report_Access),str(Device_Access)]
            Access="_".join(Access_list)


            data2={
                'name':name,
                'ownerId':user,
                'userName':email,
                'type':'2',
                'genType':GeneratorS,
                'facility':Access,
                'password':password
            }

            Add_Operator = requests.post('https://www.fishguard.in/Fuel/index.php/Fuel_Controller/addEmployee',data=data2).json()

            print(Add_Operator)

            responseCode =  Add_Operator['responseCode']

            if responseCode == 2:
                messages.info(request, 'Email already exists')
                return redirect('Add_Operator')

            return redirect('Users')    
                

            


        data1={
            'user_id':user,
        }

        Get_Generator = requests.post('https://www.fishguard.in/Fuel/index.php/Fuel_Controller/fetchGen',data=data1).json()

        # print(Get_Generator)

        responseCode = Get_Generator['responseCode']
        beanGenerator=""
        if responseCode == 1:

            beanGenerator = Get_Generator['beanGenerator']

            # print(beanGenerator)

        context={
            'beanGenerator':beanGenerator,
            'user':user,
        } 

        return render(request,'add_operators.html',context)
        
    return redirect('Login')
    
def Edit_Users(request,id):

    user = request.session['User_Id']


    if request.method=="POST":
        userName = request.POST['userName']
        name=request.POST['name']
        GeneratorS ="_".join(request.POST.getlist('GeneratorS'))

        temp = request.POST.getlist('Access')

        Power_Access=0
        Purchase_Access=0
        Service_Access=0
        Fill_Access=0
        Generator_Access=0
        Report_Access=0
        Device_Access=0



        for i in temp:
            if i =='Power Access':
                Power_Access=1
            if i =='Purchase Access':
                Purchase_Access=1    
            if i =='Service Access':
                Service_Access=1
            if i =='Fill Access':
                Fill_Access=1  
            if i =='Generator Access':
                Generator_Access=1    
            if i =='Report Access':
                Report_Access=1
            if i =='Device Access':
                Device_Access=1    


        Access_list=[str(Power_Access),str(Purchase_Access),str(Service_Access),str(Fill_Access),str(Generator_Access),str(Report_Access),str(Device_Access)]
        Access="_".join(Access_list)


        data2={
            'empId':id,
            'name':name,
            'userName':userName,
            'genType':GeneratorS,
            'facility':Access,
        }
        Edit_Operator = requests.post('https://www.fishguard.in/Fuel/index.php/Fuel_Controller/editEmployee',data=data2).json() 
        # print(Edit_Operator)

        return redirect('Users')




    data1={
            'ownerId':user,
    }

    Fetch_Operators=requests.post('https://www.fishguard.in/Fuel/index.php/Fuel_Controller/fetchEmployee',data=data1).json()

    # print(Fetch_Operators)

    responseCode = Fetch_Operators['responseCode']
    loadEmployee="" 

    employee=""   
    if responseCode == 1:

        loadEmployee = Fetch_Operators['loadEmployee']

        for i in loadEmployee:
            if id == i['employeeId']:
                employee =[i]

        for i in employee:
            genType= i['genType']
            facility=i['facility']

        print(genType)  
        
        Gen =genType.split('_')
        access=facility.split('_')

        print(access)

        Power_Access=access[0]
        Purchase_Access=access[1]
        Service_Access=access[2]
        Fill_Access=access[3]
        Generator_Access=access[4]
        Report_Access=access[5]
        Device_Access=access[6]

 
        # print(loadEmployee)
 
    data1={
            'user_id':user,
        }

    Get_Generator = requests.post('https://www.fishguard.in/Fuel/index.php/Fuel_Controller/fetchGen',data=data1).json()

        # print(Get_Generator)

    responseCode = Get_Generator['responseCode']
    beanGenerator=""
    if responseCode == 1:

        beanGenerator = Get_Generator['beanGenerator']
    context={
            'loadEmployee':loadEmployee,
            'employee':employee,
            'beanGenerator':beanGenerator,
            'Gen':Gen,
            'access':access,
            'Power_Access':Power_Access,
            'Purchase_Access':Purchase_Access,
            'Service_Access':Service_Access,
            'Fill_Access':Fill_Access,
            'Generator_Access':Generator_Access,
            'Report_Access':Report_Access,
            'Device_Access':Device_Access,
            'user':user,

    }

    return render(request,'edit_operator.html',context)

    
def Update_Status(request,id):

    if request.method=='POST':
        status = request.POST['status']

        if status =="":
            status="yes"

        data1={
            'employeeId':id,
            'status':status,
        }

        Update_status = requests.post('https://www.fishguard.in/Fuel/index.php/Fuel_Controller/editEmployeeStatus',data=data1).json()

        print(Update_status)




        return redirect('Operators') 



    return redirect('Users')    


def Add_Device(request):
    if 'User_Id' in request.session:
        
        user=request.session['User_Id']

        type = request.session["Type"]
        Purchase_Access = ""
        Service_Access = ""

        if type == "2":

            Purchase_Access = request.session['Purchase_Access']  

            Service_Access = request.session['Service_Access'] 
        if request.method=='POST':
            user=request.session['User_Id']
            # print(user)
            deviceId=request.POST['device_Id']
            # print(deviceId)
            

            deviceName=request.POST['device_name']
            # print(deviceName)
            levelType=request.POST['level_type']
            # print(levelType)
            deviceType=request.POST['device_type']
            # print(deviceType)

            start="Continues"
            # print(start)
            stop ="Continues"
            # print(stop)
            ssid=request.POST['ssid']
            # print(ssid)
            password=request.POST['password']
            # print(password)

            genId = request.session["Gen_Id"]
            # print(genId)

            underVoltage=request.POST['under_voltage']
            # print(underVoltage)
            underFrequency=request.POST['under_frequency']
            # print(underFrequency)
            batteryVoltage=request.POST['Battery_voltage']
            # print(genId )
            crankingTime= request.POST['cranking_time']
            # print(batteryVoltage)
            pollingTime=request.POST['polling_time']
            # print(pollingTime)
            lowLevel=request.POST['low_fuel_level']
            # print(lowLevel)

            choke="yes"
            # print(choke)
            chokeTimer=15
            # print(chokeTimer)
            
           
            data1={

                'userId':user,
                'deviceName':deviceName,
                'deviceType':deviceType,
                'levelType':levelType,
                'start':start,
                'stop':stop ,
                'ssid':ssid,
                'password':password,
                'genId':genId,
                'underVoltage':underVoltage,
                'underFrequency':underFrequency,
                'batteryVoltage':batteryVoltage,
                'crankingTime':crankingTime,
                'pollingTime':pollingTime,
                'lowLevel':lowLevel,
                'choke':choke,
                'chokeTimer':chokeTimer,
                'deviceId':deviceId,
                
            }

            add_dev=requests.post('https://www.fishguard.in/Fuel/index.php/Fuel_Controller/addDevice',data=data1).json()


            print(add_dev)

            if add_dev['responseCode'] == 2:

                messages.info(request, 'QR Code already exists. Scan a new QR Code')
                return redirect('Add_Device')
                
            return redirect('Home')

        context={
            'user':user,
            'Purchase_Access':Purchase_Access,
            'Service_Access':Service_Access,
            'type':type,
        }
        return render(request,'add_device.html',context)
        
    return redirect('Login')
    

def Power_Manager(request):
    if 'User_Id' in request.session:
        generator = request.session['Gen_Id']

        user = request.session['User_Id']

        type = request.session["Type"]

        Generator_Access = request.session['Generator_Access'] 

         

        Purchase_Access = request.session['Purchase_Access']  
 
        Service_Access = request.session['Service_Access'] 


        current_time = datetime.datetime.now()
        unix_timestamp = int(current_time.timestamp())
        # print(unix_timestamp)
        data1={
            'genId':generator,
        }


        fetchCurrentGenStatus= requests.post('https://www.fishguard.in/Fuel/index.php/Fuel_Controller/fetchCurrentGenStatus',data=data1).json()

        responseCode = fetchCurrentGenStatus['responseCode']
        loadCurrentGenStatus=""
        time=0
        if responseCode == 1:
            loadCurrentGenStatus = fetchCurrentGenStatus['loadCurrentGenStatus']

            for i in loadCurrentGenStatus:
                time=int(i['time'])
            print(time)
    
        print(loadCurrentGenStatus)
        # print(fetchCurrentGenStatus)
        

        data2={
            'userId':user,
        }

        fetchDeviceDetails=requests.post('https://www.fishguard.in/Fuel/index.php/Fuel_Controller/fetchDeviceDetails',data=data2).json()

        # print(fetchDeviceDetails)

        responseCode1 = fetchDeviceDetails['responseCode']
        PIM = 0
        difference=0
        X3pim=0
        pimgt=0
        if responseCode1 == 1:

            DeviceDetails = fetchDeviceDetails['loadDeviceDetails']

            # print(DeviceDetails)

            for i in DeviceDetails:

                PIM = int(i['PIM'])

            difference = unix_timestamp-time


            # print(difference)

            X3pim = PIM *3

            if X3pim > difference:
                pimgt = 1

            # print(pimgt)

        




        context = {
        'loadCurrentGenStatus':loadCurrentGenStatus,
        'pimgt':pimgt,
        'type':type,
        'Generator_Access':Generator_Access,
        'user':user,
        'Purchase_Access': Purchase_Access,
        'Service_Access':Service_Access,


        }
        return render(request,'power_manager.html',context)
        
    return redirect('Login')
    



def Automatic_mode(request):

    generator = request.session['Gen_Id']

    data1={
        'genId':generator,
        'status':'101'
    }

    Automatic_mode = requests.post('https://www.fishguard.in/Fuel/index.php/Fuel_Controller/setDeviceAutoManual',data=data1).json()

    print(Automatic_mode)


    return redirect('Power_Manager')

def Manul_mode(request):

    generator = request.session['Gen_Id']

    data1={
        'genId':generator,
        'status':'102'
    }

    Automatic_mode = requests.post('https://www.fishguard.in/Fuel/index.php/Fuel_Controller/setDeviceAutoManual',data=data1).json()

    print(Automatic_mode)


    return redirect('Power_Manager')



def Gen_on(request):

    generator = request.session['Gen_Id']

    data1={
        'genId':generator,
        'status':'105'
    }

    Gen_on = requests.post('https://www.fishguard.in/Fuel/index.php/Fuel_Controller/setDeviceDgOpenClose',data=data1).json()

    print(Gen_on)

    return redirect('Power_Manager')

def Gen_off(request):

    generator = request.session['Gen_Id']

    data1={
        'genId':generator,
        'status':'106'
    }

    Gen_off = requests.post('https://www.fishguard.in/Fuel/index.php/Fuel_Controller/setDeviceDgOpenClose',data=data1).json()

    print(Gen_off)

    return redirect('Power_Manager')



def Load_on_dg(request):

    generator = request.session['Gen_Id']

    data1={
        'genId':generator,
        'status':'104'
    }

    Load_on_dg = requests.post('https://www.fishguard.in/Fuel/index.php/Fuel_Controller/setDgRequest',data=data1).json()

    print(Load_on_dg)
    



    return redirect('Power_Manager')


def Load_on_eb(request):

    generator = request.session['Gen_Id']

    data1={
        'genId':generator,
        'status':'103'
    }

    Load_on_eb = requests.post('https://www.fishguard.in/Fuel/index.php/Fuel_Controller/setDgRequest',data=data1).json()

    print(Load_on_eb)
    



    return redirect('Power_Manager')



def alertmessage(request):

    messages.info(request, 'Please start generator first')

    return redirect('Power_Manager')

def alertmessage1(request):

    messages.info(request, 'Please set load on EB')

    return redirect('Power_Manager')








def Fill_Fuel(request):
    if 'User_Id' in request.session:


        
        type = request.session["Type"]

        Generator_Access = request.session['Generator_Access']
        Purchase_Access = request.session['Purchase_Access']  
        Service_Access = request.session['Service_Access']

        request.session['fill_fuel_mode']=""

        user = request.session['User_Id']
        if request.method=="POST":

            date = request.POST['date']
            time = request.POST['time']
            volume=request.POST['volume']
            Amount=request.POST['Amount']
            Pricelitre=request.POST['Pricelitre']

            generator = request.session['Gen_Id']

            user = request.session['User_Id']

            # print(date)
            # print(time)

            date_str = date
            time_str = time

            date_format = "%d-%m-%Y"
            time_format = "%I:%M %p"

            date = datetime.datetime.strptime(date_str, date_format)
            time = datetime.datetime.strptime(time_str, time_format)

            combined = datetime.datetime.combine(date.date(), time.time())
            timestamp = int(combined.timestamp())

            # print(timestamp)

            data1={

                'timestamp':timestamp,
                'genId':generator,
                'amountPerLitre':Pricelitre,
                'totalFilled':volume,
                'userId':user,
                
            }

            Add_Fill_Fuel = requests.post('https://www.fishguard.in/Fuel/index.php/Fuel_Controller/fillManual',data=data1).json()

            print(Add_Fill_Fuel)

            return redirect('Fill_Fuel')

            

        current_time = datetime.datetime.now().time()

        today = datetime.datetime.today()
    

        context = {
            'today':today,
            'current_time':current_time,
            'type':type,
            'Generator_Access':Generator_Access,
            'user':user,
            'Purchase_Access':Purchase_Access,
            'Service_Access':Service_Access,
                }
    
        return render(request,'fill_fuel.html',context) 
        
    return redirect('Login')
    



def Fill_Tank_Details(request):
    type = request.session["Type"]

    Generator_Access = request.session['Generator_Access']
    Purchase_Access = request.session['Purchase_Access']  
    Service_Access = request.session['Service_Access'] 
    
    if 'User_Id' in request.session:
        user = request.session["User_Id"]
        generator = request.session['Gen_Id']

        

        date3 = request.session['Fuel_Date'] 
        if request.method =="POST":
            date = request.POST['date']

            date1 = datetime.datetime.strptime(date, '%d-%m-%Y').date()


            request.session['Fuel_Date'] =str(date)

            
            
            # print(date)

            data2={
            'genId':generator,
            'timeAgo':date,
            'timeAfter':date,
            }

            Get_Fill_Tank = requests.post('https://www.fishguard.in/Fuel/index.php/Fuel_Controller/fetchFillManual',data=data2).json()

            print(Get_Fill_Tank)

            responseCode = Get_Fill_Tank['responseCode']
            fillManualArray=""
            Manual_Fill_Tank=0
            if responseCode == 1:

                fillManualArray = Get_Fill_Tank['fillManualArray']

                
                for i in fillManualArray:
                    
                    Manual_Fill_Tank += float(i['totalFilled'])  

                print(Manual_Fill_Tank) 
                
            Get_Auto_Fill_Tank = requests.post('https://www.fishguard.in/Fuel/index.php/Fuel_Controller/fetchFillAuto',data=data2).json()
            print(Get_Auto_Fill_Tank)


            responseCode2 = Get_Auto_Fill_Tank['responseCode']

            Auto_Fill_Tank = 0

            if responseCode2 ==1:

                fillAutoArray = Get_Auto_Fill_Tank['fillAutoArray']
                # print(fillAutoArray)

                for i in fillAutoArray:
                    Auto_Fill_Tank += float(i['totalFilled'])  
                
                
            # print(Auto_Fill_Tank)

            Abnormal=round(Manual_Fill_Tank - Auto_Fill_Tank,1)

            


            Abnormality=abs(Abnormal)

            mode=""
            context={
                    'today':date1,
                    'fillManualArray':fillManualArray,
                    'Abnormality':Abnormality,
                    'mode':mode,
                    'type':type,
                    'Generator_Access':Generator_Access,
                    'user':user,
                    'Purchase_Access':Purchase_Access,
                    'Service_Access':Service_Access,
                    
                    
            }

            return render(request,'fill_tank_details.html',context)

                
        
        if date3 != "" :
        
            date = request.session['Fuel_Date'] 

            

            date1 = datetime.datetime.strptime(date, '%d-%m-%Y').date()

            data2={
            'genId':generator,
            'timeAgo':date,
            'timeAfter':date,
            }

            Get_Fill_Tank = requests.post('https://www.fishguard.in/Fuel/index.php/Fuel_Controller/fetchFillManual',data=data2).json()

            # print(Get_Fill_Tank)

            responseCode = Get_Fill_Tank['responseCode']
            mode = ""
            Manual_Fill_Tank=0
            if responseCode == 1:

                fillManualArray = Get_Fill_Tank['fillManualArray']

                for i in fillManualArray:
                    
                    Manual_Fill_Tank += float(i['totalFilled'])  

                
            
                if 'fill_fuel_mode' in request.session:

                    mode=request.session['fill_fuel_mode']

                
            Get_Auto_Fill_Tank = requests.post('https://www.fishguard.in/Fuel/index.php/Fuel_Controller/fetchFillAuto',data=data2).json()
            print(Get_Auto_Fill_Tank)


            responseCode2 = Get_Auto_Fill_Tank['responseCode']

            Auto_Fill_Tank = 0

            if responseCode2 ==1:

                fillAutoArray = Get_Auto_Fill_Tank['fillAutoArray']
                # print(fillAutoArray)

                for i in fillAutoArray:
                    Auto_Fill_Tank += float(i['totalFilled'])  
                
                
            print(Auto_Fill_Tank)

            Abnormal=round(Manual_Fill_Tank - Auto_Fill_Tank,1)

            


            Abnormality=abs(Abnormal)
            context={
                'today':date1,
                'fillManualArray':fillManualArray,
                'mode':mode,
                'Abnormality':Abnormality,
                'type':type,
                'Generator_Access':Generator_Access,
                'user':user,
                'Purchase_Access':Purchase_Access,
                'Service_Access':Service_Access,
            }

            return render(request,'fill_tank_details.html',context)

        else:


            today= datetime.datetime.now().date()
            print(today)
            mode = ""
            fillManualArray=""
            Abnormality=""
            data1={
                'genId':generator,
                'timeAgo':today,
                'timeAfter':today,
            }

            Get_Fill_Tank = requests.post('https://www.fishguard.in/Fuel/index.php/Fuel_Controller/fetchFillManual',data=data1).json()

            # print(Get_Fill_Tank)

            responseCode = Get_Fill_Tank['responseCode']
            
            request.session['Fuel_Date']=""
            
            Manual_Fill_Tank=0
            if responseCode == 1:

                fillManualArray = Get_Fill_Tank['fillManualArray']

                print(fillManualArray)
               
                for i in fillManualArray:
                    
                    Manual_Fill_Tank += float(i['totalFilled'])  

                print(Manual_Fill_Tank)    
                
                if 'fill_fuel_mode' in request.session:

                    mode=request.session['fill_fuel_mode']


        
            Get_Auto_Fill_Tank = requests.post('https://www.fishguard.in/Fuel/index.php/Fuel_Controller/fetchFillAuto',data=data1).json()
            # print(Get_Auto_Fill_Tank)


            responseCode2 = Get_Auto_Fill_Tank['responseCode']

            Auto_Fill_Tank = 0

            if responseCode2 ==1:

                fillAutoArray = Get_Auto_Fill_Tank['fillAutoArray']
                # print(fillAutoArray)

                for i in fillAutoArray:
                    Auto_Fill_Tank += float(i['totalFilled'])  
                
                
            print(Auto_Fill_Tank)

            Abnormal=round(Manual_Fill_Tank - Auto_Fill_Tank,1)

            


            Abnormality=abs(Abnormal)
            context={
                'today':today,
                'fillManualArray':fillManualArray,
                'mode':mode,
                'Abnormality':Abnormality,
                'type':type,
                'Generator_Access':Generator_Access,
                'user':user,
                'Purchase_Access':Purchase_Access,
                'Service_Access':Service_Access,
                    
                }

            return render(request,'fill_tank_details.html',context) 

        
    return redirect('Login')



def Edit_Fill_Fuel(request,id):
    if 'User_Id' in request.session:

        if request.method=='POST':
            fillManualId=id
            volume = request.POST['volume']
            Amount=request.POST['Amount']
            Pricelitre=request.POST['Pricelitre']
            user =  request.session['User_Id']

            data1={
                'fillManualId':fillManualId,
                'filledVolume': volume,
                'filledAmount':Amount,
                'pricePer':Pricelitre,
                'userId':user,
            }

            Edit_Fill_Fuel = requests.post('https://www.fishguard.in/Fuel/index.php/Fuel_Controller/editFillManual',data=data1).json()

            print(Edit_Fill_Fuel)

            request.session['fill_fuel_mode']="manual"
            




            return redirect('Fill_Tank_Details')
        
    return redirect('Login')




def Purchase(request):
    type = request.session["Type"]
    Generator_Access=""
    Purchase_Access = ""
    Service_Access = ""


    if type == "2":



        Generator_Access = request.session['Generator_Access'] 

        Purchase_Access = request.session['Purchase_Access']  

        Service_Access = request.session['Service_Access'] 


    if 'User_Id' in request.session:

        generator = request.session['Gen_Id']

        user = request.session['User_Id']

        

        if request.method == 'POST':
            types = request.POST['type']
            
            

            if types == 'This Month':

                first_day_of_month = today.replace(day=1).date()
                last_day_of_month = today.replace(day=calendar.monthrange(today.year, today.month)[1]).date()

                request.session['timeAgo']=str(first_day_of_month)
                request.session['timeAfter']=str(last_day_of_month)

                request.session['Custom']='This Month'

                data1={
                    'genId' : generator,
                    'timeAgo' : first_day_of_month,
                    'timeAfter': last_day_of_month,


                }
    

                Get_Purchase=requests.post('https://www.fishguard.in/Fuel/index.php/Fuel_Controller/fetchPurchase',data=data1).json() 

                

                responseCode = Get_Purchase['responseCode']
                # print(Get_Purchase)
                loadPurchase = ""
                if responseCode == 1:


                    

                    loadPurchase=Get_Purchase['loadPurchase']

                    # print(loadPurchase)

                context = {
                            'loadPurchase':loadPurchase,
                            'first_date':first_day_of_month,
                            'last_date':last_day_of_month,
                            'month':'This Month',
                            'type':type,
                            'Generator_Access':Generator_Access,
                            'user':user,
                            'Purchase_Access':Purchase_Access,
                            'Service_Access':Service_Access,


                }

                return render(request,'purchase.html',context)

                   


            if types == 'Custom':

                fm_date = request.POST['from_date']  
                to_date =  request.POST['to_date']
                print(fm_date)

                date_object1 = datetime.datetime.strptime(fm_date, '%d-%m-%Y').date()
                date_object2 = datetime.datetime.strptime(to_date, '%d-%m-%Y').date()

                print(date_object1)
                print(date_object2)

                request.session['timeAgo']=str(date_object1)
                request.session['timeAfter']=str(date_object2)

                request.session['Custom']='Custom'
               


                data1={
                    'genId' : generator,
                    'timeAgo' : date_object1,
                    'timeAfter': date_object2,


                }
    

                Get_Purchase=requests.post('https://www.fishguard.in/Fuel/index.php/Fuel_Controller/fetchPurchase',data=data1).json() 

                

                responseCode = Get_Purchase['responseCode']
                # print(Get_Purchase)
                loadPurchase = ""
                if responseCode == 1:


                    loadPurchase=Get_Purchase['loadPurchase']

                    # print(loadPurchase)

                context = {
                            'loadPurchase':loadPurchase,
                            'first_date':date_object1,
                            'last_date':date_object2,
                            'month':'custom',
                            'type':type,
                            'Generator_Access':Generator_Access,
                            'user':user,
                            'Purchase_Access':Purchase_Access,
                            'Service_Access':Service_Access,
                }

                return render(request,'purchase.html',context)

        
        if 'Custom' in request.session:

            

            if 'This Month' == request.session['Custom']:

                

                first_day_of_month=request.session['timeAgo']
                last_day_of_month=request.session['timeAfter']

                date_object1 = datetime.datetime.strptime(first_day_of_month, '%Y-%m-%d').date()
                date_object2 = datetime.datetime.strptime(last_day_of_month, '%Y-%m-%d').date()

                

                data1={
                    'genId' : generator,
                    'timeAgo' : first_day_of_month,
                    'timeAfter': last_day_of_month,


                }
    

                Get_Purchase=requests.post('https://www.fishguard.in/Fuel/index.php/Fuel_Controller/fetchPurchase',data=data1).json() 

                

                responseCode = Get_Purchase['responseCode']
                # print(Get_Purchase)
                loadPurchase = ""
                if responseCode == 1:

                    loadPurchase=Get_Purchase['loadPurchase']

                    # print(loadPurchase)

                context = {
                            'loadPurchase':loadPurchase,
                            'first_date':date_object1,
                            'last_date':date_object2,
                            'month':'This Month',
                            'type':type,
                            'Generator_Access':Generator_Access,
                            'user':user,
                            'Purchase_Access':Purchase_Access,
                            'Service_Access':Service_Access,
                }

                return render(request,'purchase.html',context)

            if 'Custom' == request.session['Custom']: 


                date_object1=request.session['timeAgo']
                date_object2=request.session['timeAfter']

                first_day_of_month = datetime.datetime.strptime(date_object1, '%Y-%m-%d').date()
                last_day_of_month = datetime.datetime.strptime(date_object2, '%Y-%m-%d').date()

                data1={
                    'genId' : generator,
                    'timeAgo' : date_object1,
                    'timeAfter': date_object2,


                }
    

                Get_Purchase=requests.post('https://www.fishguard.in/Fuel/index.php/Fuel_Controller/fetchPurchase',data=data1).json() 

                

                responseCode = Get_Purchase['responseCode']
                # print(Get_Purchase)
                loadPurchase = ""
                if responseCode == 1:

                    loadPurchase=Get_Purchase['loadPurchase']

                    # print(loadPurchase)

                context = {
                            'loadPurchase':loadPurchase,
                            'first_date':first_day_of_month,
                            'last_date':last_day_of_month,
                            'month':'custom',
                            'type':type,
                            'Generator_Access':Generator_Access,
                            'user':user,
                            'Purchase_Access':Purchase_Access,
                            'Service_Access':Service_Access,
                }

                return render(request,'purchase.html',context)      





        # first_day_of_month = today.replace(day=1).date()
        three_months_ago = date.today() + relativedelta(months=-3)

        
        last_day_of_month = datetime.datetime.now().date()

        
       
        print(three_months_ago)
        print(last_day_of_month)



        request.session['timeAgo']=str(three_months_ago)
        request.session['timeAfter']=str(last_day_of_month)



        # print(first_day_of_month)
        # print(last_day_of_month)



        data2={
                    'genId' : generator,
                    'timeAgo' : three_months_ago,
                    'timeAfter': last_day_of_month,


                }
    

        Get_Purchase2=requests.post('https://www.fishguard.in/Fuel/index.php/Fuel_Controller/fetchPurchase',data=data2).json() 
        loadPurchase = ""
        responseCode = Get_Purchase2['responseCode']
        if responseCode == 1:
            loadPurchase=Get_Purchase2['loadPurchase']
        # print(loadPurchase)

        context={
            'loadPurchase':loadPurchase,
            'first_date':three_months_ago,
            'last_date':last_day_of_month,
            'month':'custom',
            'type':type,
            'Generator_Access':Generator_Access,
            'user':user,
            'Purchase_Access':Purchase_Access,
            'Service_Access':Service_Access,

        }

        

        return render(request,'purchase.html',context) 
        
    return redirect('Login')
    
    


def Add_New_Purchase(request):

    type = request.session["Type"]
    Generator_Access = ""
    Purchase_Access = ""
    Service_Access = ""

    if type == "2":

        Generator_Access = request.session['Generator_Access'] 

        Purchase_Access = request.session['Purchase_Access']  

        Service_Access = request.session['Service_Access'] 

    
    
    if 'User_Id' in request.session:
        request.session['Custom']=""

        

        generator = request.session['Gen_Id']
        user = request.session['User_Id']
 
        if request.method=='POST':
            des=request.POST['Description']
            amt=request.POST['Amount']


            data1={
                'purchaseName':des,
                'genId':generator,
                'empId':user,
                'amount':amt,
            }

            Add_New_Purchase=requests.post('https://www.fishguard.in/Fuel/index.php/Fuel_Controller/addPurchase',data=data1).json()

            print(Add_New_Purchase)


            return redirect('Purchase')
            
        context={
            'type':type,
            'Generator_Access':Generator_Access,
            'user':user,
            'Purchase_Access':Purchase_Access,
            'Service_Access':Service_Access,

        }

        return render(request,'add_new_purchase.html',context)  
        
    return redirect('Login')
    
def Edit_Purchase(request,id):

    Purchase_Access = request.session['Purchase_Access']  

    Service_Access = request.session['Service_Access'] 
    if 'User_Id' in request.session:


        user=request.session['User_Id']
        Purchase_id=str(id)

        if request.method=="POST":


            purchaseName = request.POST['Description']
            amount = request.POST['Amount']
            user=request.session['User_Id']

            request.session['custom_date']="True"

            data1={
            'purchaseId':id,
            'purchaseName':purchaseName,
            'amount':amount,
            'userId':user,
                }

            Edit_Purchase=requests.post('https://www.fishguard.in/Fuel/index.php/Fuel_Controller/editPurchase',data=data1).json()
            print(Edit_Purchase)
            return redirect('Purchase')
    

        generator = request.session['Gen_Id']
        first_day_of_month = request.session['timeAgo']
        last_day_of_month=request.session['timeAfter']




        data1={
            'genId' : generator,
            'timeAgo' : first_day_of_month,
            'timeAfter': last_day_of_month,


                    }
        

        Get_Purchase2=requests.post('https://www.fishguard.in/Fuel/index.php/Fuel_Controller/fetchPurchase',data=data1).json() 

        # print(Get_Purchase2)

        loadPurchase=Get_Purchase2['loadPurchase']

        # print(loadPurchase)

        

        for i in loadPurchase:
            
            if i['purchaseId'] == Purchase_id :
                Purchase = [i]

        print(Purchase)        
                

        context={
            'Purchase':Purchase,
            'Purchase_id':Purchase_id,
            'user':user,
            'Purchase_Access':Purchase_Access,
            'Service_Access':Service_Access,
        }        
            

        return render(request,'edit_purchase.html',context)
    
    return redirect('Login')



def Service(request):
    if 'User_Id' in request.session:
        
        user=request.session['User_Id']
        generator = request.session['Gen_Id']

        type = request.session["Type"]
        Generator_Access = ""
        Purchase_Access = ""
        Service_Access = ""
        if type == "2":

            Generator_Access = request.session['Generator_Access'] 
            Purchase_Access = request.session['Purchase_Access']  

            Service_Access = request.session['Service_Access'] 

        if request.method == 'POST':
            types = request.POST['type']

            
            
            

            if types == 'This Month':

                first_day_of_month = today.replace(day=1).date()
                last_day_of_month = today.replace(day=calendar.monthrange(today.year, today.month)[1]).date()

                request.session['service_timeAgo']=str(first_day_of_month)
                request.session['service_timeAfter']=str(last_day_of_month)

                

                request.session['Custom']='This Month'

                

                data3={
                    'genId' : generator,
                    'timeAgo' : first_day_of_month,
                    'timeAfter': last_day_of_month,


                }
    

                Get_fetchService1=requests.post('https://www.fishguard.in/Fuel/index.php/Fuel_Controller/fetchService',data=data3).json() 

                

                responseCode = Get_fetchService1['responseCode']
                print(responseCode)
                loadService=""
                if responseCode == 1:


                    loadService=Get_fetchService1['loadService']

                    print(loadService)

                context = {
                            'loadService':loadService,
                            'first_date':first_day_of_month,
                            'last_date':last_day_of_month,
                            'month':'This Month',
                            'user':user,
                            'Purchase_Access':Purchase_Access,
                            'Service_Access':Service_Access,
                }

                return render(request,'service.html',context)

                    


            if types == 'Custom':

                fm_date = request.POST['from_date']  
                to_date =  request.POST['to_date']
                print(fm_date)

                date_object1 = datetime.datetime.strptime(fm_date, '%d-%m-%Y').date()
                date_object2 = datetime.datetime.strptime(to_date, '%d-%m-%Y').date()

                print(date_object1)
                print(date_object2)

                request.session['service_timeAgo']=str(fm_date)
                request.session['service_timeAfter']=str(to_date)

                request.session['Custom']='Custom'
               


                data1={
                    'genId' : generator,
                    'timeAgo' : date_object1,
                    'timeAfter': date_object2,


                }
    

                Get_fetchService2=requests.post('https://www.fishguard.in/Fuel/index.php/Fuel_Controller/fetchService',data=data1).json() 

                print(Get_fetchService2)

                
                loadService=""
                responseCode = Get_fetchService2['responseCode']
                # print(Get_Purchase)

                if responseCode == 1:


                    loadService=Get_fetchService2['loadService']

                    # print(loadPurchase)

                context = {
                            'loadService':loadService,
                            'first_date':date_object1,
                            'last_date':date_object2,
                            'month':'custom',
                            'type':type,
                            'Generator_Access':Generator_Access,
                            'user':user,
                            'Purchase_Access':Purchase_Access,
                            'Service_Access':Service_Access,
                }

                return render(request,'service.html',context)

        
        if 'Custom' in request.session:

            

            

            if 'This Month' == request.session['Custom']:

                

                first_day_of_month=request.session['service_timeAgo']
                last_day_of_month=request.session['service_timeAfter']

                date_object1 = datetime.datetime.strptime(first_day_of_month, '%Y-%m-%d').date()
                date_object2 = datetime.datetime.strptime(last_day_of_month, '%Y-%m-%d').date()

                data1={
                    'genId' : generator,
                    'timeAgo' : first_day_of_month,
                    'timeAfter': last_day_of_month,


                }
    

                Get_fetchService2=requests.post('https://www.fishguard.in/Fuel/index.php/Fuel_Controller/fetchService',data=data1).json() 

                

                responseCode = Get_fetchService2['responseCode']
                # print(Get_Purchase)
                loadService=""
                if responseCode == 1:

                    loadService=Get_fetchService2['loadService']

                    # print(loadPurchase)

                context = {
                            'loadService':loadService,
                            'first_date':date_object1,
                            'last_date':date_object2,
                            'month':'This Month',
                            'type':type,
                            'Generator_Access':Generator_Access,
                            'user':user,
                            'Purchase_Access':Purchase_Access,
                            'Service_Access':Service_Access,

                
                }

                return render(request,'service.html',context)

            if 'Custom' == request.session['Custom']: 


                date_object1=request.session['service_timeAgo']
                date_object2=request.session['service_timeAfter']

                first_day_of_month = datetime.datetime.strptime(date_object1, '%d-%m-%Y').date()
                last_day_of_month = datetime.datetime.strptime(date_object2, '%d-%m-%Y').date()

                print(date_object1)
                data1={
                    'genId' : generator,
                    'timeAgo' : date_object1,
                    'timeAfter': date_object2,


                }
    

                Get_fetchService2=requests.post('https://www.fishguard.in/Fuel/index.php/Fuel_Controller/fetchService',data=data1).json() 

                

                responseCode = Get_fetchService2['responseCode']
                # print(Get_Purchase)
                loadService=""
                if responseCode == 1:

                    loadService=Get_fetchService2['loadService']

                    # print(loadPurchase)

                context = {
                            'loadService':loadService,
                            'first_date':first_day_of_month,
                            'last_date':last_day_of_month,
                            'month':'custom',
                            'type':type,
                            'Generator_Access':Generator_Access,
                            'user':user,
                            'Purchase_Access':Purchase_Access,
                            'Service_Access':Service_Access,
                }

                return render(request,'service.html',context)      





        # first_day_of_month = today.replace(day=1).date()
        three_months_ago = date.today() + relativedelta(months=-3)

        
        last_day_of_month = datetime.datetime.now().date()

        
       
        # print(three_months_ago)
        # print(last_day_of_month)



        request.session['service_timeAgo']=str(three_months_ago)
        request.session['service_timeAfter']=str(last_day_of_month)



        # print(first_day_of_month)
        # print(last_day_of_month)



        data2={
                    'genId' : generator,
                    'timeAgo' : three_months_ago,
                    'timeAfter': last_day_of_month,


                }
    

        Service=requests.post('https://www.fishguard.in/Fuel/index.php/Fuel_Controller/fetchService',data=data2).json() 
        print(Service)

        responseCode = Service['responseCode']

        loadService=""
        if responseCode != 0:

            loadService=Service['loadService']
        

        context={
            'loadService':loadService,
            'first_date':three_months_ago,
            'last_date':last_day_of_month,
            'month':'custom',
            'type':type,
            'Generator_Access':Generator_Access,
            'user':user,
            'Purchase_Access':Purchase_Access,
            'Service_Access':Service_Access,

        }

        

        return render(request,'service.html',context) 
        
    return redirect('Login')
    


def Add_New_Service(request):
    if 'User_Id' in request.session:

        generator = request.session['Gen_Id']
        user = request.session['User_Id']
        type = request.session["Type"]

        Generator_Access = ""
        Purchase_Access = ""
        Service_Access = ""

        if type == "2":

            Generator_Access = request.session['Generator_Access'] 

            Purchase_Access = request.session['Purchase_Access']  

            Service_Access = request.session['Service_Access'] 
 

        if request.method=="POST":
            service = request.POST['service']
            Amount = request.POST['Amount']

            data1={
                'serviceName':service,
                'genId':generator,
                'empId':user,
                'amount':Amount,
            }

            Add_Service = requests.post('https://www.fishguard.in/Fuel/index.php/Fuel_Controller/addService',data=data1)

            # print(Add_Service)



            return redirect('Add_New_Service')

        context={
            'type':type,
            'Generator_Access':Generator_Access,
            'user':user,
            'Purchase_Access':Purchase_Access,
            'Service_Access':Service_Access,
        }    

        return render(request,'add_new_service.html',context)  
        
    return redirect('Login')
    
def Edit_Service(request,id):
    if 'User_Id' in request.session:
        user = request.session['User_Id']
        Purchase_Access = request.session['Purchase_Access']  

        Service_Access = request.session['Service_Access'] 

        Service_id=str(id)

        if request.method=="POST":

            serviceName = request.POST['Description']
            amount = request.POST['Amount']
            user=request.session['User_Id']

            request.session['custom_date']="True"

            data2={
            'serviceId':id,
            'serviceName':serviceName,
            'amount':amount,
            'userId':user,
                }

            EditService=requests.post('https://www.fishguard.in/Fuel/index.php/Fuel_Controller/editService',data=data2).json()
            print(EditService)
            return redirect('Service')
    

        generator = request.session['Gen_Id']
        first_day_of_month = request.session['service_timeAgo']
        last_day_of_month=request.session['service_timeAfter']




        data1={
            'genId' : generator,
            'timeAgo' : first_day_of_month,
            'timeAfter': last_day_of_month,


                    }
        

        Get_Service=requests.post('https://www.fishguard.in/Fuel/index.php/Fuel_Controller/fetchService',data=data1).json() 

        # print(Get_Service)

        loadPurchase=Get_Service['loadService']

        # print(loadPurchase)

        

        for i in loadPurchase:
            
            if i['serviceId'] == Service_id :
                Service = [i]
        print(Service)       
                

        context={
            'Service':Service,
            'Service_id':Service_id,
            'user':user,
            'Purchase_Access':Purchase_Access,
            'Service_Access':Service_Access,
        }        
            

        
        return render(request,'edit_service.html',context)
    
    return redirect('Login')

def Reports(request):
    if 'User_Id' in request.session:
        type = request.session["Type"]

        user = request.session["User_Id"]

        Generator_Access = request.session['Generator_Access']
        Purchase_Access = request.session['Purchase_Access']  

        Service_Access = request.session['Service_Access'] 

        generator = request.session['Gen_Id']
        
        Auto_Fill_Report=""
        Manual_Fill_Report=""
        Purchase_Report=""
        Service_Report=""
        
        if request.method == 'POST':
            types = request.POST['type']
            report_type = request.POST['report_type']
            
            if types == 'This Month':

                month='This Month'

                first_day_of_month = today.replace(day=1).date()
                last_day_of_month = today.replace(day=calendar.monthrange(today.year, today.month)[1]).date()

                request.session['Custom']='This Month'

                request.session['report_1_date']=str(first_day_of_month)
                request.session['report_2_date']=str(last_day_of_month)

                data1={
                    'genId' : generator,
                    'timeAgo' : first_day_of_month,
                    'timeAfter': last_day_of_month,
                    


                }

                if report_type =="Auto Fill Report":

                    report='Auto Fill Report'
                    Get_Auto_Fill_Report = requests.post('https://www.fishguard.in/Fuel/index.php/Fuel_Controller/fetchFillAuto',data=data1).json()

                    # print(Get_Auto_Fill_Report)
                    responseCode = Get_Auto_Fill_Report['responseCode']
                    
                    if responseCode == 1:

                        Auto_Fill_Report=Get_Auto_Fill_Report['fillAutoArray']

                        # print(Auto_Fill_Report)

                if report_type =="Manual Fill Report":

                    report='Manual Fill Report'
                    Get_Manual_Fill_Report = requests.post('https://www.fishguard.in/Fuel/index.php/Fuel_Controller/fetchFillManual',data=data1).json()

                    # print(Get_Manual_Fill_Report)
                    responseCode = Get_Manual_Fill_Report['responseCode']
                    
                    if responseCode == 1:

                        Manual_Fill_Report=Get_Manual_Fill_Report['fillManualArray']

                        # print(Auto_Fill_Report)        
                if report_type =="Purchase Report":

                    report='Purchase Report'
                    Get_Purchase_Report = requests.post('https://www.fishguard.in/Fuel/index.php/Fuel_Controller/fetchPurchase',data=data1).json()

                    # print(Get_Purchase_Report)
                    responseCode = Get_Purchase_Report['responseCode']
                    
                    if responseCode == 1:

                        Purchase_Report=Get_Purchase_Report['loadPurchase']

                        # print(Auto_Fill_Report) 
                               
                if report_type =="Service Report":

                    report='Service Report'
                    Get_Service_Report = requests.post('https://www.fishguard.in/Fuel/index.php/Fuel_Controller/fetchService',data=data1).json()

                    print(Get_Service_Report)
                    responseCode = Get_Service_Report['responseCode']
                    
                    if responseCode == 1:

                        Service_Report=Get_Service_Report['loadService']

                        # print(Auto_Fill_Report) 
                context={
                    'Auto_Fill_Report':Auto_Fill_Report,
                    'Manual_Fill_Report':Manual_Fill_Report,
                    'Purchase_Report':Purchase_Report,
                    'Service_Report':Service_Report,
                    'month':month,
                    'first_date':first_day_of_month,
                    'last_date':last_day_of_month,
                    'report':report,
                    'type':type,
                    'Generator_Access':Generator_Access,
                    'user':user,
                    'Purchase_Access':Purchase_Access,
                    'Service_Access':Service_Access,
                    


                }


                return render(request,'reports.html',context)

            if types == 'Custom':

                month='custom'

                print(month)

                first_day_of_month = request.POST['from_date']
                last_day_of_month = request.POST['to_date']

                date_object1 = datetime.datetime.strptime(first_day_of_month, '%d-%m-%Y').date()
                date_object2 = datetime.datetime.strptime(last_day_of_month, '%d-%m-%Y').date()

                request.session['report_1_date']=str(date_object1)
                request.session['report_2_date']=str(date_object2)


                request.session['Custom']='This Month'

                data1={
                    'genId' : generator,
                    'timeAgo' : first_day_of_month,
                    'timeAfter': last_day_of_month,
                    


                }

                if report_type =="Auto Fill Report":

                    report='Auto Fill Report'
                    Get_Auto_Fill_Report = requests.post('https://www.fishguard.in/Fuel/index.php/Fuel_Controller/fetchFillAuto',data=data1).json()

                    # print(Get_Auto_Fill_Report)
                    responseCode = Get_Auto_Fill_Report['responseCode']
                    
                    if responseCode == 1:

                        Auto_Fill_Report=Get_Auto_Fill_Report['fillAutoArray']

                        # print(Auto_Fill_Report)

                if report_type =="Manual Fill Report":

                    report='Manual Fill Report'
                    Get_Manual_Fill_Report = requests.post('https://www.fishguard.in/Fuel/index.php/Fuel_Controller/fetchFillManual',data=data1).json()

                    # print(Get_Manual_Fill_Report)
                    responseCode = Get_Manual_Fill_Report['responseCode']
                    
                    if responseCode == 1:

                        Manual_Fill_Report=Get_Manual_Fill_Report['fillManualArray']

                        # print(Auto_Fill_Report)        
                if report_type =="Purchase Report":

                    report='Purchase Report'
                    Get_Purchase_Report = requests.post('https://www.fishguard.in/Fuel/index.php/Fuel_Controller/fetchPurchase',data=data1).json()

                    # print(Get_Purchase_Report)
                    responseCode = Get_Purchase_Report['responseCode']
                    
                    if responseCode == 1:

                        Purchase_Report=Get_Purchase_Report['loadPurchase']

                        # print(Auto_Fill_Report) 
                               
                if report_type =="Service Report":

                    report='Service Report'
                    Get_Service_Report = requests.post('https://www.fishguard.in/Fuel/index.php/Fuel_Controller/fetchService',data=data1).json()

                    print(Get_Service_Report)
                    responseCode = Get_Service_Report['responseCode']
                    
                    if responseCode == 1:

                        Service_Report=Get_Service_Report['loadService']

                        # print(Auto_Fill_Report) 
                context={
                    'Auto_Fill_Report':Auto_Fill_Report,
                    'Manual_Fill_Report':Manual_Fill_Report,
                    'Purchase_Report':Purchase_Report,
                    'Service_Report':Service_Report,
                    'month':month,
                    'first_date':date_object1,
                    'last_date':date_object2,
                    'report':report,
                    'type':type,
                    'Generator_Access':Generator_Access,
                    'user':user,
                    'Purchase_Access':Purchase_Access,
                    'Service_Access':Service_Access,
                    


                }


                return render(request,'reports.html',context)
                


        three_months_ago = date.today() + relativedelta(months=-3)
        last_day_of_month = datetime.datetime.now().date()

        month='custom'
        report="Auto Fill Report"
        context={
            'first_date':three_months_ago,
            'last_date':last_day_of_month,

            'Auto_Fill_Report':Auto_Fill_Report,
            'Manual_Fill_Report':Manual_Fill_Report,
            'Purchase_Report':Purchase_Report,
            'Service_Report':Service_Report,
            'month':month,
                    
            'report':report,
            'type':type,
            'Generator_Access':Generator_Access,
            'user':user,
            'Purchase_Access':Purchase_Access,
            'Service_Access':Service_Access,
                    



        }


        return render(request,'reports.html',context)
        
    return redirect('Login')
     


def Login(request):
    if 'User_Id' in request.session:
        return redirect('Home')
    if request.method=='POST':
        username = request.POST['username']
        password = request.POST['password']

        data = {'userName':username,
                'passWord':password,
        }
        sinup= requests.post('https://www.fishguard.in/Fuel/index.php/Fuel_Controller/login',data=data).json()
        print(sinup)

        response = sinup['responseCode'] 

        print(response)

        type=""
        phone=""

        if response == 1:

            request.session["User_Id"] = username

            type=sinup['type']

            request.session["Type"] = type

            phone=sinup['phone']

            request.session["Phone"] = phone

            

            return redirect('Home')


        else:
            messages.info(request, 'Incorrect username or password!!!!!')
            print("Email not matched")
            return redirect('Login')
   

    return render(request,'Landingpage.html')   

def Register(request):

    if 'User_Id' in request.session:

       return redirect('Home')
    return render(request,'register.html') 
   
def Signup(request):
    if request.method=='POST':
        name=request.POST['name']
        house=request.POST['house']
        pincode=request.POST['pincode']
        locality=request.POST['locality']
        post=request.POST['post']
        district=request.POST['district']
        state=request.POST['state']
        credentials=request.POST['credentials']
        email=request.POST['email']
        
        password=request.POST['password']
        
        data = {'name': name, 'houseName':house,'pin':pincode, 'locality':locality,'city':post,'district':district,'state':state, 'email':email,'password':password ,'type':'1' }

        response = requests.post('https://www.fishguard.in/Fuel/index.php/Fuel_Controller/userDetails',data=data)
        print(response.text)

        request.session["User_Id"] = email

        return redirect('Verifications')

def Verifications(request):
    if 'User_Id' in request.session:

       return render(request,'otpverifications.html')
        
    return redirect('Register')
    

def otpgenerate(request):

    if 'User_Id' in request.session:

        if request.method=='POST':
            ph=request.POST['phone']
            code = str(random.randint(111111,999999))
            print(ph)
            print(code)

            request.session['Mobile']=ph

            data={'otp':code,'mobileNumber':ph}

            otp = requests.post('https://www.fishguard.in/Fuel/index.php/Fuel_Controller/otpSend',data=data).json()
            
            print(otp)

            response = otp['responseCode'] 
            print(response)
            request.session["otp1"] = code

            request.session["phone"] = ph

            return redirect(OTP)
        
        if 'phone' in request.session:

            code = str(random.randint(111111,999999))
            
            print(code)

            ph =request.session['phone']

            data={'otp':code,'mobileNumber':ph}

            otp = requests.post('https://www.fishguard.in/Fuel/index.php/Fuel_Controller/otpSend',data=data).json()
            
            print(otp)

            response = otp['responseCode'] 
            print(response)

            return redirect('OTP')


        
        
        
    return redirect('Register')
    
    

          

def OTP(request):

    if 'User_Id' in request.session:

       return render(request,'otp.html') 
        
    return redirect('Register')
    
           

def Verify(request):

    if 'User_Id' in request.session:

        code=request.session['otp1']
        otp= request.POST['otp']
       
        user= request.session['User_Id']
        phone=request.session['phone']

        print(user)
        print(phone)

        
        if code==otp:
            data={
                    'userId':user,
                    'phone':phone,
            }

            add_otp=requests.post('https://www.fishguard.in/Fuel/index.php/Fuel_Controller/updatePhone',data=data).json()
            print(add_otp)

            if add_otp['responseCode']== 2 :

                messages.info(request, 'Phone number already exists')
                return redirect('Verifications')
                


            request.session["Phone"] = 1
            return redirect('Home')
        
    return redirect('Register')

 

def Logout(request):
    if 'User_Id' in request.session:
        request.session.flush()
        auth.logout(request) 
    return redirect('Login')







def Edit_Device(request):
    if 'User_Id' in request.session:
        Purchase_Access = request.session['Purchase_Access']  

        Service_Access = request.session['Service_Access'] 
        device_id= request.session['Device_Id']
        user = request.session['User_Id']
        type = request.session["Type"]
        data={
           'deviceId':device_id,
        }

        Get_Device_Details = requests.post('https://www.fishguard.in/Fuel/index.php/Fuel_Controller/fetchDeviceData',data=data).json()

        # print(Get_Device_Details)

        loadDevice=Get_Device_Details['loadDevice']

        # print(loadDevice)

        

        if request.method=='POST':
           level_type1=request.POST['level_type'] 
           ssid =request.POST['ssid']
           password=request.POST['password']
           under_voltage=request.POST['under_voltage']
           under_frequency=request.POST['under_frequency']
           Battery_voltage=request.POST['Battery_voltage']
           cranking_time=request.POST['cranking_time']
           polling_time=request.POST['polling_time']
           low_fuel_level=request.POST['low_fuel_level']

           user=request.session['User_Id']
           deviceId=request.session['Device_Id']
           genId = request.session['Gen_Id']

           print(user)
           print(deviceId)
           print(genId)

           data={
            'deviceId':deviceId,
           }

           get_device = requests.post('https://www.fishguard.in/Fuel/index.php/Fuel_Controller/fetchDeviceData',data=data).json()

        #    print(get_device)

           loadDevice2=get_device['loadDevice']

           print(loadDevice2)

           for i in loadDevice2:
                levelType2=i['levelType']
                deviceName=i['deviceName']
                deviceType=i['deviceType']
                start=i['start']
                stop=i['stop']
                choke=i['choke']
                chokeTimer=i['chokeTimer']


           if level_type1 =="":
                level_type1=levelType2


           data1={

            'userId':user,
            'deviceName':deviceName,
            'deviceType':deviceType,
            'levelType':level_type1,
            'start':start,
            'stop':stop,
            'ssid':ssid,
            'password':password,
            'genId':genId,
            'underVoltage':under_voltage,
            'underFrequency':under_frequency,
            'batteryVoltage':Battery_voltage,
            'crankingTime':cranking_time,
            'pollingTime':polling_time,
            'lowLevel':low_fuel_level,
            'deviceId':deviceId,
            'choke':choke,
            'chokeTimer':chokeTimer,

           }

           edit_device = requests.post('https://www.fishguard.in/Fuel/index.php/Fuel_Controller/editDevice',data=data1).json()
           print(edit_device)

           return redirect('Home')   

        context={
            'loadDevice':loadDevice,
            'user':user,
            'Purchase_Access':Purchase_Access,
            'Service_Access':Service_Access,
            'type':type,
        }


        return render(request,'edit_device.html',context)   
        
    return redirect('Login')





def Edit_Application(request):
    if 'User_Id' in request.session:

        user = request.session['User_Id']
        genId = request.session['Gen_Id']


        if request.method=='POST':
            user=request.session['User_Id']
           
            name=request.POST['name']

            shape=request.POST['shape']
            totalFuel= request.POST['totalFuel']

            consumption=0

            rectanklength=request.POST['rectanklength']
            rectankwidth=request.POST['rectankwidth']
            rectankheight=request.POST['rectankheight']
            rectankslope=request.POST['rectankslope']
            vctankheight=request.POST['vctankheight']
            htanklenght=request.POST['htanklenght']
            vc_h_tankslope=request.POST['vc_h_tankslope']
            vc_h_tankradious=request.POST['vc_h_tankradious']


            enginmake=request.POST['engine_make']

            ratinginkw = request.POST['rating_kw']

            application_type =request.POST['application']

            ratingInHp=0

            if application_type == 'Fire Engine':

                ratingInHp=request.POST['hp']


            


            phase=request.POST['phase']


            valueZero = 0
            value25 = 0
            value50 = 0
            value75 = 0
            value100 = 0
            engineMakename=""
            if enginmake == "Others":
                valueZero = request.POST['valueZero']
                value25 = request.POST['value25']
                value50 = request.POST['value50']
                value75 = request.POST['value75']
                value100 = request.POST['value100']

                engineMakename = request.POST['other_enginmake']

            ratingInKWname=""
            
            if ratinginkw == "Others":

                ratingInKWname = request.POST['other_Kw']


            length=0
            width=0
            height=0
            radious=0
            slope=0
            volume=0
            if 'Rectangle' == shape:
                length=rectanklength
                width=rectankwidth
                height=rectankheight
                slope=rectankslope

                
                volume=float(length)*float(width)*float(height)/1000
                


            if 'Vertical' == shape:
                height=vctankheight
                slope=vc_h_tankslope
                radious=vc_h_tankradious

                volume=3.14*float(radious)*float(radious)*float(height)/1000


            if 'Horizontal' == shape:
                length=htanklenght
                slope=vc_h_tankslope
                radious=vc_h_tankradious

                volume=3.14*float(radious)*float(radious)*float(length)/1000
    
            print(totalFuel)
            print(volume)
            if ((volume >=float(totalFuel) ) and (volume <= float(totalFuel) + 1)):
                
                
                data1={
                    'userId':user,
                    'name':name,
                    'shape':shape,
                    'totalFuel':totalFuel,
                    'length':length,
                    'width':width,
                    'height':height,
                    'radious':radious,
                    'slope':slope,
                    'consumption':consumption,
                    'engineMake':enginmake,
                    'ratingInKW':ratinginkw,
                    'ratingInHp':ratingInHp,
                    'phase':phase,
                    'application':application_type,
                    'valueZero':valueZero,
                    'value25':value25,
                    'value50':value50,
                    'value75':value75,
                    'value100':value100,
                    'engineMakename':engineMakename,
                    'ratingInKWname':ratingInKWname,




                }

                edit_device=requests.post('https://www.fishguard.in/Fuel/index.php/Fuel_Controller/editGen',data=data1).json()
                print(edit_device)

                return redirect(Home)
            else:
                    
                messages.info(request, 'Check Tank Dimensions')

                return redirect('Edit_Application')

        fetchEnginMake = requests.post('https://www.fishguard.in/Fuel/index.php/Fuel_Controller/listEngineMake').json()

        # print(fetchEnginMake)

        listEngineMake = fetchEnginMake['listEngineMake']

        # for item in my_list :
        #      if forloop.first :
        #    item 
      
        print(listEngineMake)

        first_engine_make='Cummins'
        for engine in listEngineMake:
            first_engine_make = engine['engineMake']
            print(first_engine_make)
            break

        pra={
            'enginMake':first_engine_make,
        }

        fetchKw = requests.post('https://www.fishguard.in/Fuel/index.php/Fuel_Controller/listKW',data=pra).json()

        listKw=fetchKw['listKw']
        # print(fetchKw)


        data={
            'user_id': user
        }

        get_generator= requests.post('https://www.fishguard.in/Fuel/index.php/Fuel_Controller/fetchGen',data=data).json()

        # print(get_generator)

        beanGenerator = get_generator['beanGenerator'] 
        # print(beanGenerator)
        for i in beanGenerator:
            if i['genId']==genId:
                Generator = [i]

        print(Generator)        


        context={
            'Generator':Generator,
            'user':user,
            'listEngineMake':listEngineMake,
            'listKw':listKw,
        }        


        return render(request,'edit_generator.html',context)

        
        
    return redirect('Login')



def link_callback(uri, rel):
    # Convert HTML/CSS relative paths to absolute paths
    sUrl = settings.STATIC_URL
    sRoot = settings.STATICFILES_DIRS
    mUrl = settings.MEDIA_URL
    mRoot = settings.MEDIA_ROOT

    if uri.startswith(mUrl):
        path = os.path.join(mRoot, uri.replace(mUrl, ""))
    elif uri.startswith(sUrl):
        path = os.path.join(sRoot, uri.replace(sUrl, ""))
    else:
        return uri  # not a static or media resource

    # Add the CSS file to the PDF document
    with open(path, "rb") as f:
        return f.read()
    return None


def Manul_report(request):
    

    Generator=request.session["Gen_Id"]

    user=request.session['User_Id']

    date1=request.session['report_1_date']
    date2=request.session['report_2_date']
    Manual_Fill_Report=""
    imgs=img.objects.all()
    data1={
            'user_id':user
            } 
    
    data2={
                    'genId' : Generator,
                    'timeAgo' : date1,
                    'timeAfter': date2,
                    


                }
    

    fetchGen=requests.post('https://www.fishguard.in/Fuel/index.php/Fuel_Controller/fetchGen',data=data1).json()

    
            
    beanGenerator= fetchGen['beanGenerator']

    # print(beanGenerator)
    genname=""
    for i in beanGenerator:
        if i['genId'] == Generator:
            genname=i['name']


    


    Get_Manual_Fill_Report = requests.post('https://www.fishguard.in/Fuel/index.php/Fuel_Controller/fetchFillManual',data=data2).json()

    # print(Get_Manual_Fill_Report)
    responseCode = Get_Manual_Fill_Report['responseCode']
    
    if responseCode == 1:

        Manual_Fill_Report=Get_Manual_Fill_Report['fillManualArray']



   
    context = {
        'genname':genname,
        'date1':date1,
        'date2':date2,
        'Manual_Fill_Report':Manual_Fill_Report,
        'imgs':imgs,
    
    }
   

    html = render_to_string('manul_report_pdf.html', context)

    # Generate the PDF using pisa
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'filename="Manul_Report.pdf"'
    pisa.CreatePDF(html, dest=response, link_callback=link_callback)

    return response




def Auto_report(request):
    

    Generator=request.session["Gen_Id"]

    user=request.session['User_Id']

    date1=request.session['report_1_date']
    date2=request.session['report_2_date']
    Auto_Fill_Report=""
    imgs=img.objects.all()
    data1={
            'user_id':user
            } 
    
    data2={
                    'genId' : Generator,
                    'timeAgo' : date1,
                    'timeAfter': date2,
                    


                }
    

    fetchGen=requests.post('https://www.fishguard.in/Fuel/index.php/Fuel_Controller/fetchGen',data=data1).json()

    
            
    beanGenerator= fetchGen['beanGenerator']

    # print(beanGenerator)
    genname=""
    for i in beanGenerator:
        if i['genId'] == Generator:
            genname=i['name']


    


    Get_Auto_Fill_Report = requests.post('https://www.fishguard.in/Fuel/index.php/Fuel_Controller/fetchFillAuto',data=data2).json()

    print(Get_Auto_Fill_Report)
    responseCode = Get_Auto_Fill_Report['responseCode']
    
    if responseCode == 1:

        Auto_Fill_Report=Get_Auto_Fill_Report['fillAutoArray']



   
    context = {
        'genname':genname,
        'date1':date1,
        'date2':date2,
        'Auto_Fill_Report':Auto_Fill_Report,
        'imgs':imgs,
    
    }
   

    html = render_to_string('auto_report_pdf.html', context)

    # Generate the PDF using pisa
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'filename="Auto_Report.pdf"'
    pisa.CreatePDF(html, dest=response, link_callback=link_callback)

    return response



def Purchase_report(request):
    

    Generator=request.session["Gen_Id"]

    user=request.session['User_Id']

    date1=request.session['report_1_date']
    date2=request.session['report_2_date']
    Purchase_Report=""
    imgs=img.objects.all()
    data1={
            'user_id':user
            } 
    
    data2={
                    'genId' : Generator,
                    'timeAgo' : date1,
                    'timeAfter': date2,
                    


                }
    

    fetchGen=requests.post('https://www.fishguard.in/Fuel/index.php/Fuel_Controller/fetchGen',data=data1).json()

    
            
    beanGenerator= fetchGen['beanGenerator']

    # print(beanGenerator)
    genname=""
    for i in beanGenerator:
        if i['genId'] == Generator:
            genname=i['name']


    


    Get_Purchase_Report = requests.post('https://www.fishguard.in/Fuel/index.php/Fuel_Controller/fetchPurchase',data=data2).json()

    # print(Get_Purchase_Report)
    responseCode = Get_Purchase_Report['responseCode']
    
    if responseCode == 1:

        Purchase_Report=Get_Purchase_Report['loadPurchase']



   
    context = {
        'genname':genname,
        'date1':date1,
        'date2':date2,
        'Purchase_Report':Purchase_Report,
        'imgs':imgs,
    
    }
   

    html = render_to_string('purchase_report_pdf.html', context)

    # Generate the PDF using pisa
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'filename="Purchase_Report.pdf"'
    pisa.CreatePDF(html, dest=response, link_callback=link_callback)

    return response


def Service_report(request):
    

    Generator=request.session["Gen_Id"]

    user=request.session['User_Id']

    date1=request.session['report_1_date']
    date2=request.session['report_2_date']
    Service_Report=""
    imgs=img.objects.all()
    data1={
            'user_id':user
            } 
    
    data2={
                    'genId' : Generator,
                    'timeAgo' : date1,
                    'timeAfter': date2,
                    


                }
    

    fetchGen=requests.post('https://www.fishguard.in/Fuel/index.php/Fuel_Controller/fetchGen',data=data1).json()

    
            
    beanGenerator= fetchGen['beanGenerator']

    # print(beanGenerator)
    genname=""
    for i in beanGenerator:
        if i['genId'] == Generator:
            genname=i['name']


    


    Get_Service_Report = requests.post('https://www.fishguard.in/Fuel/index.php/Fuel_Controller/fetchService',data=data2).json()

    print(Get_Service_Report)
    responseCode = Get_Service_Report['responseCode']
    
    if responseCode == 1:

        Service_Report=Get_Service_Report['loadService']



   
    context = {
        'genname':genname,
        'date1':date1,
        'date2':date2,
        'Service_Report':Service_Report,
        'imgs':imgs,
    
    }
   

    html = render_to_string('service_report_pdf.html', context)

    # Generate the PDF using pisa
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'filename="Service_Report.pdf"'
    pisa.CreatePDF(html, dest=response, link_callback=link_callback)

    return response




def google_login(request):

    google_user = request.user

    email = google_user.email
    fn = google_user.first_name
    ln = google_user.last_name
    name=fn+" "+ln

    data1={
        'personName':name,
        'personEmail':email,
    }

    google_login = requests.post('https://www.fishguard.in/Fuel/index.php/Fuel_Controller/gmailLogin',data=data1).json()
    print(google_login)


    response = google_login['responseCode'] 

    print(response)

    type=""
    phone=""

    if response == 1:

        request.session["User_Id"] = email

        type=google_login['type']

        request.session["Type"] = type

        phone=google_login['phone']

        request.session["Phone"] = phone


        return redirect('Home')

    
    return redirect('Login')
    # request.session["User_Id"] = email

    # return redirect('Home')

    # return render (request,'googlesignin.html')

def Reset_Password(request):

    if request.method=='POST':

        email = request.POST['email']

        otp_code = str(random.randint(1111,9999))

        request.session['Password_Otp']=otp_code

        request.session['Password_Email']=email

        
        print(otp_code)

        pra={
            'otp':otp_code,
            'email':email,
        }


        fuelOtp = requests.post('https://www.fishguard.in/Fuel/index.php/Fuel_Controller/fuelOtp',data=pra).json()
        print(fuelOtp)
        
        return redirect('Otp_Password')
    
    if 'Password_Email' in request.session:

        

        otp_code = str(random.randint(1111,9999))

        request.session['Password_Otp']=otp_code

        email = request.session['Password_Email']

        
        print(otp_code)

        pra={
            'otp':otp_code,
            'email':email,
        }


        fuelOtp = requests.post('https://www.fishguard.in/Fuel/index.php/Fuel_Controller/fuelOtp',data=pra).json()
        print(fuelOtp)
        
        return redirect('Otp_Password')


    return render(request,'reset_password.html')


def Otp_Password(request):

    if request.method == "POST":
        otp=request.POST['otp']

        if otp != request.session['Password_Otp']:
            messages.info(request, 'OTP is invalid try again')
            return redirect('Otp_Password')
        

        return redirect('New_Password')    
  

    return render(request,'otp_password.html')


def New_Password(request):

    if request.method == "POST":
        password = request.POST['password']
        email = request.session['Password_Email']

        pswd={
            'userId':email,
            'password':password

        }

        forgotPassword = requests.post('https://www.fishguard.in/Fuel/index.php/Fuel_Controller/forgotPassword',data=pswd).json()

        print(forgotPassword)

        request.session.flush()

        return redirect('Login')


    return render(request,'new_password.html')



def get_rating_kw(request):
    engine_make = request.GET.get('engine_make', None)

    pra={
        'enginMake':engine_make,
    }
    rating_kw_list = requests.post('https://www.fishguard.in/Fuel/index.php/Fuel_Controller/listKW',data=pra).json()

    listKw = rating_kw_list['listKw']

    

    
    return JsonResponse({'rating_kw_list': listKw})




def Emergency_Stop(request):
    generator = request.session["Gen_Id"] 

   

    pra1 = {
        'genId': generator,
        'status':107,
    }

    setDeviceEmergency = requests.post('https://www.fishguard.in/Fuel/index.php/Fuel_Controller/setDeviceEmergency',data=pra1).json()
    print(setDeviceEmergency)
           



    return redirect('Power_Manager')


def Restart(request):
    generator = request.session["Gen_Id"] 

   

    pra1 = {
        'genId': generator,
        'status':108,
    }

    setDeviceEmergency = requests.post('https://www.fishguard.in/Fuel/index.php/Fuel_Controller/setDeviceEmergency',data=pra1).json()
    print(setDeviceEmergency)
           



    return redirect('Power_Manager')



def contact(request):

    if request.method == "POST":
        name = request.POST['message_name']
        email = request.POST['message_email']
        ms= request.POST['message']

        messages = "Name : " + name +"\n \n" + "Email : " + email + "\n \n" +"Messages : " + ms


        send_mail (
            'FuelTM Contact Website Form ',#subject
            messages,# message
            email,#from message
            ['info@cabaltechnologies.com'],#to email

        )
        return render(request,'mailsuccess.html')
    return redirect('Home')