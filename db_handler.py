from Settings import client



'''insertData = [
        
        {'Name':'suraj','user_id':'suraj123'},
        {'Name':'sushant','user_id':'sushant123'},
        {'Name':'pawan','user_id':'pawan123'},
        {'Name':'sanjay','user_id':'sanjay123'},

                  
    ] 
collection.insert_many(insertData)
'''
class database:
    def __init__ (self,client):
        #self.db = db
        self.client = client
        #self.collection = collection
        #self.Name = Name
        
    # writing files    
    def insert_data(self,collection,insertData):
        #self.collection = collection
        collection.insert_many(insertData)
       # pass
        return True
    #reading files   
    def read_data(self,collection):
        all_data = collection.find()
        for data in all_data:
            print(data)
            
    #update files
    
    def update(self,collection):
        data_u = collection.find_one({'Name':'suraj'})
        print(data_u)
        updating = {"$set": {"Name":"suraj das"},"$set":{"add":"delhi"}}
        collection.update_one(data_u,updating)


        #print()
    def delete(self,collection):
        pass
            
    

    