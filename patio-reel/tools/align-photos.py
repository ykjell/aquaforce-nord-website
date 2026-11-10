# Richtet das Nachher-Foto per SIFT-Homographie deckungsgleich auf das Vorher-Foto aus und
# schneidet beide auf den gemeinsamen 9:16-Bereich (1080x1920) zu -> assets/photos/.
#   pip install opencv-python-headless numpy
#   python3 tools/align-photos.py vorher.jpg nachher.jpg /tmp/debug assets/photos
import cv2, numpy as np, sys
out=sys.argv[3]
B=cv2.imread(sys.argv[1]); A=cv2.imread(sys.argv[2])
sift=cv2.SIFT_create(8000)
gb=cv2.cvtColor(B,cv2.COLOR_BGR2GRAY); ga=cv2.cvtColor(A,cv2.COLOR_BGR2GRAY)
kb,db=sift.detectAndCompute(gb,None); ka,da=sift.detectAndCompute(ga,None)
m=cv2.BFMatcher().knnMatch(da,db,k=2)
good=[x for x,y in m if x.distance<0.72*y.distance]
pa=np.float32([ka[g.queryIdx].pt for g in good]); pb=np.float32([kb[g.trainIdx].pt for g in good])
H,mask=cv2.findHomography(pa,pb,cv2.RANSAC,4.0)
print(len(good), int(mask.sum())); print(H)
W=cv2.warpPerspective(A,H,(B.shape[1],B.shape[0]))
cv2.imwrite(out+'/after_warp.jpg',W)
blend=cv2.addWeighted(B,0.5,W,0.5,0); cv2.imwrite(out+'/blend.jpg',cv2.resize(blend,None,fx=0.5,fy=0.5))
inl=pb[mask.ravel()==1]; print('inlier y range',inl[:,1].min(),inl[:,1].max(),'x',inl[:,0].min(),inl[:,0].max())
mask=cv2.warpPerspective(np.full(A.shape[:2],255,np.uint8),H,(B.shape[1],B.shape[0]))
ys,xs=np.where(mask==255)
# find largest 9:16 box: scan
best=None
Hh,Ww=mask.shape
ii=(mask==255).astype(np.int32).cumsum(0).cumsum(1)
def full(x0,y0,w,h):
    x1,y1=x0+w-1,y0+h-1
    s=ii[y1,x1]-(ii[y0-1,x1] if y0>0 else 0)-(ii[y1,x0-1] if x0>0 else 0)+(ii[y0-1,x0-1] if x0>0 and y0>0 else 0)
    return s==w*h
for w in range(Ww,400,-4):
    h=int(round(w*16/9))
    if h>Hh: continue
    found=None
    for y0 in range(0,Hh-h+1,4):
        for x0 in range(0,Ww-w+1,4):
            if full(x0,y0,w,h): found=(x0,y0); break
        if found: break
    if found: best=(found[0],found[1],w,h); break
print('crop',best)
x0,y0,w,h=best
for img,name in [(B,'vorher'),(W,'nachher')]:
    c=cv2.resize(img[y0:y0+h,x0:x0+w],(1080,1920),interpolation=cv2.INTER_LANCZOS4)
    cv2.imwrite(sys.argv[4]+f'/{name}.jpg',c,[cv2.IMWRITE_JPEG_QUALITY,92])
