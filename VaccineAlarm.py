import requests
from datetime import date,datetime,timedelta
import os
import smtplib
from time import time,ctime,sleep
from playsound import playsound
import random


today = datetime.now()
tomorrow = today + timedelta(1)

age_limit = 45

__pincodes = ["400060","400093"]
__district = "395"
__preferance = "pincode";
minutes = 1

d1 = tomorrow.strftime("%d/%m/%Y")


__date = str(d1).replace("/","-")

def parse_json(result):
    output = []
    centers = result['centers']
    for center in centers:
        sessions = center['sessions']
        for session in sessions:
            if session['available_capacity'] > 0:
                res = { 'name': center['name'], 'block_name':center['block_name'],'age_limit':session['min_age_limit'], 'vaccine_type':session['vaccine'] , 'date':session['date'],'available_capacity':session['available_capacity'],'pincode':center['pincode'] }
                if session['min_age_limit'] == age_limit:
                    output.append(res)
    return output


def call_api():
    print(ctime(time()))
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.76 Safari/537.36'} # This is chrome, you can set whatever browser you like
    #api= 'https://cdn-api.co-vin.in/api/v2/appointment/sessions/calendarByDistrict?district_id=395&date='+__date
    #api= 'https://cdn-api.co-vin.in/api/v2/appointment/sessions/public/calendarByDistrict?district_id=395&date=09-05-2021'
    #api= 'https://cdn-api.co-vin.in/api/v2/appointment/sessions/calendarByDistrict?district_id=395&date=10-05-2021'
    if __preferance == 'pincode':
        for pincode in __pincodes:
            api=  'https://cdn-api.co-vin.in/api/v2/appointment/sessions/calendarByPin?pincode='+pincode+'&date='+__date
            print(api)
            response = requests.get(api,headers=headers)
            check_availablity(response)
            #print(response.json())
    else:
        api= 'https://cdn-api.co-vin.in/api/v2/appointment/sessions/calendarByDistrict?district_id='+__district+'&date='+__date

    #else:
        #api='https://cdn-api.co-vin.in/api/v2/appointment/sessions/calendarByDistrict?district_id='+district_id+'&date='+__date
   # https://cdn-api.co-vin.in/api/v2/appointment/sessions/public/calendarByDistrict?district_id=392&date=11-05-2021
    #api= 'https://cdn-api.co-vin.in/api/v2/appointment/sessions/public/findByDistrict?district_id=395&date=09-05-2021'



def check_availablity(response):
    if response.status_code == 200 :
        result=response.json()
        #print(result)
        output = parse_json(result)

        if len(output) > 0:
            print ("Vaccines available")
            print('\007')
            result_str = ""
            for center in output:

                '''print center['name']
                print "block:"+center['block_name']
                print "vaccine count:"+str(center['available_capacity'])
                print "vaccines type:" + center['vaccine_type']
                print center['date']
                print "age_limit:"+ str(center['age_limit'])
                print "---------------------------------------------------------" '''

                result_str = result_str + center['name'] + "\n"
                result_str = result_str + str(center['pincode']) + "\n"
                result_str = result_str + "block:"+center['block_name'] + "\n"
                result_str = result_str + "vaccine count:"+str(center['available_capacity']) + "\n"
                result_str = result_str + "vaccine type:"+ center['vaccine_type'] + "\n"
                result_str = result_str + center['date'] + "\n"
                result_str = result_str + "age_limit:"+str(center['age_limit'])+"\n"
                result_str = result_str + "-----------------------------------------------------\n"

                file = "office.mp3"

                print(result_str)
                playsound(file)
        else :
            print('not available')


#call_api()

t = datetime.now()

if __name__ == '__main__':
    call_api()
    while True:
        delta = datetime.now()-t
        minuitesRefresh=random.randint(1, minutes)
    #print(minuitesRefresh)
        if delta.seconds >= 0.5 * 60:
            call_api()
            t = datetime.now()
#   	#sleep(minutes * 60)
