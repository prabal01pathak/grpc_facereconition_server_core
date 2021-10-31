from concurrent import futures
import threading
import queue

from google.protobuf import message
import numpy as np
import grpc
from pymongo import database
import bidirectional_pb2_grpc as bidirectional_pb2_grpc
import bidirectional_pb2 as pb2
import utils
import random
from Settings import *
import db_handler
import face_recognition
import cv2
from etlpipe import EtlLayer
import logging
logging.basicConfig(filename='debug.log', level=logging.DEBUG)
logging.debug('This message should go to the log file')
db = client['FaceGenie_database']
collection = db['Face_registration']

# etl encoder 
ETL=EtlLayer()
ETL.loader()
a = db_handler.database(client)

# queue implementation
que =queue.Queue()



def recorder(frame,face_id):

    face_encodings =extractor(frame)
    if face_encodings ==None:
        return False
    else:
        try:
            logging.debug("pushing")
            if ETL.pushers(face_encodings,face_id)==True:
                print("pushed")
                return True
            else:
                return False


        except Exception as e:
            print("cant push encodings{}".format(e))
            return False

def extractor(frame):
    '''
    Extract face from frame and return encodings
    '''
    small_frame=cv2.resize(frame,(0,0),fx=0.25,fy=0.25)
    rgb_small_frame=small_frame[:,:,::-1]
    face_location=face_recognition.face_locations(rgb_small_frame,number_of_times_to_upsample=Number_of_times_to_upsample, model=Model_Type)
    
    if len(face_location)>0:
        face_encodings =face_recognition.face_encodings(rgb_small_frame,face_location)
        print(face_location)
        #print("extractor face encodings {}".format(face_encodings))
        return face_encodings
    else:
        return []

def custom_face_distance(face_encodings,face_to_compare):
    if len(face_encodings)==0:
        return np.empty((0))
    return np.linalg.norm(face_encodings-face_to_compare,axis=1)



def custom_compare_faces(k_encodings,face_to_compare,sensitivity=0.4):
    return list(custom_face_distance(k_encodings,face_to_compare)<=sensitivity)


def recognition(k_encodings,face_encoding,sensitivity,k_names):
    matches=custom_compare_faces(k_encodings,face_encoding,sensitivity)
    
    face_distance = custom_face_distance(k_encodings,face_encoding)
    best_match_index=np.argmin(face_distance)
    if matches[best_match_index]:
        return k_names[best_match_index]
    else:
        return "Unknown"

def sender(request,r1):
    print("function triggred with request")
    request = request
    img_arr=utils.convert_and_save(request.image)
    print(img_arr)
    img = cv2.imdecode(img_arr, flags=cv2.IMREAD_COLOR)
    
    print("r1 value {}".format(r1))    

    if recorder(img,request.uuid)==True:
        encoding = extractor(frame=img)
        #save registerd encodings
        try:
            # ETL.save() # you can also put this to demon thread so it will do all its process in background
            print("saved")
            # e,n=ETL.loader()
            # #=ETL.puller()
            # print("test {}".format(e))
             # this function is not triggering
            
            Etl_thread = threading.Thread(
                        target=ETL.save(),
                        name="ETL_puller",
                        args=(encoding,request.uuid,),
                    )
            Etl_thread.daemon = True
            Etl_thread.start()
        except:
            print("cant save")

        if os.path.exists(os.path.join(UPLOAD_PATH,request.uuid)):
            # path=os.path.join(Settings.BASE_DIRECTORY,UPLOAD_PATH,face_id)+'/'+str(r1)+".jpg
            print("creating directory")
            cv2.imwrite(os.path.join(UPLOAD_PATH,request.uuid)+'/'+str(r1)+".jpg",img)
            print("created dir")
            
            
        else:
            os.mkdir(os.path.join(UPLOAD_PATH,request.uuid))
            # path=os.path.join(Settings.BASE_DIRECTORY,UPLOAD_PATH,face_id))+'/'+str(r1)+".jpg"
            print("creating directory")
            cv2.imwrite(str(os.path.join(UPLOAD_PATH,request.uuid))+'/'+str(r1)+".jpg",img)
            print("created directory")
            
        print("register done")
        









class BidirectionalService(bidirectional_pb2_grpc.BidirectionalServicer):

    def GetServerResponse(self, request_iterator, context):
        '''
            this service work for bidirection face recognition        
        '''
        print("rcognition function triggered  {}".format(request_iterator))
        face_id = "unknown"
        for message in request_iterator:
            
            nparr = utils.convert_and_save(message.message)
            print("numpy array converted")
            img = cv2.imdecode(nparr, flags=cv2.IMREAD_COLOR)
            print("decodecd to image")
            


            #TODO: extract face encoding
            face_encodings =extractor(img)
            print(" encoded face {}".format(face_encodings))

            #TODO:get all encodings and labels from ETL.puller()
            k_encodings,k_names=ETL.loader()
            print("Length of known face encoding {}".format(k_encodings))
            if len(k_encodings)>0:
                
                for face_encoding in face_encodings:
                    face_id=recognition(k_encodings,face_encoding,Sensitivity,k_names)
                    print("Fcae id {}".format(face_id))
                    
                            
            else:
                face_id="unknown"
            
        return pb2.Message(message=face_id)
                

        #         yield face_id
                #face_id="no face found"
            
        # extract name of faceid
           #data= #a.read_data(collection)
        # a.update(collection)
        # print(a.client)

            #print(face_id)
            #yield face_id #data
            
    # function to register 
    
    def GetRegisterFace(self, request, context):
        #pass
        print(request.uuid)
        que.put(request)
        r1 = random.randint(0, 10)
        #sender(request,r1)
        
        thread_ = threading.Thread(
                        target=sender,
                        name="Thread1",
                        args=(request,r1,),
                    )
        thread_.daemon = True
        thread_.start()
        data=[{'uuid':request.uuid,'image_url':os.path.join(UPLOAD_PATH,request.uuid)+'/'+str(r1)+".jpg"},

                    ]
        try:

                    
            print(data)
            a.insert_data(collection=collection,insertData=data)
            print("inserted to data base")

        except Exception as e:
            print(e)
        
        #Todo register user in mongodb server
        
        #a.insert_data(collection=collection,insertData=data)
        return pb2.RegisterMessage(uuid=request.uuid,image=request.image)
            
        #return super().GetRegisterFace(request, context)
        #pass


def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    bidirectional_pb2_grpc.add_BidirectionalServicer_to_server(BidirectionalService(), server)
    bidirectional_pb2_grpc.add_FaceRegistrationServicer_to_server(BidirectionalService(),server)
    server.add_insecure_port('[::]:50052')
    server.start()
    print("server started")
    server.wait_for_termination()


if __name__ == '__main__':
    serve()