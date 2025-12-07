import os, shutil, hashlib

igd = {'__pycache__', 'ras', 'GameAssets', 'Assets', 'obj', 'bin'}
igf = {'script.py'}
igx = {'.log', '.tmp'}

def hx(p):
    try:
        with open(p, 'rb') as f: return hashlib.sha256(f.read()).hexdigest()[:8]
    except: return 'FAIL'

os.makedirs('ras', exist_ok=1)

# root files
with open('ras/root.txt', 'w', encoding='utf-8') as out:
    for f in os.listdir('.'):
        if os.path.isfile(f) and f not in igf and not f.endswith(tuple(igx)):
            out.write(f'F: {f}\nH: {hx(f)}\n')
            try: out.write(open(f, encoding='utf-8').read())
            except: out.write('[BIN]')
            out.write('\n\n')

# dirs
for d in os.listdir('.'):
    if os.path.isdir(d) and d not in igd:
        with open(f'ras/{d}.txt', 'w', encoding='utf-8') as out:
            out.write(f'D: {d}\n')
            for dp, dn, fl in os.walk(d):
                dn[:] = [x for x in dn if x not in igd]
                for f in fl:
                    if f.endswith(tuple(igx)): continue
                    p = os.path.join(dp, f)
                    rp = os.path.relpath(p, d)
                    out.write(f'F: {rp}\nH: {hx(p)}\n')
                    try: out.write(open(p, encoding='utf-8').read())
                    except: out.write('[BIN]')
                    out.write('\n\n')

shutil.make_archive('archive', 'tar', 'ras')
print('done')

# github: kilixkilik
