SELECT 
    fi.invoice_id,
    d.full_date as invoice_date,
    c.clinic_name,
    fi.total_charge,
    fi.insurance_portion,
    fi.patient_portion,
    fi.status as payment_status
FROM olap.fact_invoice fi
JOIN olap.dim_date d ON fi.date_key = d.date_key
JOIN olap.dim_clinic c ON fi.clinic_key = c.clinic_key
