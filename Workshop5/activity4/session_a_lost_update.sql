-- ==========================================
-- 4.1 Lost Update Demo - SESSION A
-- ==========================================
SET SESSION TRANSACTION ISOLATION LEVEL READ COMMITTED;
START TRANSACTION;
SELECT balance FROM accounts WHERE id=1;
-- Application computes: 1000 + 100 = 1100
UPDATE accounts SET balance=1100 WHERE id=1;
COMMIT;
