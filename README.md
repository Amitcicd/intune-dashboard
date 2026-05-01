# Intune Dashboard — Python Flask

**A real-time web dashboard for Microsoft Intune — Device Compliance, Autopilot Deployments, and Win32 App Status.**

Built by **Amit Bahuguna** — Senior Modern Workplace Engineer  
`MD-102 Certified | GE Healthcare | HCLTech`  
[linkedin.com/in/amit-bahuguna](https://linkedin.com/in/amit-bahuguna)

---

## What it shows

| Tab | Data |
|---|---|
| **Overview** | Summary cards + compliance donut + platform bar + autopilot trend + app status |
| **Devices** | All managed devices — compliance, platform, OS, encryption, last sync |
| **Autopilot** | Deployment trend chart, success/fail donut, full deployment table |
| **Win32 Apps** | App-by-app deployment status with progress bars, intent, groups |

---

## Quick Start

```bash
# 1. Clone the repo
git clone https://github.com/Amitcicd/intune-dashboard
cd intune-dashboard

# 2. Install dependencies
pip install -r requirements.txt

# 3. Run
python app.py

# 4. Open browser
http://localhost:5000
```

---

## Project Structure

```
intune-dashboard/
├── app.py              # Flask backend — mock data APIs
├── requirements.txt
├── README.md
└── templates/
    └── index.html      # Dashboard UI — Chart.js + vanilla JS
```

---

## Connecting to Live Intune Data

Replace mock data functions in `app.py` with Microsoft Graph API calls:

```python
import requests

GRAPH_BASE = "https://graph.microsoft.com/v1.0"

def get_graph_token(tenant_id, client_id, client_secret):
    r = requests.post(
        f"https://login.microsoftonline.com/{tenant_id}/oauth2/v2.0/token",
        data={
            "grant_type":    "client_credentials",
            "client_id":     client_id,
            "client_secret": client_secret,
            "scope":         "https://graph.microsoft.com/.default"
        }
    )
    return r.json()["access_token"]

# Then replace make_devices() with:
def get_live_devices(token):
    headers = {"Authorization": f"Bearer {token}"}
    r = requests.get(f"{GRAPH_BASE}/deviceManagement/managedDevices", headers=headers)
    return r.json()["value"]
```

**Required Graph API permissions:**
- `DeviceManagementManagedDevices.Read.All`
- `DeviceManagementApps.Read.All`
- `Group.Read.All`

---

## Built from Production Experience

Designed from real endpoint management work managing **5,000+ devices** at **GE Healthcare** via HCLTech — covering Intune, Autopilot, Win32 deployment, WDAC, and CIS Benchmark hardening.

---

## Author

**Amit Bahuguna**  
Senior Modern Workplace Engineer | MD-102 Certified  
[github.com/Amitcicd](https://github.com/Amitcicd)
