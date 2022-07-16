from functools import reduce
from math import floor
from skimage import color
from skimage import io

BRIGHTNESS_LOWER_THRESHOLD=0.09
BRIGHTNESS_TOLERANCE=0.02
NEIGBORHOOD_STEPS=9
IMAGE_PATH='sample.png'


def flood_search(i,j,v):
    chain = set()
    bigger = flood_search_impl(i,j,v,chain)
    for (xi,xj) in chain:
        img[xi,xj] = v + eps
    return None if bigger else chain

def flood_search_impl(i,j,v,chain:set):
    bigger=False
    scanned = set()
    to_scan = set()
    to_scan.add( (i,j) )
    while (len(to_scan) > 0):
        
        (ii,jj) = to_scan.pop()
        t = (ii,jj)

        scanned.add(t)

        dv = img[ii,jj]
        if dv < v - eps: continue
        if dv > v: 
            bigger = True
            continue

        chain.add( t )

        for di in range(max(ii-NEIGBORHOOD_STEPS,0),min(ii+NEIGBORHOOD_STEPS+1,h)):
            for dj in range(max(jj-NEIGBORHOOD_STEPS,0),min(jj+NEIGBORHOOD_STEPS+1,w)):
                t = (di, dj)
                if t in scanned: continue
                if t in to_scan: continue

                to_scan.add ( t )
    
    return bigger

            


# source = io.imread('sample.png')
source = io.imread(IMAGE_PATH)
source = source[:,:,:3]
img = color.rgb2gray(source)

h,w = img.shape
mx = img.max()
mn = img.min()
eps = (mx - mn) * BRIGHTNESS_TOLERANCE
threshold = (mx - mn) * BRIGHTNESS_LOWER_THRESHOLD + mn


visible_target = [(i,j,img[i,j]) for i in range(h) for j in range(w) if img[i,j] > threshold]
pixels = sorted(visible_target, key=lambda kv:kv[2], reverse=True)




seeds = [] # list of [(i,j),v], center of each object, and the brightness

for (i,j,v) in pixels:
    if img[i,j] > v: continue # prevoiusly processed
    area = flood_search(i,j,v)
    if area is not None:
        #cacluate center of area (sum / len)
        scenter=reduce(lambda s,p:(s[0]+p[0],s[1]+p[1]),area,(0,0))
        center = (floor(scenter[0] / len(area)), floor(scenter[1] / len(area)))
        seeds.append([center,v])


# show the result
print(f"number of seeds: {len(seeds)}")

with open('result.csv','w') as f:
    f.write('id,i,j,v\r\n')
    ID = 0
    for [(i,j),v] in seeds:
        ID += 1
        f.write(f"{ID},{i},{j},{v}\r\n")

for [(i,j),v] in seeds:
    
    for y in range(max(i-4,0),min(i+5,h)):
        for x in range(max(j-4,0),min(j+5,w)):
            if y == i and x == j or y - i == x - j or y - i == j - x:
                source[y,x] = [255,217,5]
            else:
                source[y,x] = [40,30,0]

io.imsave("output.png",source)

