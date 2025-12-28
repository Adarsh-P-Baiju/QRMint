# QRMint - Enterprise QR Suite

**QRMint** is a professional-grade desktop application designed to streamline UPI (Unified Payments Interface) operations for businesses and power users. It combines a secure, "kiosk-style" interface with powerful tools for bulk generation, financial tracking, and operational analytics.

Designed for reliability and speed, QRMint operates completely offline, ensuring your transaction data remains private and secure on your local machine.

---

## ✨ Comprehensive Feature Suite

### 1. 🖥️ Immersive "Kiosk" Interface
QRMint is built to be a dedicated workstation tool.
*   **True Borderless Mode**: The application launches in a distraction-free, fullscreen "Game Mode," maximizing screen real estate for data visibility.
*   **Safe Exit Protocols**: Prevents accidental closures. Exiting requires specific actions (Login Button, Sidebar Footer, or `Ctrl+C` shortcut) with a confirmation dialog.
*   **Custom UI Experience**: Features a fully custom design system with rounded corners, glass-morphism effects, and consistent custom dialogs (Success, Error, Confirmation) that replace standard operating system alerts.

### 2. ⚡ Advanced QR Generation
Create standard-compliant UPI QR codes instantly.
*   **Smart Preview**: See your QR code generate in real-time as you type.
*   **Logo Integration**: Upload and center-align your brand's logo. The app automatically handles resizing and transparency to ensure the QR remains scannable.
*   **Persistent Credentials**: Set default VPA (UPI ID) and Payee Names in Settings to speed up manual entry.
*   **Status Tracking**: Mark generated codes as "Paid", "Unpaid", or "Pending" right from the moment of creation.

### 3. 🚀 High-Volume Batch Processing
Ideal for payroll, rent collection, or mass invoicing.
*   **Excel & CSV Support**: Upload spreadsheets containing hundreds of payment records.
*   **Smart Validation**: The system automatically validates row data (VPA, Name, Amount) before processing to prevent errors.
*   **Automated Reporting**: Automatically generates a downloadable Excel report (`.xlsx`) upon completion, detailing every generated QR and its status.
*   **Template Download**: Includes a built-in "Download Sample Template" feature so you know exactly how to structure your data.

### 4. � Intelligent History & Management
A powerful ledger for all your generated codes.
*   **Unified Timeline**: View both manually generated and batch-generated records in a single, responsive feed.
*   **Real-Time Search**: Filter thousands of records instantly by Name, VPA, Amount, or Note phrases.
*   **Status Filtering**: Quickly isolate "Unpaid" bills or "Pending" transactions with a dedicated dropdown filter.
*   **Inline Editing**: Fix typos, update payment statuses, or change logos for any past record without regenerating the code.
*   **Details Drawer**: a non-intrusive side-drawer allows you to view full details, print, or download individual QRs.

### 5. 📊 Dashboard Analytics
Turn your generation activity into actionable insights.
*   **Visual Charts**: Interactive Pie Charts showing Paid vs. Unpaid distribution and Bar Charts tracking generation volume over the last 7 days.
*   **Financial Overview**: Instant cards displaying Total Generated Value, Total Collected (Paid), and Outstanding (Unpaid) amounts.
*   **Recent Activity**: A quick-glance table showing the most recent 5 transactions for immediate context.

### 6. 🔄 Recurring Templates
Save time on repetitive tasks.
*   **One-Click Load**: Save frequent payment profiles (e.g., "Office Rent", "Staff Salary", "Vendor A").
*   **Drawer Access**: Access your saved templates via a slide-out drawer on the Generator page, allowing you to populate forms instantly.

### 7. 🎨 Design Studio (NEW in V6.0)
Customize your QR codes to match your brand identity.
*   **Color Presets**: Choose from 6 professionally curated color schemes (Classic, Brand Blue, Eco Green, Royal Purple, Dark Mode, Gold).
*   **Custom Colors**: Apply any hex color to QR foreground and background for complete brand alignment.
*   **Live Updates**: See changes instantly - change colors and regenerate QR codes on the fly.
*   **Scannable Quality**: All color combinations are tested to maintain QR code scannability.

### 8. 🔗 Smart Payment Links (NEW in V6.0)
Share payment details beyond QR codes.
*   **Copy UPI Link**: Generate and copy standard `upi://pay?` links with one click for sharing via WhatsApp, SMS, or Email.
*   **Universal Access**: Recipients can open the link on any UPI-enabled app without scanning.
*   **Generator & History**: Available in both the Generator page (after preview) and History Details drawer.

### 9. 🏦 Multi-Bank Account Management (NEW in V7.0)
Manage unlimited bank accounts with quick-switch capability.
*   **Dedicated Banks Page**: Card-based UI displaying all saved bank accounts with VPA, account holder name, and default status.
*   **Quick Switch**: Dropdown in Generator to select any saved bank - VPA and Name auto-fill instantly.
*   **Add On-The-Fly**: "+ Add Bank" button right in the Generator for seamless workflow.
*   **Default Bank**: Set any bank as default to auto-load on Generator page.
*   **Full CRUD**: Add, edit, delete, and set default banks from the Banks page.

### 10. 🔒 Enterprise-Grade Security
*   **User Authentication**: The application is locked behind a secure login screen.
*   **Password Management**: Users can update their security credentials directly from the Settings page.
*   **Local Data Sovereignty**: All data is stored in an encrypted local `SQLite` database. Zero cloud dependencies mean zero data leaks.
*   **Disaster Recovery**: Built-in "Backup & Restore" allows you to save a snapshot of your entire database to a secure location and restore it instantly if needed.

### 11. 🖨️ Production Ready
*   **Direct Print**: Send QR codes directly to your connected printer with a single click (Windows native support).
*   **Export Capabilities**: Generate professional PDF reports or Excel dumps of your entire transaction history for auditing or sharing with stakeholders.

---
*Built with Python 3.10+, CustomTkinter, and local SQLite.*

## 📦 Installation & Setup

Follow these steps to set up QRMint on your local machine.

### Prerequisites
*   **Python 3.10** or higher installed.
*   **Git** installed.

### 1. Clone the Repository
Open your terminal or command prompt and run:
```bash
git clone https://github.com/Adarsh-P-Baiju/QRMint.git
cd QRMint
```

### 2. Create a Virtual Environment (Recommended)
Isolate your dependencies by creating a virtual environment:
```bash
# Windows
python -m venv env
.\env\Scripts\activate

# Mac/Linux
python3 -m venv env
source env/bin/activate
```

### 3. Install Dependencies
Install all required Python packages from the requirements file:
```bash
pip install -r requirements.txt
```

---

## 🚀 How to Run

Once installed, there are two ways to launch the application:

### Option A: Run from Source (Development)
Simply execute the main script:
```bash
python main.py
```

### Option B: Build Executable (Production)
To create a standalone `.exe` file that you can share or run without opening a terminal:

1.  **Run the Build Script**:
    ```bash
    python build.py
    ```
2.  **Locate the App**:
    After the build completes, your `QRMint.exe` file will be in the `dist/` folder.

