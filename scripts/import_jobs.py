#!/usr/bin/env python3
"""Merge a reviewed JSON shortlist into the public feed without an API key.
Usage: python3 scripts/import_jobs.py path/to/reviewed.json
       python3 scripts/import_jobs.py --check
"""
import argparse, datetime as dt, hashlib, json, pathlib, urllib.parse
OUT=pathlib.Path(__file__).resolve().parents[1]/"public/data/jobs.json"
REQUIRED=("company","title","season","location","work_mode","apply_url","overview","why_fit","relevant_experiences","gaps","fit_score")
ENUM={"season":{"spring","summer","both"},"work_mode":{"remote","hybrid","onsite","unverified"},"status":{"active","unverified","closed"}}
def canonical(url):
 u=urllib.parse.urlsplit(url);return urllib.parse.urlunsplit((u.scheme.lower(),u.netloc.lower(),u.path.rstrip('/'),"",""))
def validate(job):
 for f in REQUIRED:
  if f not in job or job[f] is None or job[f]=="":raise ValueError("Missing "+f)
 for k,vals in ENUM.items():
  if k in job and job[k] not in vals:raise ValueError("Invalid "+k)
 p=urllib.parse.urlsplit(job["apply_url"])
 if p.scheme not in ("http","https") or not p.netloc:raise ValueError("Invalid application URL")
 if type(job["fit_score"]) not in (float,int) or not 0<=job["fit_score"]<=10:raise ValueError("Invalid score")
 if not isinstance(job["relevant_experiences"],list) or not isinstance(job["gaps"],list):raise ValueError("Invalid lists")
 for k in ("posted_at","first_seen_at","last_verified_at","start_date","end_date"):
  if job.get(k):
   dt.datetime.fromisoformat(job[k].replace("Z","+00:00"))
def main():
 p=argparse.ArgumentParser();p.add_argument("input",nargs="?");p.add_argument("--check",action="store_true");args=p.parse_args()
 feed=json.loads(OUT.read_text())
 if args.check:
  for j in feed["jobs"]:validate(j)
  print("Valid:",len(feed["jobs"]),"jobs");return
 if not args.input:p.error("Provide reviewed JSON for import")
 incoming=json.loads(pathlib.Path(args.input).read_text())
 incoming=incoming["jobs"] if isinstance(incoming,dict) else incoming
 if not isinstance(incoming,list):raise ValueError("Expected JSON jobs array")
 known={canonical(j["apply_url"]):j for j in feed["jobs"]}
 now=dt.datetime.now(dt.timezone.utc).isoformat(timespec="seconds")
 for raw in incoming:
  j=dict(raw);key=canonical(j["apply_url"]);prior=known.get(key)
  j["id"]=prior["id"] if prior else j.get("id",hashlib.sha256(key.encode()).hexdigest()[:16])
  j["first_seen_at"]=prior["first_seen_at"] if prior else now
  for k in ("posted_at","last_verified_at","start_date","end_date","compensation","hours"):j.setdefault(k,None)
  for k,v in (("eligibility","unverified"),("freshness","unverified"),("status","unverified"),("source","Unknown")):j.setdefault(k,v)
  validate(j);known[key]=j
 feed={"updated_at":now,"jobs":sorted(known.values(),key=lambda j:j["fit_score"],reverse=True)}
 OUT.write_text(json.dumps(feed,indent=2,ensure_ascii=False)+"\n")
 print("Imported",len(incoming),"jobs; total",len(known))
if __name__=="__main__":main()
