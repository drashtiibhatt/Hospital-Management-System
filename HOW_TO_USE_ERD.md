# How to Generate ERD Diagram Using dbdiagram.io

## Method 1: Using dbdiagram.io Website (Recommended)

### Step 1: Go to dbdiagram.io
Visit: **https://dbdiagram.io/home**

### Step 2: Create New Diagram
1. Click on **"Go to App"** or **"Sign In"** (free account recommended)
2. Click **"New Diagram"** button

### Step 3: Import the DBML Script
**Option A: Copy-Paste**
1. Open the file `database_erd.dbml` in any text editor
2. Copy all the content (Ctrl+A, Ctrl+C)
3. In dbdiagram.io, delete the sample code
4. Paste your copied DBML code (Ctrl+V)
5. The diagram will auto-generate on the right side

**Option B: Import File**
1. Click **"Import"** button in dbdiagram.io
2. Select **"Import from file"**
3. Choose the `database_erd.dbml` file
4. Click **"Open"**

### Step 4: View and Customize
- The ERD diagram will automatically appear on the right panel
- You can:
  - **Zoom In/Out**: Use mouse scroll or zoom controls
  - **Pan**: Click and drag the diagram
  - **Rearrange Tables**: Drag tables to organize layout
  - **Change Theme**: Light/Dark mode toggle
  - **Auto-arrange**: Click "Auto Arrange" button for clean layout

### Step 5: Export the Diagram
Click **"Export"** button and choose:
- **Export as PDF** - For documentation
- **Export as PNG** - For presentations/reports
- **Export as SQL** - Get SQL CREATE statements

---

## Method 2: Quick View Without Account

1. Go to: **https://dbdiagram.io/d**
2. Click **"Import"** > **"From File"**
3. Select `database_erd.dbml`
4. View the generated diagram
5. Export as needed

---

## What You'll See in the Diagram

### Tables Included (8 Total)
1. **users** - Base authentication table (orange/purple group)
2. **admin** - Admin-specific data (orange/purple group)
3. **doctor** - Doctor profiles (orange/purple group)
4. **patient** - Patient information (orange/purple group)
5. **specialization** - Medical departments (blue group)
6. **doctor_availability** - Doctor schedules (blue group)
7. **appointment** - Booking records (green group)
8. **treatment** - Medical records (green group)

### Relationships Shown
- **One-to-One**: users ↔ admin, users ↔ doctor, users ↔ patient
- **One-to-Many**:
  - specialization → doctor
  - doctor → doctor_availability
  - doctor → appointment
  - patient → appointment
- **One-to-One**: appointment ↔ treatment

### Color-Coded Groups
- 🟣 **User Management**: users, admin, doctor, patient
- 🔵 **Medical Data**: specialization, doctor_availability
- 🟢 **Appointment System**: appointment, treatment

---

## Features of the Generated Diagram

✅ **All 8 tables** with complete column definitions
✅ **Primary keys** highlighted
✅ **Foreign key relationships** with connecting lines
✅ **Indexes** for performance optimization
✅ **Data types** for each column
✅ **Constraints** (unique, not null, default values)
✅ **Table notes** with descriptions
✅ **Column notes** for documentation
✅ **Table grouping** by functionality

---

## Tips for Best View

1. **Auto-Arrange**: Click the "Auto Arrange" button for clean layout
2. **Zoom**: Adjust zoom to 75-100% for best overview
3. **Full Screen**: Use full screen mode (F11) for better visibility
4. **Export High-Res**: Export as PNG at 2x or 3x resolution for clarity

---

## Editing the Diagram

### To Add a New Table:
```dbml
Table new_table {
  id integer [pk, increment]
  name varchar(100)

  Note: 'Description here'
}
```

### To Add a Relationship:
```dbml
Ref: table1.column > table2.column  // One-to-Many
Ref: table1.column - table2.column  // One-to-One
Ref: table1.column < table2.column  // Many-to-One
```

### To Add an Index:
```dbml
Table example {
  id integer [pk]
  name varchar(100)

  indexes {
    name [unique]
    (column1, column2) [name: 'idx_name']
  }
}
```

---

## Troubleshooting

**Issue**: Diagram not loading
- **Solution**: Refresh the page and re-import

**Issue**: Relationships not showing
- **Solution**: Check that foreign key references are correct

**Issue**: Export not working
- **Solution**: Sign in to dbdiagram.io (free account)

---

## Alternative Tools

If dbdiagram.io doesn't work, you can also use:
1. **draw.io** (https://draw.io) - Manual drawing
2. **Lucidchart** (https://lucidchart.com) - Professional tool
3. **MySQL Workbench** - If using MySQL
4. **DBeaver** - Database visualization tool

---

## File Location
- DBML Script: `database_erd.dbml`
- Database Schema Doc: `docs/database_schema.md`

---

**Created**: 2025-11-29
**For**: Hospital Management System - IIT Madras Project
