# Copyright (c) 2025, Manan Shah and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document

class SSCCSettings(Document):

    # this calculate check digit required in SSCC using modulo func
    def calculate_check_digit(self, sscc_base: str) -> int:
        """Calculate GS1 Mod 10 check digit."""
        total = 0
        reverse_digits = sscc_base[::-1]
        for i, digit in enumerate(reverse_digits):
            n = int(digit)
            total += n * (3 if i % 2 == 0 else 1)
        return (10 - (total % 10)) % 10

    def generate_single_sscc(self, ai, company_prefix: str, extension_digit: int, serial: int = None) -> str:
        """Generate a single SSCC."""
        prefix_len = len(company_prefix)
        serial_ref_len = 17 - 1 - prefix_len
        serial_ref = str(serial).zfill(serial_ref_len)
        sscc_base = f"{extension_digit}{company_prefix}{serial_ref}"
        check_digit = self.calculate_check_digit(sscc_base)
        return f"{ai}{sscc_base}{check_digit}"

    @frappe.whitelist()
    def generate_next_sscc(self) -> str:
        """
        Generate next SSCC for this company record and update last_generated_sscc.
        """
        ai = self.application_identifier
        company_prefix = self.gs1_company_prefix
        last_sscc = self.last_generated_sscc

        if not company_prefix:
            frappe.throw("Please set the GS1 Company Prefix for this company")

        prefix_len = len(company_prefix)
        serial_ref_len = 17 - 1 - prefix_len
        max_serial = 10**serial_ref_len - 1

        extension_digit = 0
        serial = 0

        if last_sscc and len(last_sscc) == 18:
            sscc_body = last_sscc[:-1]  #Remove check digit
            extension_digit = int(sscc_body[0])
            serial = int(sscc_body[len(company_prefix) + 1:]) + 1

            if serial > max_serial:
                serial = 0
                extension_digit = (extension_digit + 1) % 10

        new_sscc = self.generate_single_sscc(ai, company_prefix, extension_digit, serial)
        self.last_generated_sscc = new_sscc
        self.save(ignore_permissions=True)
        frappe.db.commit()

        return new_sscc