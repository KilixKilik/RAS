import os
import shutil
import hashlib
import tarfile

# init: папка вывода
os.makedirs("ras", exist_ok=True)

# ign: игнор-списки
igd = {"__pycache__", "ras", "GameAssets", "Assets"}
igf = {"script.py"}
igx = {".log", ".tmp"}  # new: игнор по расширению

# rmj: чистка мусора
def rmj(r, n):
    for a, b, _ in os.walk(r, topdown=False):
        for d in b:
            if d in n:
                p = os.path.join(a, d)
                print(f"del: {p}")
                shutil.rmtree(p)

rmj(".", {"obj", "bin"})

# hx: короткий хеш
def hx(f):
    h = hashlib.sha256()
    try:
        with open(f, "rb") as ff:
            h.update(ff.read())
        return h.hexdigest()[:8]
    except:
        return "FAIL"

# root: обработка корня
with open("ras/Корневая.txt", "w", encoding="utf-8") as k:
    for i in os.listdir("."):
        if os.path.isfile(i) and i not in igf and not i.endswith(tuple(igx)):
            k.write(f"ПАПКА: .\n")
            k.write(f"--------Файл: {i}\n")
            k.write(f"ХЭШ: {hx(os.path.join('.', i))}\n")  # fix: полный путь
            try:
                with open(i, "r", encoding="utf-8") as f:
                    k.write(f.read())
            except:
                k.write("[BIN]")
            k.write("\n\n")

# scan: обработка подпапок
for i in os.listdir("."):
    if os.path.isdir(i) and i not in igd:
        o = f"ras/{i}.txt"
        with open(o, "w", encoding="utf-8") as f:
            f.write(f"ПАПКА: {i}\n")
            for dp, dn, fl in os.walk(i):
                dn[:] = [d for d in dn if d not in igd]
                for fi in fl:
                    if fi.endswith(tuple(igx)):
                        continue
                    p = os.path.join(dp, fi)
                    rp = os.path.relpath(p, i)
                    f.write(f"--------Файл: {rp}\n")
                    f.write(f"ХЭШ: {hx(p)}\n")
                    try:
                        with open(p, "r", encoding="utf-8") as inf:
                            f.write(inf.read())
                    except:
                        f.write("[BIN]")
                    f.write("\n\n")

# arch: архивация результата
shutil.make_archive("ras_archive", "tar", "ras")
print("Архив ras_archive.tar готов")

# github: KilixKilik