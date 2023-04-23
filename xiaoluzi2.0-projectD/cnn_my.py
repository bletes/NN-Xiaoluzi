


from keras.models import load_model
import numpy as np
from sklearn.preprocessing import MinMaxScaler
import time
import numpy as np
#t2=time.time()
model=load_model(r"C:\Users\admin\Desktop\xiaoluzi2.0-projectD\cnn\TABPAB10-03-28-04-20-2023-7.h5")

scaler = MinMaxScaler(feature_range=(0, 1))
##tsA=250
##tsB=250
##tdd=[[175.9,
##              227,
##              0.02839,
##              33.48],
##              [176,
##              227.1,
##              0.02836,
##              33.49]]
def ou(tsA,tsB,tdd,lenth=10):
       #t2=time.time()
       nd=[]#new data
       for i in tdd[-(lenth//4):]:
              for j in i:
                     nd.append(j)
       nd.append(tsA)
       nd.append(tsB)
##       aa=scaler.fit_transform(np.array([[-2.136852],[368.620882],[175.9],
##              [227],
##              [0.02839],
##              [33.48],
##              [176],
##              [227.1],
##              [0.02836],
##              [33.49],[17],[22.1],
##                                         ]))
      # t3=time.time()
       tt1=[]
       for i in range(lenth):
              tt1.append([nd[i]])
              
       aa=scaler.fit_transform(np.array([[-2.136852],[368.620882]]+tt1))
       cc=np.reshape(aa[2:], (aa[2:].shape[1], aa[2:].shape[0], 1))
       bb=model(cc)
       print(bb)
       #print(time.time()-t3)
       print((scaler.inverse_transform(np.concatenate([np.array([[bb[0][0]],[bb[0][1]]]),aa])))[-6:])
       o1,o2=(scaler.inverse_transform(np.concatenate([np.array([[bb[0][0]],[bb[0][1]]]),aa])))[0:2]
       #print(time.time()-t2)
       o1,o2=float(o1),float(o2)
       o1t,o2t=o1,o2
       if o1t<0:
              pass
##              o1=(o1t+o2t)*0.2
##              o2=(o1t+o2t)*0.8
       if o2t<0:
              pass
##              o1=(o1t+o2t)*0.8
##              o2=(o1t+o2t)*0.2
       print('solution:',o1t,o2t,'fix:',o1,o2)
       return float(o1),float(o2)
##o1,o2=ou(250,250,[[175.9,
##              227,
##              0.02839,
##              33.48],
##              [176,
##              227.1,
##              0.02836,
##              33.49]])


