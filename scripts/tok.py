import base64, json, time
for p in [r"E:\ai_project\NISAR\earthdata.txt", r"E:\ai_project\30days_challenge\day5_views\токен.txt"]:
    try:
        t=open(p,encoding="utf-8").read().strip()
        payload=t.split(".")[1]; payload+="="*(-len(payload)%4)
        d=json.loads(base64.urlsafe_b64decode(payload))
        print(p, d.get("uid"), "iat", time.strftime("%Y-%m-%d", time.gmtime(d["iat"])), "exp", time.strftime("%Y-%m-%d", time.gmtime(d["exp"])), "now", time.strftime("%Y-%m-%d"))
    except Exception as e: print(p, e)