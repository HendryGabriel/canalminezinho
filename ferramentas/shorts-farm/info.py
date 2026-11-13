"""Info das tomadas: v0 (pts do 1o quadro em epoch), a_off, duracao e eventos relativos.
uso: info.py <pasta_brutos> [<pasta2>...] -> grava <pasta>/info.json e imprime eventos"""
import sys, json, os, subprocess, glob

for pasta in sys.argv[1:]:
    info = {}
    for mkv in sorted(glob.glob(os.path.join(pasta, '*.mkv'))):
        base = mkv[:-4]; n = os.path.basename(base)
        p = subprocess.run(['ffprobe', '-v', 'error', '-select_streams', 'v', '-read_intervals', '%+#1', '-show_entries',
                            'packet=pts_time', '-of', 'csv=p=0', mkv], capture_output=True, text=True).stdout.split()
        v0 = float(p[0])
        js = json.load(open(base + '.json'))
        dur = float(subprocess.run(['ffprobe', '-v', 'error', '-show_entries', 'format=duration', '-of', 'csv=p=0', mkv],
                                   capture_output=True, text=True).stdout) - v0
        ev = [(e, round(t - v0, 2)) for e, t in json.load(open(base + '_events.json'))] if os.path.exists(base + '_events.json') else []
        info[n] = {'v0': v0, 'a_off': js['audio_start_epoch'] - v0, 'dur': round(dur, 2), 'ev': ev}
        print(n, round(dur, 1), [f'{e}@{t}' for e, t in ev][:40])
    json.dump(info, open(os.path.join(pasta, 'info.json'), 'w'), indent=1)
