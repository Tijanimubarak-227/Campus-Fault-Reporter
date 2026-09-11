"""First draft (v0) - kept only as defect evidence for the workbook.
This version does NOT guard against overpayment: it silently clamps the
balance to 0 instead of rejecting the excess payment."""

def calculate_hall_dues_v0(amount_due, previous_payments, new_payment):
    total_paid = previous_payments + new_payment
    remaining = amount_due - total_paid
    if remaining < 0:
        remaining = 0  # BUG: silently accepts overpayment, no signal to caller/UI
    status = "PAID_IN_FULL" if remaining == 0 else "PARTIAL"
    return remaining, status
