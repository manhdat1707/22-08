
from kafka import KafkaConsumer
from pymongo import MongoClient
import json


client = MongoClient("localhost", 27017)
db = client.test




while True:
    consumer = KafkaConsumer('topic-test1', group_id='my_favorite_group')
    for msg in consumer:
        record = json.loads(msg.value)
        name = record['name']
        age = record['age']
        address = record['address']
        phone = record['phone']
        mail = record['mail']
        time_update = record['time_update']
        try:
            a = {'name': name, 'age': age, 'address': address, 'phone': phone, 'mail': mail, 'time_update' :time_update}
            update_1 = db.user.update_one({"account_id":1}, { "$set": a})
            print("Data updated with record ids", update_1)
        except:
            print("Could not update into MongoDB")



    



        

        
