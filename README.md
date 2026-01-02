## SSCC Generator

The SSCC Generator app provides a reliable and GS1-compliant way to generate Serial Shipping Container Codes (SSCC) directly within the Frappe Framework or ERPNext.

#### License

mit

### 📦 Overview

The **SSCC Generator App** (`sscc_generator`) is a custom Frappe application designed to generate and manage **Serial Shipping Container Codes (SSCC-18)** for multiple companies within the ERP system.

SSCCs uniquely identify logistic units (such as cartons, pallets, or containers) and are compliant with the **GS1 SSCC-18 standard**.

Each generated SSCC-18 code is stored in the system and incremented automatically for future generations.

## 🧩 Core Concept: SSCC-18 Structure

An **SSCC-18** is a **unique 18-digit number** that identifies a single logistic unit.  
Its structure is defined by the **GS1 standard** and consists of the following parts:

| Component                       | Description                                                                        | Example   | Length |
| ------------------------------- | ---------------------------------------------------------------------------------- | --------- | ------ |
| **Application Identifier (AI)** | Identifies that this data element is an SSCC. Always `"00"`.                       | 00        | 2      |
| **Extension Digit**             | Used to extend serial capacity. Assigned by the company generating the SSCC (0–9). | 0         | 1      |
| **GS1 Company Prefix**          | Unique number assigned by GS1 to the company.                                      | 0012345   | 7      |
| **Serial Reference**            | Unique number within the company prefix to identify a logistic unit.               | 000000024 | 9      |
| **Check Digit**                 | Calculated using the Modulo 10 algorithm.                                          | 9         | 1      |
| **Total Digits (excluding AI)** | —                                                                                  | —         | 18     |

![[Pasted image 20251030094636.png]]

👉 The complete format looks like:

```
(00) 0 0012345 000000024 9
```

Or, concatenated as a **20-character string** (including AI):

```
00000123450000000249
```

---

## ⚙️ Frappe App Structure

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

## 🧾 Doctype: SSCC Settings

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

## 🧰 Usage Steps

### 1. Setup

- Go to **SSCC Settings** doctype in Frappe.
    
- Create a record for your company:
    
    - Enter _Company Name_
        
    - Set _Application Identifier_ (default `00`)
        
    - Set _GS1 Company Prefix_ (7–10 digits)
        

### 2. Generate New SSCC

From Frappe console, API, or server script:

```python
doc = frappe.get_doc("SSCC Settings", "company_name")
new_sscc = doc.generate_next_sscc()
print(new_sscc)
```

### 3. Expected Output

```
00000123450000000250
```

---

## 📚 References

- GS1: [What is an SSCC?](https://www.gs1.org/standards/id-keys/sscc)
    
- GS1: [Check Digit Calculator](https://www.gs1.org/services/check-digit-calculator)
    
- GS1: [Company Prefix Registration](https://www.gs1.org/company-prefix)