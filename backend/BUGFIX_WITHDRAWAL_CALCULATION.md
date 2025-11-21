# Bug Fix: Withdrawal Calculation Error

## Issue Reported

User tried to withdraw 1000 BDT from a campaign with:
- Donated: 2000 BDT
- Available: Should be 1900 BDT (after 5% platform fee)

But got error:
```
ValidationError: Total withdrawals (2000.00) cannot exceed net donations (1900.00)
```

## Root Causes Found

### Bug #1: Incorrect `available_balance` Calculation ⚠️ **CRITICAL**

**Location**: `apps/campaigns/models.py` line 146

**Problem**:
```python
# WRONG - was using gross amount
return max(Decimal('0'), self.current_amount - self.withdrawn_amount)
```

**Issue**: 
- `current_amount` is the GROSS donation amount (before platform fees)
- But creators can only withdraw the NET amount (after platform fees)
- This caused `available_balance` to show 2000 BDT instead of 1900 BDT

**Fix**:
```python
# CORRECT - now using net amount
return max(Decimal('0'), self.net_amount - self.withdrawn_amount)
```

**Impact**: 
- This was allowing users to see they could withdraw more than actually available
- Would have caused validation errors when trying to withdraw
- Could have led to financial discrepancies

### Bug #2: Signal Validation Running on Every Save

**Location**: `apps/withdrawals/signals.py` line 60-65

**Problem**:
The `post_save` signal was validating withdrawal amounts even for pending withdrawals.

**Issue**:
- Signal should ONLY update `withdrawn_amount` field
- Validation should happen in:
  1. `Withdrawal.clean()` - for initial creation
  2. `pre_save` signal - when status changes to 'completed'
- The `post_save` signal was incorrectly validating, causing errors

**Fix**:
Removed validation from `post_save` signal. Now it only updates `withdrawn_amount`.

### Bug #3: Incomplete Validation in `pre_save` Signal

**Location**: `apps/withdrawals/signals.py` line 13-30

**Problem**:
The `pre_save` signal was using `campaign.can_withdraw()` which doesn't account for the current withdrawal being completed.

**Fix**:
Updated to manually calculate total withdrawals including the current one:
```python
# Get all OTHER completed withdrawals
other_completed = Withdrawal.objects.filter(
    campaign=campaign,
    status='completed'
).exclude(pk=instance.pk)

other_total = other_completed.aggregate(
    total=models.Sum('amount')
)['total'] or Decimal('0')

# Add this withdrawal amount
new_total = other_total + instance.amount

# Check against net amount
if new_total > net_amount:
    raise ValidationError(...)
```

## Files Modified

1. **apps/campaigns/models.py**
   - Fixed `available_balance` property to use `net_amount` instead of `current_amount`

2. **apps/withdrawals/signals.py**
   - Removed validation from `post_save` signal
   - Improved validation in `pre_save` signal
   - Added better error messages

3. **apps/withdrawals/models.py**
   - Improved `save()` method to only validate on creation or when amount/campaign changes

4. **FINANCIAL_TRANSACTIONS.md**
   - Added clarification about gross vs net amounts

## Testing

### Before Fix
```
current_amount (gross): 2000.00 BDT
net_amount (after fees): 1900.00 BDT
withdrawn_amount: 0.00 BDT
available_balance: 2000.00 BDT  ❌ WRONG!
```

### After Fix
```
current_amount (gross): 2000.00 BDT
net_amount (after fees): 1900.00 BDT
withdrawn_amount: 0.00 BDT
available_balance: 1900.00 BDT  ✅ CORRECT!
```

### Validation Tests
```
Can withdraw 1000 BDT? ✅ Yes
Can withdraw 1900 BDT? ✅ Yes (all available)
Can withdraw 2000 BDT? ❌ No - "Insufficient balance. Available: 1900.00 BDT"
```

## Key Concepts

### Financial Flow
```
Donation: 2000 BDT
    ↓
Platform Fee (5%): -100 BDT
    ↓
Net Amount: 1900 BDT ← This is what creator can withdraw
    ↓
Withdrawn: 0 BDT
    ↓
Available Balance: 1900 BDT
```

### Important Formulas
```python
current_amount = sum(completed_donations.amount)  # Gross
net_amount = sum(completed_donations.net_amount)  # After fees
available_balance = net_amount - withdrawn_amount  # What can be withdrawn
```

## Prevention

To prevent similar bugs in the future:

1. **Always use `net_amount` for withdrawal calculations**, never `current_amount`
2. **Platform fees are deducted from donations**, so creators receive less than donated
3. **Validation should happen before save**, not in post_save signals
4. **Test with realistic scenarios** including platform fees

## Migration Required

No database migration needed - this was a logic bug in the code, not a schema issue.

## Deployment Notes

1. No downtime required
2. No data migration needed
3. Existing withdrawals are not affected
4. New withdrawals will now calculate correctly

## Related Issues

This fix ensures:
- ✅ Creators cannot withdraw more than net amount
- ✅ Platform fees are properly accounted for
- ✅ Available balance shows correct amount
- ✅ Validation happens at the right time
- ✅ ACID compliance is maintained

