import sys
import requests
import json
import threading

Cluster_IP = str(sys.argv[1])
Cluster_Port = str(sys.argv[2])
Number_of_clients = int(sys.argv[3])
Tomorrows_date = str(sys.argv[4])
Debug = int(sys.argv[5])

def login_request():
    flag = 0
    URL = "http://" + Cluster_IP + ":" + Cluster_Port + "/api/v1/users/login"
    PARAMS = {'username':"fdse_microservice",'password':"111111",'verificationCode':"1234"}
    r = requests.post(url=URL, json=PARAMS)
    try:
    	result = r.json()
    except:
        flag = 1
        if(Debug == 1):
        	print("Login error! Response: " + str(r))
    if(flag == 0):
        if(Debug == 1):
           print(result)
        return result['data']['token'], result['data']['userId']

def travel_search():
    flag = 0
    URL = "http://" + Cluster_IP + ":" + Cluster_Port + "/api/v1/travelservice/trips/left"
    PARAMS = {"startingPlace":"Shang Hai","endPlace":"Su Zhou","departureTime":Tomorrows_date}
    r = requests.post(url=URL, json=PARAMS)
    try:
    	result = r.json()
    except:
        flag = 1
        if(Debug == 1):
        	print("Travel Search error! Response: " + str(r))
    if(flag == 0):
    	if(Debug == 1):
        	print("Travel Search result: " + str(result))

def book_travel():
	flag = 0
	URL = "http://" + Cluster_IP + ":" + Cluster_Port + "/client_ticket_book.html"
	PARAMS = {"tripId":"D1345","from":"Shang Hai","to":"Su Zhou","seatType":"2","seat_price":"50.0","date":Tomorrows_date}
	r = requests.get(url=URL, json=PARAMS)
	if(Debug == 1):
		print("Result: " + str(r))

def assurance_types(token): #Code 403
	URL = "http://" + Cluster_IP + ":" + Cluster_Port + "/api/v1/assuranceservice/assurances/types"
	PARAMS = {}
	r = requests.get(url=URL, json=PARAMS, headers={'Authorization':"Bearer " + token})
	if(Debug == 1):
		print("Result1: " + str(r))

def food_service():
    flag = 0
    URL = "http://" + Cluster_IP + ":" + Cluster_Port + "/api/v1/foodservice/foods/2020-03-26/Shang%20Hai/Su%20Zhou/D1345"
    PARAMS = {}
    r = requests.get(url=URL, json=PARAMS)
    try:
    	result = r.json()
    except:
        flag = 1
        if(Debug == 1):
        	print("Food Service error! Response: " + str(r))
    if(flag == 0):
    	if(Debug == 1):
        	print(result)

def preserve(token):
    flag = 0
    URL = "http://" + Cluster_IP + ":" + Cluster_Port + "/api/v1/preserveservice/preserve"
    PARAMS = {"accountId":"4d2a46c7-71cb-4cf1-b5bb-b68406d9da6f","contactsId":"231e4595-ccc7-4327-9c47-1a247f550e8f","tripId":"D1345","seatType":"2","date":Tomorrows_date,"from":"Shang Hai","to":"Su Zhou","assurance":"1","foodType":"2","stationName":"suzhou","storeName":"Roman Holiday","foodName":"Spicy hot noodles","foodPrice":"5"}
    r = requests.post(url=URL, json=PARAMS, headers={'Authorization':"Bearer " + token})
    if(Debug == 1):
    	print("Result2: " + str(r))
    try:
    	result = r.json()
    except:
        flag = 1
        if(Debug == 1):
        	print("Travel Search error! Response: " + str(r))
    if(flag == 0):
    	if(Debug == 1):
        	print(result)

def client_order_list(userID,token):
    flag = 0
    URL = "http://" + Cluster_IP + ":" + Cluster_Port + "/api/v1/orderservice/order/refresh"
    PARAMS = {"loginId":userID,"enableStateQuery":"false","enableTravelDateQuery":"false","enableBoughtDateQuery":"false","travelDateStart":"null","travelDateEnd":"null","boughtDateStart":"null","boughtDateEnd":"null"}
    r = requests.post(url=URL, json=PARAMS)
    try:
    	result = r.json()
    except:
        flag = 1
        if(Debug == 1):
        	print("Client Order List error! Response: " + str(r))
    if(flag == 0):
    	if(Debug == 1):
        	#print(result)
        	for i in range(0,len(result['data'])):
        		if(result['data'][i]['status'] == 0):
        			print("Number: " + str(i) + "--->" + str(result['data'][i]['id'])	)
        			confirm_payment(result['data'][i]['id'],result['data'][i]['trainNumber'],token)




def confirm_payment(orderID,tripID,token): #Completar
	URL = "http://" + Cluster_IP + ":" + Cluster_Port + "/api/v1/inside_pay_service/inside_payment"
	PARAMS = {"orderId":orderID,"tripId":tripID}
	r = requests.post(url=URL, json=PARAMS, headers={'Authorization':"Bearer " + token})
	print(r)



def thread_to_run(number):
    print("Thread " + str(number) + " starting...")
    token = None
    userID = None
    try:
    	(token, userID) = login_request()
    except:
    	print("ERROR -> Login returns null")
    travel_search()
    book_travel()
    if(token != None):
        preserve(token)
        assurance_types(token)
        food_service()
        client_order_list(userID,token)
    
    print("Thread " + str(number) + " ending...")

def main():
	for i in range(0,Number_of_clients):
		x = threading.Thread(target=thread_to_run, args=(i,))
		x.start()
	#print(Cluster_IP + ":" + Cluster_Port + ", " + str(Number_of_clients))


if __name__ == '__main__':
    main()