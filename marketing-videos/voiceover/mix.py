#!/usr/bin/env python3
"""Legt die Sprachaufnahmen auf die Schnitte der Reels und mischt den Ton.

    python3 voiceover/mix.py [1 2 3 4 5]      -> renders/mit-ton/0X-….mp4

Pro Video: Sprechabschnitte (Quelle von–bis in der Aufnahme) und ihre Startzeit im Video.
Die Abschnitte stammen aus der Pausen-Erkennung (ffmpeg silencedetect), nicht aus einem Transkript.
Stimmkette: Hochpass, leichte Rauschminderung, Entmulmen, Präsenz, Luft, De-Esser, Kompression, -15 LUFS.
Unter Reinigungsszenen liegt leise der Originalton der Lanze (bed).
"""
import subprocess, sys, os

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ORIG = os.environ.get("AQ_ORIG", "/root/.claude/uploads/33c4c146-e853-5f9a-89f1-f559a708b6be")
POV_SUN = f"{ORIG}/b1e16e6c-VIDEO-2026-11-12-14-57-46.mp4"   # Lanze, trocken
POV_WET = f"{ORIG}/d253a0a4-VIDEO-2026-11-12-14-57-46.mp4"   # Lanze, nass

CHAIN = ("highpass=f=85,afftdn=nr=10:nf=-50,equalizer=f=260:t=q:w=1.1:g=-2.5,"
         "equalizer=f=3800:t=q:w=1.4:g=2.5,highshelf=f=9500:g=2,deesser=i=0.35,"
         "acompressor=threshold=-22dB:ratio=3.2:attack=8:release=140:makeup=2")

# name, Gesamtlänge, [(quelle_von, quelle_bis, start_im_video)], [(bed_datei, quelle_ab, video_von, video_bis)]
V = {
    1: ("01-die-linie", 22.6, [
        (3.147, 6.396, 0.20), (6.701, 8.485, 3.70), (8.996, 11.073, 5.75), (11.713, 14.693, 8.05),
        (15.291, 17.993, 11.35), (18.237, 19.303, 14.20), (19.496, 20.560, 15.35), (21.619, 27.307, 16.60),
    ], [(POV_SUN, 1.0, 0.0, 11.4)]),
    2: ("02-vorher-nachher", 18.4, [
        (0.768, 5.221, 0.20), (5.484, 8.963, 4.85), (9.548, 12.523, 8.60), (12.799, 15.000, 11.75),
        (15.630, 19.474, 14.15),
    ], []),
    3: ("03-der-rundgang", 19.4, [
        (0.612, 3.072, 0.20), (3.630, 4.959, 2.90), (5.201, 6.072, 4.40), (6.885, 8.816, 5.50),
        (9.146, 11.014, 7.55), (11.497, 13.859, 9.50), (14.272, 16.672, 12.00), (17.162, 21.525, 14.55),
    ], []),
    4: ("04-markenfilm", 17.2, [
        (3.621, 6.168, 0.30), (6.658, 11.023, 3.40), (11.353, 12.329, 8.00), (12.798, 15.228, 9.60),
        (16.096, 19.649, 12.90),
    ], [(POV_SUN, 3.0, 3.3, 6.4)]),
    5: ("05-drei-zeichen", 23.2, [
        (0.863, 3.303, 0.20), (3.707, 4.347, 3.40), (4.603, 6.881, 4.20), (7.584, 8.298, 7.00),
        (8.716, 11.544, 7.85), (12.149, 15.335, 10.95), (16.169, 16.795, 14.50), (17.002, 20.422, 15.30),
        (21.204, 25.035, 18.90),
    ], [(POV_WET, 4.0, 14.3, 16.6)]),
}


def build(n):
    name, total, segs, beds = V[n]
    src = f"{ROOT}/voiceover/audio/audio_{n}.m4a"
    f = [f"[0:a]aresample=48000,{CHAIN},asplit={len(segs)}" + "".join(f"[c{i}]" for i in range(len(segs)))]
    lab = []
    for i, (a, b, s) in enumerate(segs):
        a2, b2 = max(0, a - 0.06), b + 0.14
        d = b2 - a2
        f.append(f"[c{i}]atrim={a2:.3f}:{b2:.3f},asetpts=PTS-STARTPTS,afade=t=in:d=0.03,"
                 f"afade=t=out:st={d - 0.1:.3f}:d=0.1,adelay={max(0, int((s - 0.06) * 1000))}:all=1[s{i}]")
        lab.append(f"[s{i}]")
    f.append("".join(lab) + f"amix=inputs={len(segs)}:normalize=0,loudnorm=I=-15:TP=-1.5:LRA=9,apad=whole_dur={total}[vo]")
    ins = ["-i", src]
    mix = ["[vo]"]
    for j, (bf, ss, v0, v1) in enumerate(beds):
        d = v1 - v0
        ins += ["-ss", str(ss), "-t", str(d), "-i", bf]
        f.append(f"[{j + 1}:a]aresample=48000,highpass=f=150,lowpass=f=9000,volume=-17dB,afade=t=in:d=0.3,"
                 f"afade=t=out:st={d - min(1.4, d / 2):.2f}:d={min(1.4, d / 2):.2f},adelay={int(v0 * 1000)}:all=1,apad=whole_dur={total}[b{j}]")
        mix.append(f"[b{j}]")
    f.append("".join(mix) + f"amix=inputs={len(mix)}:normalize=0,alimiter=limit=0.84,volume=-1.8dB,atrim=0:{total}[a]")
    vid = f"{ROOT}/renders/{name}.mp4"
    out = f"{ROOT}/renders/mit-ton/{name}.mp4"
    os.makedirs(os.path.dirname(out), exist_ok=True)
    vdur = float(subprocess.check_output(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", vid]))
    pad = max(0.0, total - vdur)
    f.append(f"[{len(beds) + 1}:v]tpad=stop_mode=clone:stop_duration={pad + 0.1:.2f}[v]")
    cmd = ["ffmpeg", "-v", "error", "-y", *ins, "-i", vid, "-filter_complex", ";".join(f), "-map", "[v]", "-map", "[a]",
           "-c:v", "libx264", "-preset", "medium", "-crf", "20", "-pix_fmt", "yuv420p", "-c:a", "aac", "-b:a", "192k",
           "-ac", "2", "-movflags", "+faststart", "-t", str(total), out]
    subprocess.check_call(cmd)
    print("ok", out, f"video {vdur:.1f}s -> {total}s")


for n in [int(x) for x in sys.argv[1:]] or [1, 2, 3, 4, 5]:
    build(n)
