from matplotlib import pyplot as plt;
import numpy as np;
import networkx as nx;
np.set_printoptions(precision=2);
import os
os.makedirs("out", exist_ok=True)
import scipy.io
from skimage import io
import cv2
#path, dirs, files = next(os.walk("video_frames"))
#file_count = len(files)

#img_query = io.imread('frame0.jpg', as_gray=True)
#X,Y = img_query.shape
def isoMapping(query_image_path):
    dir_frames = 'video_frames'
    filenames = []
    filesinfo = os.scandir(dir_frames)

    filenames = [f.path for f in filesinfo if f.name.endswith(".jpg")]
    filenames.sort(key=lambda f: int(''.join(filter(str.isdigit, f))))

    frameCount = len(filenames)
    frameHeight, frameWidth, frameChannels = cv2.imread(filenames[0]).shape
    frames = np.zeros((frameCount, frameHeight, frameWidth),dtype=np.float32)

    for idx, file_i in enumerate(filenames):
        frames[idx] = cv2.cvtColor(cv2.imread(file_i), cv2.COLOR_BGR2GRAY) / 255.0
        
    flat_frames = np.empty((frameCount,frames.shape[1]*frames.shape[2]))

    for i in range(frameCount):
        flat_frames[i] = frames[i,:,:].flatten()

    img_query = io.imread(query_image_path, as_gray=True)
    flat_frames = np.append(flat_frames,[img_query.flatten()],axis=0)


    ################# Distances    
    def l2_distance(x,y):
        return np.sqrt(np.sum((x-y)**2))


    def l1_distance(x,y):
        return np.sum(np.abs(x-y));

    def make_sim_graph(images, dist_func):
        num_img = len(images);
        

        G = np.zeros([num_img,num_img])
        for i in range(num_img):
            for j in range(i,num_img):
                G[i,j] = G[j,i] = dist_func(images[i], images[j])


        edge_threshold = 0;

        for i in range(num_img):
            weights = np.sort(G[i,:]);
            if len(weights) > 100:
                weights = weights[:100];

            min_threshold = weights[-1];
            edge_threshold = max(min_threshold, edge_threshold);

        for i in range(num_img):
            for j in range(i, num_img):
                if G[i,j] > edge_threshold:
                    G[i,j] = G[j,i] = 99999.0;
        
        return G

    G_l2 = make_sim_graph(flat_frames, l2_distance)
    #plt.figure()
    #plt.imshow(G_l2,cmap="gray")



    def Matrix_D(W): 
        n = np.shape(W)[0]
        Graph = nx.DiGraph()
        for i in range(n):
            for j in range(n):
                Graph.add_weighted_edges_from([(i,j,min(W[i,j], W[j,i]))])
    
        res = dict(nx.all_pairs_dijkstra_path_length(Graph))
        D = np.zeros([n,n])
        for i in range(n):
            for j in range(n):
                D[i,j] = res[i][j]
        
        return D

    def isomap(G):
        num_img = len(G);
        
        D = Matrix_D(G)
        #print('D:', D)

        D = (D + D.T)/2
        #print(np.max(D-D.T))
        
        ones = np.ones([num_img,1])
        H = np.eye(num_img) - 1/num_img*ones.dot(ones.T)
        C = -H.dot(D**2).dot(H)/(2*num_img)
        
        eig_val, eig_vec = np.linalg.eig(C)
        
        index = np.argsort(-eig_val) 
        #print(eig_val[index[0:2]])
        Z = eig_vec[:,index[0:2]].dot(np.diag(1/np.sqrt(eig_val[index[0:2]])))
        #print(np.shape(Z))
        
        return Z


    Z_l2 = isomap(G_l2)

    # plt.figure(figsize=(15,10))
    # plt.scatter(Z_l2[:,0], Z_l2[:,1], s = 10)
    # plt.title("l2 embedding")
    # plt.savefig('out/embedding_l2.png', dpi=600)

    def find_nearest(array, value):
        array = np.asarray(array)
        idx = np.empty(10)
        for i in range(len(idx)):
            idx[i] = (np.abs(array - value)).argmin()
            array[idx[i].astype(int)] = np.inf
        return idx

    idx = find_nearest(Z_l2[0:-1,0],Z_l2[-1,0])

    output = np.zeros((10,frameHeight, frameWidth, frameChannels))


    for j,i in enumerate(np.ndarray.tolist(idx.astype(int))):
        output[j,:,:,:] = cv2.imread(filenames[i])

    result = []
    for i in range(10):
        #plt.figure()
        #plt.imshow(output[i,:,:,:])
        filename = 'static/result/frame' + str(i) + '.png'
        cv2.imwrite(filename,output[i,:,:,:])
        #plt.savefig(filename)
        result.append(filename)
    print(result)
    return result
