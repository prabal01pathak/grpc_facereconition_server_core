import os
import io
import pickle

class EtlLayer(object):
  def __init__ (self,dir_path='./encoding.pickle'):
    self.encodings=[]
    self.names=[]
    self.dir_path=dir_path

  def user_loader(self,openfile):
    try:
      user_data= pickle.load(openfile)
      return user_data
    except Exception as e:
      print("[001] problem in loading pickle  file {}".format(e))

  def reader(self):
    #load existing models
    # self.known_face_encodings = []
    # self.known_face_names  = []
    try:
      openfile=open(self.dir_path, "rb")
      
      while True:
        try:
          users_data = pickle.load(openfile)
          self.encodings = users_data["encodings"]
          self.names = users_data["names"]
          print("openfile")
          self.encodings,self.names
        except EOFError:
          break
    except Exception as e:
      print("No Known Encodings Found {}".format(e))
      
    return self.encodings,self.names


  def loader(self):
    '''
      this function returns encoding names lists of registered User
    '''
    self.encodings,self.names=self.reader()
    return self.encodings,self.names


  def pushers(self,encodings,names):
    '''
    this function takes parametr as enodings list and name
    And Return updated encodings and names
    '''
    #print("user encodings {}".format(encodings))
    #print("user names {}".format(names))
    for encoding in encodings:
      if len(encoding)>0:
        self.encodings.append(encoding)
        self.names.append(names)
    print("saving")
    if self.save(self.encodings,self.names) == True:
      print("saved _pusher func done")
      return True
    else:
      return False
    
  def puller(self):
    return self.encodings,self.names
  def save(self,encoding,name):
    '''
    this function write pickel file of each data
    '''
    
    reg_users_face_encodings = {"encodings": encoding, "names": name}
    #print(reg_users_face_encodings)
    try:
      f = open(self.dir_path, "wb")
    except Exception as e:
      print(" file open exception{}".format(e))
    try:
      print("writing")
      f.write(pickle.dumps(reg_users_face_encodings))
      f.close()
      print("saved")
      return True
    except:
      return False
    
   