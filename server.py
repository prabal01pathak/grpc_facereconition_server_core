from concurrent import futures

from google.protobuf import message

import grpc
import bidirectional_pb2_grpc as bidirectional_pb2_grpc
import bidirectional_pb2 as pb2
import utils
from Settings import *

class BidirectionalService(bidirectional_pb2_grpc.BidirectionalServicer):
    
    def GetServerResponse(self, request_iterator, context):
        '''
            this service work for bidirection face recognition        
        '''
        for message in request_iterator:
            nparr = utils.convert_and_save(message.message,'sushant')

            



            yield nparr
            
    # function to register 
    
    def GetRegisterFace(self, request, context):
        #pass
        print(request.uuid,request.image)
        

            

        #Todo apply etl pipeliner

        #etl.save to save data

        #Todo register user in mongodb server

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