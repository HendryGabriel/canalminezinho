import subprocess, numpy as np, sys
def med(p, ss, t=2):
    cmd=['ffmpeg','-v','error','-ss',str(ss),'-i',p,'-t',str(t),'-vf','setpts=PTS-STARTPTS,fps=60,scale=152:270,format=gray','-f','rawvideo','-']
    b=subprocess.run(cmd,capture_output=True).stdout
    f=np.frombuffer(b,np.uint8).reshape(-1,270,152).astype(float)
    d=np.array([np.abs(f[i+1]-f[i]).mean() for i in range(len(f)-1)])
    nz=d[d>0.3]
    return f'dup {np.mean(d<0.3):.2f}  cv {nz.std()/nz.mean():.2f}  media {nz.mean():.1f}'
for a in sys.argv[1:]:
    p,ss=a.split('@'); print(p, med(p,float(ss)))
