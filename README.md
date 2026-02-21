
# 🚛 FleetFlow — Fleet Management System

A full-featured web-based fleet management system built with Django for the Hackathon.

---

## 📋 Problem Statement

Traditional fleet operations rely on manual logbooks, spreadsheets, and phone calls — leading to:
- Cargo overloading risks
- Expired driver licenses going unnoticed
- No real-time vehicle availability tracking
- Zero financial visibility on fuel & maintenance costs

**FleetFlow** solves all of this with a digital, role-based fleet management platform.

---

## 🎯 Core Features

### 🚗 Vehicle Registry
- Add, edit, and retire vehicles
- Track vehicle type (Truck / Van / Bike)
- Max load capacity per vehicle
- Real-time status: Available / On Trip / In Shop / Retired
- Odometer tracking per vehicle
- Region-wise vehicle management

### 👨‍💼 Driver Profiles
- Complete driver profile with license details
- License expiry tracking with auto-alerts
- Safety score system (0-100)
- Driver status: On Duty / Off Duty / Suspended
- Auto-block expired license drivers from trip assignment

### 🗺️ Trip Dispatcher
- Create and dispatch delivery trips
- Cargo weight validation (blocks if cargo > vehicle capacity)
- Only available vehicles shown in dispatcher
- Only valid-license drivers shown in dispatcher
- Trip lifecycle: Draft → Dispatched → Completed / Cancelled
- Auto vehicle status update on dispatch and completion
- End odometer entry on trip completion

### 🔧 Maintenance Logs
- Log vehicle maintenance/service records
- Auto-sets vehicle status to "In Shop" on maintenance entry
- Vehicle automatically removed from dispatcher pool
- Cost tracking per maintenance record

### ⛽ Fuel & Expense Logs
- Fuel log per vehicle and trip
- Total fuel cost tracking
- Total maintenance cost tracking
- Combined operational cost summary

### 📊 Analytics & Reports
- Fleet utilization rate
- Average fuel efficiency (km/Liter)
- Average cost per km
- Per-vehicle cost breakdown (Fuel + Maintenance)
- Total completed trips count
- CSV Export for external reporting

### 🏠 Command Center (Dashboard)
- Real-time KPI cards
- Active fleet count
- Maintenance alerts
- Fleet utilization percentage
- Pending/Draft trips count
- Recent trips table
- Fleet status breakdown (Available / On Trip / In Shop)
- License expiry alerts

---

## 🔐 Role-Based Access Control (RBAC)

| Feature | Manager | Dispatcher | Safety Officer | Analyst |
|---|---|---|---|---|
| Command Center | ✅ | ❌ | ❌ | ❌ |
| Vehicle Registry | ✅ | ✅ | ❌ | ❌ |
| Driver Profiles | ✅ | ❌ | ✅ | ❌ |
| Trip Dispatcher | ✅ | ✅ | ❌ | ❌ |
| Maintenance Logs | ✅ | ✅ | ❌ | ❌ |
| Fuel & Expenses | ✅ | ✅ | ❌ | ❌ |
| Analytics | ✅ | ❌ | ❌ | ✅ |
| CSV Export | ✅ | ❌ | ❌ | ✅ |
| Admin Panel | ✅ | ❌ | ❌ | ❌ |

- Each user is redirected to their role-specific dashboard on login
- Direct URL access is blocked for unauthorized roles
- Superuser has full access to everything

---

## 👥 User Registration with Admin Approval

- New users can submit a registration request
- Admin receives email notification instantly
- Admin reviews and approves/rejects from Admin Panel
- User receives approval/rejection email
- Approved users get auto-assigned to their requested role group

---

## 🔑 Password Reset via Email

- Forgot password flow with email verification
- Secure token-based reset link (expires in 1 hour)
- Full email template with FleetFlow branding

---

## 🧠 Business Logic / Auto Rules

| Rule | Trigger | Result |
|---|---|---|
| Cargo Validation | Trip creation | Blocks if cargo > vehicle capacity |
| License Expiry | Driver assignment | Blocks expired license drivers |
| Auto In Shop | Maintenance logged | Vehicle status → In Shop |
| Auto Available | Trip completed | Vehicle status → Available |
| Auto On Duty | Trip dispatched | Driver status → On Duty |
| Auto Off Duty | Trip completed | Driver status → Off Duty |

---

## 🛠️ Tech Stack

| Layer | Technology |
|---|---|
| Backend | Django 4.2.28 |
| Frontend | Django Templates + Bootstrap 5.3 |
| Database | SQLite3 |
| Styling | Custom CSS (Dark Theme) |
| Icons | Bootstrap Icons 1.11 |
| Email | Gmail SMTP |
| Auth | Django Auth + Groups (RBAC) |
| Platform | macOS (Apple Silicon M4) |

---

## 📁 Project Structure
```
fleetflow/
├── accounts/          # Login, Register, Password Reset
├── vehicles/          # Vehicle Registry
├── drivers/           # Driver Profiles
├── trips/             # Trip Dispatcher
├── maintenance/       # Maintenance Logs
├── expenses/          # Fuel & Expense Logs
├── analytics/         # Reports & CSV Export
├── dashboard/         # Command Center
├── templates/         # All HTML Templates
├── static/css/        # Custom CSS
├── db.sqlite3         # Database
└── manage.py
```

---

## 🚀 Setup & Installation
```bash
# 1. Clone the repository
git clone https://github.com/vishalshekh89-dotcom/FleetFlow_oddoxgvp_Hackathon.git
cd FleetFlow_oddoxgvp_Hackathon/fleetflow

# 2. Create virtual environment
python3 -m venv venv
source venv/bin/activate

# 3. Install dependencies
pip install django pillow reportlab

# 4. Run migrations
python manage.py makemigrations
python manage.py migrate

# 5. Create superuser
python manage.py createsuperuser

# 6. Run server
python manage.py runserver
```

---

## 👤 Default Test Users

| Username | Password | Role |
|---|---|---|
| root | root | Superuser |
| manager1 | Pass@1234 | Manager |
| dispatcher1 | Pass@1234 | Dispatcher |
| safety1 | Pass@1234 | Safety Officer |
| analyst1 | Pass@1234 | Analyst |

---

## 📸 Pages

- `/` — Command Center Dashboard
- `/accounts/login/` — Login
- `/accounts/register/` — Registration Request
- `/vehicles/` — Vehicle Registry
- `/drivers/` — Driver Profiles
- `/trips/` — Trip Dispatcher
- `/maintenance/` — Maintenance Logs
- `/expenses/` — Fuel & Expenses
- `/analytics/` — Analytics & Reports
- `/admin/` — Admin Panel

---

Super user username and password is : root,Kamlesh@2004

Manager Login redirection
Username: manager1
Password: Pass@1234

Dispatcher Login redirection
Username: dispatcher1
Password: Pass@1234

Safety Officer Login redirection
Username: safety1
Password: Pass@1234

Analyst Login redirection
Username: analyst1
Password: Pass@1234
