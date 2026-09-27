# ParkFlow Kenya 🇰🇪

## Smart Parking Management and Payment System

ParkFlow Kenya is a web-based parking management system designed to automate vehicle entry, parking slot allocation, fee calculation, payment recording, receipts, auditing, reporting, and parking availability monitoring.

The system was developed using **Python/Django** for the web application and **C++** for the supporting object-oriented prototype and parking algorithms.

---

## 🚗 Key Features

### Vehicle Entry
- Records vehicle registration number
- Records vehicle type
- Automatically assigns the first available parking slot
- Prevents the same vehicle from having multiple active parking sessions

### Live Parking Management
- Displays total parking slots
- Shows available slots
- Shows occupied slots
- Displays active parking sessions
- Provides a public live parking display

### Automatic Fee Calculation

The system supports configurable parking rates:

| Parking Duration | Fee |
|---|---:|
| Up to 30 minutes | KSh 0 |
| 31 minutes - 2 hours | KSh 50 |
| Over 2 - 4 hours | KSh 100 |
| Over 4 - 6 hours | KSh 300 |
| Over 6 hours | KSh 500 |

Parking rates can be changed through the management interface without modifying the application source code.

### Payment Management

The system supports:

- M-Pesa
- Card
- Cash

Each confirmed payment receives:

- Transaction reference
- Receipt number
- Payment timestamp
- Payment method
- Amount
- VAT field

> Note: M-Pesa and card transactions are currently simulated for the prototype. Live payment gateway integration can be added in a production deployment.

### Receipts
The system generates a receipt after a confirmed payment containing the relevant parking and payment information.

### Audit Trail
Confirmed payments are recorded in an audit log containing:

- Payment action
- Vehicle
- Amount
- Payment method
- Receipt number
- User
- Timestamp

### Management Reports
Management users can view:

- Total revenue
- Cash revenue
- M-Pesa revenue
- Card revenue
- Number of transactions
- Completed parking sessions
- Recent payment transactions

### User Roles

#### Parking Staff
Can:
- Log in
- Register vehicles
- Process vehicle exits
- Process parking payments
- View operational information

#### Management
Can:
- Access reports
- Manage parking rates
- View audit records
- Access operational functions

---

# 🏗️ System Architecture

```text
                    USER / DRIVER
                         │
                         ▼
                ┌─────────────────┐
                │   Web Browser   │
                └────────┬────────┘
                         │
                         ▼
                ┌─────────────────┐
                │ HTML / CSS / JS │
                └────────┬────────┘
                         │
                         ▼
                ┌─────────────────┐
                │     Django      │
                │    Backend      │
                └────────┬────────┘
                         │
                         ▼
                ┌─────────────────┐
                │ Business Logic  │
                └────────┬────────┘
                         │
                         ▼
                ┌─────────────────┐
                │ SQLite Database │
                └─────────────────┘