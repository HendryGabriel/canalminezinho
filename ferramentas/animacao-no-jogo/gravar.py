"""Grava a janela do Minecraft (gfxcapture) + audio so do processo javaw (process loopback).
uso: gravar.py <saida_sem_ext> [max_seg]
Para parar: criar o arquivo <saida_sem_ext>.stop
Gera: <saida>.mkv (pts = relogio de parede em us), <saida>.wav, <saida>.json (inicio do audio em epoch)."""
import sys, os, time, json, subprocess, wave, threading
import numpy as np
import flexaudio

base = sys.argv[1]; maxs = float(sys.argv[2]) if len(sys.argv) > 2 else 600
stop = base + '.stop'
if os.path.exists(stop): os.remove(stop)
pid = next(p.pid for p in flexaudio.processes() if p.name.lower().startswith('javaw'))

vf = ("gfxcapture=window_exe=javaw.exe:capture_cursor=0:max_framerate=60,hwdownload,format=bgra,"
      "setpts=RTCTIME/(TB*1000000)")
ff = subprocess.Popen(['ffmpeg', '-hide_banner', '-loglevel', 'error', '-y', '-filter_complex', vf,
                       '-fps_mode', 'passthrough', '-c:v', 'h264_nvenc', '-preset', 'p6', '-tune', 'hq', '-rc', 'vbr', '-cq', '16',
                       '-pix_fmt', 'yuv420p', '-enc_time_base', '1/1000000', base + '.mkv'], stdin=subprocess.PIPE)

s = flexaudio.open('process', process_id=pid, output_rate=48000, output_channels=2)
w = wave.open(base + '.wav', 'wb'); w.setnchannels(2); w.setsampwidth(2); w.setframerate(48000)
t_first = None; nframes = 0; t0 = time.time()
while time.time() - t0 < maxs and not os.path.exists(stop):
    c = s.poll_chunk()
    if c is None:
        time.sleep(0.005); continue
    if t_first is None:
        t_first = time.time() - c.frames / 48000.0
    a = np.frombuffer(c.data, dtype=np.float32) if isinstance(c.data, (bytes, bytearray)) else np.asarray(c.data, dtype=np.float32)
    w.writeframes((np.clip(a, -1, 1) * 32767).astype('<i2').tobytes()); nframes += c.frames
s.stop(); w.close()
ff.stdin.write(b'q'); ff.stdin.flush()
try:
    ff.wait(15)
except Exception:
    ff.kill()
json.dump({'audio_start_epoch': t_first, 'audio_frames': nframes, 'pid': pid, 't0': t0, 't_end': time.time()}, open(base + '.json', 'w'))
print('GRAVADO', base, nframes / 48000.0)
