from __future__ import print_function


import grpc
import bidirectional_pb2_grpc as bidirectional_pb2_grpc
import bidirectional_pb2 as bidirectional_pb2
import bidirectional_pb2 as pb2

import base64
import time

# fake_data = Faker()
uuid = "sushant123"

with open("./images/sushant.jpeg", "rb") as f:
    im_b64 = base64.b64encode(
        f.read()
    )  # Encode the picture into stream data, put it in the memory cache, and then convert it into string format

# p=os.path.join(Settings.BASE_DIRECTORY,Settings.UPLOAD_PATH,'pawan')
# print(p)


def registering_data(uuid, im_b64):
    return bidirectional_pb2.RegisterMessage(uuid=uuid, image=im_b64)


def make_data(im_b64):
    return bidirectional_pb2.Message(
        # message=fake_data
        message=im_b64
    )


# print (fake_data.name())
def generate_messages():
    for _ in range(0, 10):

        messages = [
            make_data(im_b64),
        ]
        for msg in messages:
            print("Hello Server Sending you the %s" % msg.message)
            yield msg


def register_data():
    # for _ in range(0,1):

    registering = [
        # registering_data(uuid='sushant123',message = im_b64)
        registering_data(uuid, im_b64)
    ]
    for reg in registering:

        # yield reg
        # print(reg)
        return reg


def send_message(stub):

    startTime = time.time()
    responses2 = stub.GetRegisterFace(register_data())

    # responses = stub.GetServerResponse(generate_messages())
    """
    try:
        
        responses2 = stub.GetRegisterFace(register_data())
        print(responses2)
        for response in responses2:
           print("Hello from the server received your %s" % response.message)
    except Exception as E:
        print(E)
        
    #for response in responses:
      # print("Hello from the server received your %s" % response.message)
       """
    endTime = time.time()
    print(str(endTime - startTime))


def registration(stub):
    pass
    response = stub.GetRegisterFace(pb2.RegisterMessage(uuid=uuid, image=im_b64))
    print(response.uuid)


def run():
    with grpc.insecure_channel(
        "localhost:50052", options=(("grpc.enable_http_proxy", 0),)
    ) as channel:
        stub = bidirectional_pb2_grpc.FaceRegistrationStub(channel)
        send_message(stub)
        registration(stub)


if __name__ == "__main__":
    run()
