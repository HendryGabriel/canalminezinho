"""Transcreve um vídeo/áudio com faster-whisper (local, CPU). Uso: python transcrever.py video.mp4 > saida.txt"""
import sys
from faster_whisper import WhisperModel
m = WhisperModel('small', device='cpu', compute_type='int8')
segs, _ = m.transcribe(sys.argv[1], language='pt', vad_filter=True)
for s in segs: print(f'[{int(s.start)//60:02d}:{int(s.start)%60:02d}] {s.text.strip()}')
