
from kafka import KafkaConsumer
from pymongo import MongoClient
import json


client = MongoClient("localhost", 27017)
db = client.test



while True:
        consumer = KafkaConsumer('topic-test2', group_id='my_favorite_group')
        for msg in consumer:
            record = json.loads(msg.value)
            print(record)
            name = record['name']
            age = record['age']
            address = record['address']
            phone = record['phone']
            mail = record['mail']
            update_time = record['update_time']
            try:
                a = {'name': name, 'age': age, 'address': address, 'phone': phone, 'mail': mail, 'update_time' :update_time}
                update_1 = db.user.update_one({"account_id":1}, { "$set": a})
                print("Data updated with record ")
            except:
                print("Could not update into MongoDB")



    



        

        
