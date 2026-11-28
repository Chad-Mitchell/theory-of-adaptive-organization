# Load CGM series into a common long format: subject, cohort, t_min (minutes), glucose (mg/dL), dt (sampling min)
import pandas as pd, numpy as np, glob, zipfile, os, re
OUT="data/series.parquet"
def replacebg():
    z=zipfile.ZipFile("data/replacebg.zip")
    it=pd.read_csv(z.open("Data Tables/HDeviceCGM.txt"),sep="|",usecols=["PtID","DeviceDtTmDaysFromEnroll","DeviceTm","RecordType","GlucoseValue"],chunksize=2_000_000)
    parts=[]
    for c in it:
        c=c[c.RecordType=="CGM"]
        tm=pd.to_timedelta(c.DeviceTm).dt.total_seconds()/60
        c=pd.DataFrame(dict(subject="RBG"+c.PtID.astype(str),t_min=c.DeviceDtTmDaysFromEnroll*1440+tm,glucose=c.GlucoseValue.astype(float)))
        parts.append(c)
    d=pd.concat(parts); d["cohort"]="REPLACEBG_T1D"; d["dt"]=5.0
    return d
def shanghai():
    parts=[]
    for f in sorted(glob.glob("data/shanghai/diabetes datasets/Shanghai_T*/*.xls*")):
        b=os.path.basename(f); pid,per=b.split("_")[0],b.split("_")[1]
        cohort="SH_T1DM" if "T1DM" in f else "SH_T2DM"
        x=pd.read_excel(f); col=[c for c in x.columns if str(c).startswith("CGM")][0]
        x=x[["Date",col]].dropna(); t=pd.to_datetime(x.Date)
        parts.append(pd.DataFrame(dict(subject=f"SH{pid}_{per}",cohort=cohort,t_min=(t-t.min()).dt.total_seconds()/60,glucose=x[col].astype(float).values,dt=15.0)))
    return pd.concat(parts)
def colas():
    parts=[]
    for f in sorted(glob.glob("data/colas/S1/case*.csv")):
        n=re.findall(r"\d+",os.path.basename(f))[0]
        x=pd.read_csv(f); s=pd.to_timedelta(x.hora).dt.total_seconds()/60
        # times-of-day only; unwrap midnight crossings
        s=s.values.copy(); add=0
        for i in range(1,len(s)):
            if s[i]+add<s[i-1]-1: add+=1440
            s[i]+=add
        parts.append(pd.DataFrame(dict(subject=f"CO{n}",cohort="COLAS",t_min=s,glucose=x.glucemia.astype(float),dt=5.0)))
    return pd.concat(parts)
if __name__=="__main__":
    d=pd.concat([replacebg(),shanghai(),colas()],ignore_index=True)
    d=d.sort_values(["subject","t_min"]).drop_duplicates(["subject","t_min"])
    d.to_parquet(OUT)
    g=d.groupby(["cohort","subject"]).agg(n=("glucose","size"),span_d=("t_min",lambda x:(x.max()-x.min())/1440))
    print(g.groupby("cohort").agg(subjects=("n","size"),med_n=("n","median"),med_days=("span_d","median")))
