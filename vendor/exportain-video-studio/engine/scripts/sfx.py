#!/usr/bin/env python3
"""plan.json -> sfx.wav : motion-graphics sound design synced to the timeline.
All sounds are synthesised with ffmpeg (no downloads):
  whoosh  - every scene circle-wipe (peaks as the wipe lands)
  pop     - icon card pops in
  tick    - each keyword chip lands
  boom    - logo intro + end-card burst (sub impact + noise hit)
  riser   - 1.6 s build into the end card
  chime   - bright shimmer as the URL appears
Timings mirror timeline.html (scene 0 starts at max(start, 1.0), wipe .65 s,
chips at +0.7 s + 0.12 s each)."""
import argparse, json, os, subprocess, tempfile, re

SR = 48000
SOUNDS = {
    "whoosh": ("anoisesrc=d=0.75:c=pink:a=0.9:r=48000,highpass=f=350,lowpass=f=6000,"
               "volume='pow(sin(PI*t/0.75),3)':eval=frame,aphaser=in_gain=0.6:out_gain=0.9:speed=1.6:decay=0.5,"
               "apulsator=hz=1.3:amount=0.6"),
    "pop": "aevalsrc='0.9*sin(2*PI*(230+950*exp(-t*38))*t)*exp(-t*16)':d=0.3:s=48000",
    "tick": "aevalsrc='0.55*sin(2*PI*2300*t)*exp(-t*70)+0.3*sin(2*PI*3450*t)*exp(-t*90)':d=0.09:s=48000",
    "boom": ("aevalsrc='0.95*sin(2*PI*(42+90*exp(-t*9))*t)*exp(-t*3.2)+0.35*(random(0)*2-1)*exp(-t*14)':d=1.6:s=48000,"
             "lowpass=f=2500,aecho=0.8:0.6:60|130:0.25|0.15"),
    "riser": ("aevalsrc='(0.32*sin(2*PI*(180*t+117*t*t*t))+0.18*(random(0)*2-1))*pow(t/1.6,2.2)':d=1.6:s=48000,"
              "highpass=f=200,aecho=0.8:0.7:90|170:0.3|0.2"),
    "chime": ("aevalsrc='(0.35*sin(2*PI*1318.5*t)+0.28*sin(2*PI*1975.5*t)+0.2*sin(2*PI*2637*t))*exp(-t*2.6)':d=1.8:s=48000,"
              "aecho=0.8:0.7:110|230:0.35|0.25"),
}
SOUNDS.update({
    "bubble": "aevalsrc='0.8*sin(2*PI*(400+1400*t*4)*t)*exp(-t*22)':d=0.22:s=48000",
    "pop2": "aevalsrc='0.9*sin(2*PI*(520+700*exp(-t*45))*t)*exp(-t*20)':d=0.22:s=48000",
    "click": "aevalsrc='0.7*sin(2*PI*1800*t)*exp(-t*120)+0.4*(random(0)*2-1)*exp(-t*200)':d=0.06:s=48000",
    "ding": ("aevalsrc='(0.5*sin(2*PI*1568*t)+0.25*sin(2*PI*3136*t))*exp(-t*4)':d=1.0:s=48000,"
             "aecho=0.8:0.6:90:0.25"),
    "sparkle": ("aevalsrc='0.25*(sin(2*PI*2093*t)*exp(-t*9)+sin(2*PI*2637*(t-0.06))*exp(-(t-0.06)*9)*gte(t,0.06)"
                "+sin(2*PI*3136*(t-0.12))*exp(-(t-0.12)*9)*gte(t,0.12))':d=0.8:s=48000,aecho=0.8:0.6:70|140:0.3|0.2"),
    "shutter": "aevalsrc='0.8*(random(0)*2-1)*(exp(-t*80)+0.7*exp(-(t-0.07)*90)*gte(t,0.07))':d=0.2:s=48000,highpass=f=900",
    "swoosh": ("anoisesrc=d=0.45:c=pink:a=0.9:r=48000,highpass=f=900,lowpass=f=7000,"
               "volume='pow(sin(PI*t/0.45),2)':eval=frame"),
    "rise": ("aevalsrc='0.35*sin(2*PI*(300*t+700*t*t))*pow(t/0.7,1.5)':d=0.7:s=48000,aecho=0.8:0.6:60:0.25"),
})
GAIN = {"whoosh": -6, "pop": -8, "tick": -14, "boom": -3, "riser": -8, "chime": -10,
        "bubble": -10, "pop2": -9, "click": -10, "ding": -11, "sparkle": -9, "shutter": -8, "swoosh": -10, "rise": -10}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--plan", required=True); ap.add_argument("--out", required=True)
    a = ap.parse_args()
    plan = json.load(open(a.plan, encoding="utf-8"))
    V, T = plan["voice_duration"], plan["total"]
    work = tempfile.mkdtemp(prefix="sfx_")
    for name, src in SOUNDS.items():
        subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-f", "lavfi", "-i", src, "-ac", "2", "-ar", str(SR),
                        "-af", f"volume={GAIN[name]}dB", f"{work}/{name}.wav"], check=True)

    ev = [("whoosh", 0.0), ("boom", 0.08)] if plan.get("intro", True) else []
    for i, sc in enumerate(plan["scenes"]):
        st = max(sc["start"], 1.0) if (i == 0 and plan.get("intro", True)) else sc["start"]
        ev += [("whoosh", max(0, st - 0.12))]
        if sc.get("kind") == "logo_reveal":
            ev += [("boom", st + 0.25), ("chime", st + 0.9)]
        elif "beats" in sc:
            names = sc.get("sfx") or ["pop"]
            ev += [(names[j % len(names)], bt + 0.03) for j, bt in enumerate(sc["beats"])]
        else:
            ev += [("pop", st + 0.14)]
            chips = len({re.sub(r"[,।?!.:;—\-]+$", "", w) for w in sc.get("emphasis", [])})
            ev += [("tick", st + 0.72 + k * 0.12) for k in range(min(chips, 3))]
    if plan.get("endcard", 0) > 0:
        ev += [("riser", max(0, V - 1.6)), ("whoosh", V - 0.1), ("boom", V + 0.15), ("chime", V + 0.7)]

    cmd = ["ffmpeg", "-y", "-loglevel", "error"]
    for name, _ in ev: cmd += ["-i", f"{work}/{name}.wav"]
    fc = "".join(f"[{k}:a]adelay={int(t*1000)}|{int(t*1000)}[e{k}];" for k, (_, t) in enumerate(ev))
    fc += "".join(f"[e{k}]" for k in range(len(ev))) + f"amix=inputs={len(ev)}:normalize=0:duration=longest,apad=whole_dur={T},atrim=0:{T}[out]"
    cmd += ["-filter_complex", fc, "-map", "[out]", "-ar", str(SR), a.out]
    subprocess.run(cmd, check=True)
    print(f"{len(ev)} sfx events -> {a.out}")


if __name__ == "__main__":
    main()
