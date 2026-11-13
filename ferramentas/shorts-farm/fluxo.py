import subprocess, numpy as np, sys
def shifts(p, ss, t=2.5):
    cmd=['ffmpeg','-v','error','-ss',str(ss),'-i',p,'-t',str(t),'-vf','setpts=PTS-STARTPTS,fps=60,scale=256:456,format=gray','-f','rawvideo','-']
    f=np.frombuffer(subprocess.run(cmd,capture_output=True).stdout,np.uint8).reshape(-1,456,256).astype(float)
    win=np.outer(np.hanning(456),np.hanning(256))
    out=[]
    for i in range(len(f)-1):
        A=np.fft.fft2((f[i]-f[i].mean())*win); B=np.fft.fft2((f[i+1]-f[i+1].mean())*win)
        R=A*np.conj(B); R/=np.abs(R)+1e-9; r=np.fft.ifft2(R).real
        y,x=np.unravel_index(r.argmax(),r.shape)
        if x>128: x-=256
        if y>228: y-=456
        out.append((x,y))
    return np.array(out)
for a in sys.argv[1:]:
    p,ss=a.split('@'); s=shifts(p,float(ss)); m=np.hypot(s[:,0],s[:,1])
    d=np.abs(np.diff(m))
    print(p, 'mov medio %.2f px/q  jerk medio %.2f  zeros %.2f' % (m.mean(), d.mean(), np.mean(m==0)))
    print('   ', ' '.join(str(int(round(v))) for v in m[:60]))
