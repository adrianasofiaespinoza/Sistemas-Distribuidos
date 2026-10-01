-- ==========================================
-- 4.1 Lost Update Demo - SESSION B
-- ==========================================
SET SESSION TRANSACTION ISOLATION LEVEL READ COMMITTED;
START TRANSACTION;
SELECT balance FROM accounts WHERE id=1;
-- Application computes: 1000 - 50 = 950
UPDATE accounts SET balance=950 WHERE id=1;
COMMIT;
