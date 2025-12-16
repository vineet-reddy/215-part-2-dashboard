SELECT 
    fa.appointment_id,
    d.full_date,
    c.clinic_name,
    bc.booking_channel,
    vm.visit_mode,
    fa.status,
    fa.is_completed,
    fa.is_cancelled,
    fa.is_no_show
FROM olap.fact_appointment fa
JOIN olap.dim_date d ON fa.date_key = d.date_key
JOIN olap.dim_clinic c ON fa.clinic_key = c.clinic_key
JOIN olap.dim_booking_channel bc ON fa.booking_channel_key = bc.booking_channel_key
JOIN olap.dim_visit_mode vm ON fa.visit_mode_key = vm.visit_mode_key
