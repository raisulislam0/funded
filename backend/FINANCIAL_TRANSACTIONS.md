# Financial Transaction System - ACID Compliance

This document describes the ACID-compliant financial transaction system implemented for the crowdfunding platform.

## Overview

The system tracks three key financial metrics for each campaign:

1. **current_amount**: Total donations received (gross amount)
2. **withdrawn_amount**: Total amount withdrawn by campaign creator
3. **net_amount**: Amount after platform fees (available for withdrawal)

## Key Principles

### 1. ACID Compliance

All financial transactions use Django's database transactions with row-level locking to ensure:

- **Atomicity**: All operations complete or none do
- **Consistency**: Data integrity is maintained
- **Isolation**: Concurrent transactions don't interfere
- **Durability**: Committed transactions are permanent

### 2. Financial Rules

- Only **completed** donations count toward campaign totals
- Only **completed** withdrawals count toward withdrawn_amount
- Withdrawals cannot exceed net_amount (donations minus platform fees)
- Database constraints prevent negative balances
- All amounts are validated before processing

## Data Flow

### Donation Flow

```
1. Donation created (status='pending')
   ↓
2. Payment processed
   ↓
3. Status changed to 'completed'
   ↓
4. Signal updates campaign.current_amount
   ↓
5. Platform fee calculated
   ↓
6. Net amount available for withdrawal
```

### Withdrawal Flow

```
1. Creator requests withdrawal
   ↓
2. System validates available balance
   ↓
3. Admin reviews and approves
   ↓
4. Status changed to 'completed'
   ↓
5. Signal updates campaign.withdrawn_amount (with row lock)
   ↓
6. Available balance recalculated
```

## Database Schema

### Campaign Model

```python
goal_amount          # Target fundraising amount
current_amount       # Total donations GROSS amount (auto-calculated)
withdrawn_amount     # Total withdrawals (auto-calculated)
net_amount          # Property: donations - platform_fees (what creator receives)
available_balance   # Property: net_amount - withdrawn_amount (what can be withdrawn)
```

**IMPORTANT**:

- `current_amount` = GROSS donations (before fees)
- `net_amount` = NET donations (after platform fees) - **This is what the creator actually receives**
- `available_balance` = `net_amount - withdrawn_amount` - **This is what can still be withdrawn**
- Platform fees are deducted from donations, so creators can only withdraw the net amount

### Constraints

```sql
CHECK (withdrawn_amount >= 0)
CHECK (withdrawn_amount <= current_amount)
```

## Signals

### Donation Signals (`apps/donations/signals.py`)

- **post_save**: Updates campaign totals when donation status changes
- **post_delete**: Recalculates totals when donation is deleted
- Uses `select_for_update()` for row-level locking

### Withdrawal Signals (`apps/withdrawals/signals.py`)

- **pre_save**: Validates withdrawal before saving
- **post_save**: Updates withdrawn_amount with atomic transaction
- Uses `select_for_update()` to prevent race conditions

## Validation Layers

### 1. Model Level (`models.py`)

```python
# Campaign.can_withdraw(amount)
- Checks amount > 0
- Validates against net_amount - withdrawn_amount
- Returns (bool, error_message)

# Withdrawal.clean()
- Validates creator is campaign owner
- Calls campaign.can_withdraw()
```

### 2. Serializer Level (`serializers.py`)

```python
# CreateWithdrawalSerializer
- Validates campaign ownership
- Validates positive amount
- Calls campaign.can_withdraw()
```

### 3. Admin Level (`admin.py`)

```python
# WithdrawalAdmin
- Displays available balance
- Shows financial summary
- Validates on status change
```

### 4. Database Level

```sql
# Check constraints
- withdrawn_amount >= 0
- withdrawn_amount <= current_amount
```

## Race Condition Prevention

### Problem

Two simultaneous withdrawals could exceed available balance:

```
Thread A: Check balance (OK) → Withdraw 1000
Thread B: Check balance (OK) → Withdraw 1000
Result: Over-withdrawal!
```

### Solution

```python
with transaction.atomic():
    campaign = Campaign.objects.select_for_update().get(pk=pk)
    # Row is locked, other transactions wait
    # Validate and update
    campaign.withdrawn_amount += amount
    campaign.save()
# Lock released
```

## Management Commands

### Recalculate Campaign Stats

```bash
python manage.py recalculate_campaign_stats
```

Recalculates current_amount, total_donors, total_donations from completed donations.

### Recalculate Withdrawals

```bash
python manage.py recalculate_withdrawals
```

Recalculates withdrawn_amount from completed withdrawals.

## Testing Checklist

- [ ] Create donation with status='pending' → campaign amount unchanged
- [ ] Change donation to 'completed' → campaign amount updated
- [ ] Create withdrawal exceeding balance → validation error
- [ ] Complete withdrawal → withdrawn_amount updated
- [ ] Concurrent withdrawals → no over-withdrawal
- [ ] Delete completed donation → campaign amount recalculated
- [ ] Platform fee correctly deducted from net_amount

## Security Considerations

1. **Authorization**: Only campaign creators can request withdrawals
2. **Validation**: Multiple layers prevent invalid transactions
3. **Audit Trail**: All transactions logged with timestamps
4. **Idempotency**: Signals handle duplicate calls safely
5. **Constraints**: Database enforces data integrity

## Error Handling

All financial operations include proper error handling:

- ValidationError for business rule violations
- IntegrityError for database constraint violations
- Transaction rollback on any error
- User-friendly error messages

## Future Enhancements

- [ ] Add transaction history table
- [ ] Implement refund workflow
- [ ] Add withdrawal fee calculation
- [ ] Implement partial withdrawals
- [ ] Add financial reporting dashboard
- [ ] Implement automated reconciliation
