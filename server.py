from concurrent import futures

from google.protobuf import message
import numpy as np
import grpc
import bidirectional_pb2_grpc as bidirectional_pb2_grpc
import bidirectional_pb2 as pb2
import utils
import random
from Settings import *
from db_handler import database as db
import face_recognition
import cv2
from etlpipe import EtlLayer
db = client['FaceGenie_database']
collection = db['Face_registration']

# etl encoder 
ETL=EtlLayer()
ETL.loader()



def recorder(frame,face_id):

    face_encodings =extractor(frame)
    if face_encodings ==None:
        return False
    else:
        try:
            print("pushing")
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


a = db(client,db,collection)








class BidirectionalService(bidirectional_pb2_grpc.BidirectionalServicer):

    def GetServerResponse(self, request_iterator, context):
        '''
            this service work for bidirection face recognition        
        '''
        for message in request_iterator:
            nparr = utils.convert_and_save(message.message,'sushant')
            img = cv2.imdecode(nparr, flags=cv2.IMREAD_COLOR)


            #TODO: extract face encoding
            face_encodings =extractor(img)

            #TODO:get all encodings and labels from ETL.puller()
            k_encodings,k_names=ETL.loader()

            if len(k_encodings)>0:
                
                for face_encoding in face_encodings:
                    face_id=recognition(k_encodings,face_encoding,Sensitivity,k_names)
                
                            
            else:
                face_id="no face found"
            
        # extract name of faceid
           #data= #a.read_data(collection)
        # a.update(collection)
        # print(a.client)


            yield nparr #data
            
    # function to register 
    
    def GetRegisterFace(self, request, context):
        #pass
        print(request.uuid,request.image)
        img_arr=utils.convert_and_save(request.image,request.uuid)
        img = cv2.imdecode(img_arr, flags=cv2.IMREAD_COLOR)
        r1 = random.randint(0, 10)
        
            

        if recorder(img,request.uuid)==True:
            #save registerd encodings
            try:
                # ETL.save() # you can also put this to demon thread so it will do all its process in background
                print("saved")
                e,n=ETL.loader()
                #=ETL.puller()
                print("test {}".format(e))

            except:
                print("cant save")

        if os.path.exists(os.path.join(UPLOAD_PATH,request.uuid)):
            # path=os.path.join(Settings.BASE_DIRECTORY,UPLOAD_PATH,face_id)+'/'+str(r1)+".jpg
            cv2.imwrite(os.path.join(UPLOAD_PATH,request.uuid)+'/'+str(r1)+".jpg",img)
            try:
                data=[{'uuid':request.uuid,'image_url':os.path.join(UPLOAD_PATH,request.uuid)+'/'+str(r1)+".jpg"},

                        ]
            except:
                pass
        else:
            os.mkdir(os.path.join(UPLOAD_PATH,request.uuid))
            # path=os.path.join(Settings.BASE_DIRECTORY,UPLOAD_PATH,face_id))+'/'+str(r1)+".jpg"
            cv2.imwrite(str(os.path.join(UPLOAD_PATH,request.uuid))+'/'+str(r1)+".jpg",img)
            try:
                data=[{'uuid':request.uuid,'image_url':os.path.join(UPLOAD_PATH,request.uuid)+'/'+str(r1)+".jpg"},

                        ]
            except:
                pass

        #Todo register user in mongodb server
        
        a.insert_data(collection)
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