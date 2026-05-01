"""
Intune Dashboard — Flask Backend
Author: Amit Bahuguna | github.com/Amitcicd
Mock data demo — connect to Graph API for live data
"""

from flask import Flask, render_template, jsonify
import random
from datetime import datetime, timedelta

app = Flask(__name__)

# ── MOCK DATA GENERATORS ──────────────────────────────────────────────────────

DEVICE_NAMES = [
    "GEHC-LT-001","GEHC-LT-002","GEHC-DT-045","GEHC-LT-112","GEHC-MB-033",
    "CORP-WIN-201","CORP-WIN-202","CORP-LT-089","CORP-DT-156","CORP-MB-044",
    "FIN-LT-301","FIN-LT-302","FIN-DT-078","HR-LT-401","HR-LT-402",
    "IT-LT-501","IT-DT-023","IT-MB-067","OPS-LT-601","OPS-DT-034",
    "ENG-LT-701","ENG-LT-702","ENG-DT-089","SALES-LT-801","SALES-MB-012",
]
USERS = [
    "john.smith","sarah.jones","amit.bahuguna","mike.wilson","lisa.chen",
    "david.kumar","emily.ross","raj.patel","anna.white","tom.harris",
    "priya.sharma","carlos.mendez","nina.brown","james.taylor","kate.martin",
]
OS_VERSIONS = {
    "Windows": ["Windows 11 22H2","Windows 11 23H2","Windows 11 24H2","Windows 10 22H2"],
    "iOS":     ["iOS 17.4","iOS 17.5","iOS 16.7","iOS 17.3"],
    "Android": ["Android 13","Android 14","Android 12"],
    "macOS":   ["macOS 14.4","macOS 13.6","macOS 14.3"],
}
PLATFORMS   = ["Windows","Windows","Windows","Windows","iOS","iOS","Android","macOS"]
COMPLIANCE  = ["Compliant","Compliant","Compliant","NonCompliant","InGracePeriod","NotEvaluated"]
APPS = [
    {"name":"Google Chrome","version":"124.0.6367","publisher":"Google LLC"},
    {"name":"7-Zip 23.01","version":"23.01","publisher":"Igor Pavlov"},
    {"name":"Zoom Client","version":"6.0.11","publisher":"Zoom Video Comm."},
    {"name":"Adobe Acrobat Reader","version":"24.002","publisher":"Adobe Inc."},
    {"name":"Notepad++","version":"8.6.4","publisher":"Notepad++ Team"},
    {"name":"Microsoft Teams","version":"24104.2","publisher":"Microsoft Corp."},
    {"name":"Slack","version":"4.38.125","publisher":"Slack Technologies"},
    {"name":"VLC Media Player","version":"3.0.21","publisher":"VideoLAN"},
]
INTENTS     = ["Required","Available","Required","Required","Available"]
DEPLOY_STATUS = ["Success","Success","Success","Failed","Pending","Success","Success"]
GROUP_NAMES = [
    "All-Devices","IT-Team","Finance-Users","HR-Department",
    "Sales-Team","Engineering","Operations","Executive-Team",
]
AP_STATUS   = ["Enrolled","Enrolled","Enrolled","Failed","Pending","Enrolled","Enrolled"]
AP_PROFILES = ["AADJ-Standard","Hybrid-Join","AADJ-Kiosk","AADJ-Standard","Hybrid-Join"]


def rand_date(days_back=30):
    return (datetime.now() - timedelta(days=random.randint(0, days_back))).strftime("%Y-%m-%d %H:%M")


def make_devices(n=25):
    devices = []
    for i in range(n):
        platform = random.choice(PLATFORMS)
        compliance = random.choice(COMPLIANCE)
        devices.append({
            "id":         f"DEV-{i+1:04d}",
            "name":       DEVICE_NAMES[i % len(DEVICE_NAMES)],
            "user":       USERS[i % len(USERS)] + "@corp.com",
            "platform":   platform,
            "os":         random.choice(OS_VERSIONS[platform]),
            "compliance": compliance,
            "lastSync":   rand_date(7),
            "enrolled":   rand_date(90),
            "encrypted":  random.choice([True, True, True, False]),
            "managed":    True,
        })
    return devices


def make_autopilot(n=20):
    deployments = []
    for i in range(n):
        status = random.choice(AP_STATUS)
        deployments.append({
            "id":       f"AP-{i+1:04d}",
            "serial":   f"{random.randint(1000,9999)}-{random.randint(1000,9999)}-{random.randint(1000,9999)}",
            "device":   f"CORP-{random.choice(['LT','DT','MB'])}-{random.randint(100,999)}",
            "profile":  random.choice(AP_PROFILES),
            "groupTag": random.choice(["AADJ","HAADJ","KIOSK"]),
            "status":   status,
            "date":     rand_date(14),
            "duration": f"{random.randint(8,45)} min" if status == "Enrolled" else "—",
            "user":     random.choice(USERS) + "@corp.com",
        })
    return deployments


def make_apps():
    apps = []
    for i, app_info in enumerate(APPS):
        total   = random.randint(80, 200)
        success = random.randint(int(total * 0.75), total)
        failed  = random.randint(0, int(total * 0.1))
        pending = total - success - failed
        apps.append({
            "id":        f"APP-{i+1:04d}",
            "name":      app_info["name"],
            "version":   app_info["version"],
            "publisher": app_info["publisher"],
            "intent":    random.choice(INTENTS),
            "groups":    random.sample(GROUP_NAMES, random.randint(1,3)),
            "total":     total,
            "success":   success,
            "failed":    failed,
            "pending":   pending,
            "lastUpdate":rand_date(3),
        })
    return apps


# ── ROUTES ────────────────────────────────────────────────────────────────────

@app.route("/")
def index():
    return render_template("index.html")


@app.route("/api/summary")
def api_summary():
    devices = make_devices(25)
    ap      = make_autopilot(20)
    apps    = make_apps()

    compliant    = sum(1 for d in devices if d["compliance"] == "Compliant")
    non_compliant= sum(1 for d in devices if d["compliance"] == "NonCompliant")
    grace        = sum(1 for d in devices if d["compliance"] == "InGracePeriod")
    not_eval     = sum(1 for d in devices if d["compliance"] == "NotEvaluated")
    encrypted    = sum(1 for d in devices if d["encrypted"])
    ap_success   = sum(1 for a in ap if a["status"] == "Enrolled")
    ap_failed    = sum(1 for a in ap if a["status"] == "Failed")
    ap_pending   = sum(1 for a in ap if a["status"] == "Pending")
    app_success  = sum(a["success"] for a in apps)
    app_failed   = sum(a["failed"] for a in apps)
    app_pending  = sum(a["pending"] for a in apps)

    return jsonify({
        "devices": {
            "total":       len(devices),
            "compliant":   compliant,
            "nonCompliant":non_compliant,
            "gracePeriod": grace,
            "notEvaluated":not_eval,
            "encrypted":   encrypted,
            "complianceRate": round(compliant / len(devices) * 100, 1),
        },
        "autopilot": {
            "total":   len(ap),
            "success": ap_success,
            "failed":  ap_failed,
            "pending": ap_pending,
            "successRate": round(ap_success / len(ap) * 100, 1),
        },
        "apps": {
            "total":   len(apps),
            "success": app_success,
            "failed":  app_failed,
            "pending": app_pending,
        },
        "lastRefresh": datetime.now().strftime("%H:%M:%S"),
    })


@app.route("/api/devices")
def api_devices():
    return jsonify(make_devices(25))


@app.route("/api/compliance-chart")
def api_compliance_chart():
    devices = make_devices(25)
    by_platform = {}
    for d in devices:
        p = d["platform"]
        if p not in by_platform:
            by_platform[p] = {"Compliant": 0, "NonCompliant": 0, "InGracePeriod": 0, "NotEvaluated": 0}
        by_platform[p][d["compliance"]] += 1
    return jsonify({
        "donut": {
            "labels": ["Compliant","Non-Compliant","Grace Period","Not Evaluated"],
            "data":   [
                sum(1 for d in devices if d["compliance"] == "Compliant"),
                sum(1 for d in devices if d["compliance"] == "NonCompliant"),
                sum(1 for d in devices if d["compliance"] == "InGracePeriod"),
                sum(1 for d in devices if d["compliance"] == "NotEvaluated"),
            ],
        },
        "platform": {
            "labels":      list(by_platform.keys()),
            "compliant":   [by_platform[p]["Compliant"] for p in by_platform],
            "nonCompliant":[by_platform[p]["NonCompliant"] for p in by_platform],
        },
    })


@app.route("/api/autopilot")
def api_autopilot():
    ap = make_autopilot(20)
    # trend: last 14 days
    trend = {}
    for i in range(14):
        day = (datetime.now() - timedelta(days=13-i)).strftime("%b %d")
        trend[day] = {"success": random.randint(0, 5), "failed": random.randint(0, 2)}
    return jsonify({
        "deployments": ap,
        "trend": {
            "labels":  list(trend.keys()),
            "success": [trend[d]["success"] for d in trend],
            "failed":  [trend[d]["failed"] for d in trend],
        },
    })


@app.route("/api/apps")
def api_apps():
    return jsonify(make_apps())


if __name__ == "__main__":
    app.run(debug=True, port=5000)
