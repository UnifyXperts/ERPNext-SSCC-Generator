## ERPNext SSCC Generator

The SSCC Generator app provides a reliable and GS1-compliant way to generate Serial Shipping Container Codes (SSCC) directly within the Frappe Framework or ERPNext.

### Overview

The **SSCC Generator App** (`sscc_generator`) is a custom Frappe application designed to generate and manage **Serial Shipping Container Codes (SSCC-18)** for multiple companies within the ERP system.

SSCCs uniquely identify logistic units (such as cartons, pallets, or containers) and are compliant with the **GS1 SSCC-18 standard**.

Each generated SSCC-18 code is stored in the system and incremented automatically for future generations.

## Core Concept: SSCC-18 Structure
 
Its structure is defined by the **GS1 standard** and consists of the following parts:

| Component                       | Description                                                                        | Example   | Length |
| ------------------------------- | ---------------------------------------------------------------------------------- | --------- | ------ |
| **Application Identifier (AI)** | Identifies that this data element is an SSCC. Always `"00"`.                       | 00        | 2      |
| **Extension Digit**             | Used to extend serial capacity. Assigned by the company generating the SSCC (0–9). | 0         | 1      |
| **GS1 Company Prefix**          | Unique number assigned by GS1 to the company.                                      | 0012345   | 7      |
| **Serial Reference**            | Unique number within the company prefix to identify a logistic unit.               | 000000024 | 9      |
| **Check Digit**                 | Calculated using the Modulo 10 algorithm.                                          | 9         | 1      |
| **Total Digits (excluding AI)** | —                                                                                  | —         | 18     |

The complete format looks like:

```
(00) 0 0012345 000000024 9
```

Or, concatenated as a **20-character string** (including AI):

```
00000123450000000249
```

---

## Frappe App Structure

```
sscc_generator/
├── sscc_generator/
│   ├── sscc_generator/
│   │   ├── doctype/
│   │   │   ├── sscc_settings/
│   │   │   │   ├── sscc_settings.py   ← Core Logic
│   │   │   │   ├── sscc_settings.json ← Doctype Meta
│   │   │   │   ├── sscc_settings.js   ← Client Script (optional)
│   │   │   │   └── __init__.py
│   │   ├── __init__.py
│   ├── hooks.py
│   ├── __init__.py
└── MANIFEST.in
```

---

## Doctype: SSCC Settings

### Purpose

The `SSCC Settings` doctype is the main configuration and data storage for each company’s SSCC generation logic.

Each record corresponds to one company and stores its **GS1 Company Prefix**, **Application Identifier**, and **last generated SSCC**.

### Fields

| Field                           | Type   | Description                                                                     |
| ------------------------------- | ------ | ------------------------------------------------------------------------------- |
| **Company Name**                | Data   | Name of the company this record represents.                                     |
| **Application Identifier**      | Data   | Default is `"00"`. Identifies SSCC data type.                                   |
| **GS1 Company Prefix**          | Data   | GS1-assigned prefix for this company (7–10 digits).                             |
| **Last Generated SSCC**         | Data   | Stores the last generated SSCC (20 characters). Used for sequential generation. |
| **Creation / Modified / Owner** | System | Standard Frappe metadata fields.                                                |

### Example Record

```json
{
  "name": "Makable",
  "company_name": "Makable",
  "application_identifier": "00",
  "gs1_company_prefix": "0012345",
  "last_generated_sscc": "00000123450000000249",
  "doctype": "SSCC Settings"
}
```

---

## Installation Guide

The **SSCC Generator** app can be installed on any existing **Frappe / ERPNext** site.

---

### Prerequisites

Before installing, ensure you have:

* Frappe Framework **v14+ or v15+**
* ERPNext (optional, but supported)
* Bench installed and working
* Access to the server terminal

Check versions:

```bash
bench version
```

---

### Step 1: Get the App

From your bench directory, run:

```bash
bench get-app sscc_generator https://github.com/<your-username>/sscc_generator
```

Replace `<your-username>` with the actual GitHub username or organization.

---

### Step 2: Install the App on Your Site

```bash
bench --site your-site-name install-app sscc_generator
```

**Example:**

```bash
bench --site site1.local install-app sscc_generator
```

---

### Step 3: Apply Migrations

```bash
bench migrate
```

This will:

* Create the **SSCC Settings** doctype
* Register permissions
* Sync app metadata

---

### Step 4: Restart Bench

```bash
bench restart
```

*(Required for production or supervisor setups.)*

---

### Step 5: Configure SSCC Settings

1. Login to ERPNext
2. Go to **SSCC Settings**
3. Create a new record for each company

### Required Fields:

* **Company Name**
* **GS1 Company Prefix** (7–10 digits)
* **Application Identifier** (default: `00`)

Save the record.

---

### Step 6: Generate Your First SSCC

From **Bench Console**:

```bash
bench console
```

```python
doc = frappe.get_doc("SSCC Settings", "Makable")
doc.generate_next_sscc()
```

**Output:**

```
00000123450000000478
```

✔ 18-digit SSCC
✔ GS1 compliant
✔ Ready for barcode generation

---

## References

- GS1: [What is an SSCC?](https://www.gs1.org/standards/id-keys/sscc)
    
- GS1: [Check Digit Calculator](https://www.gs1.org/services/check-digit-calculator)
    
- GS1: [Company Prefix Registration](https://www.gs1.org/company-prefix)
