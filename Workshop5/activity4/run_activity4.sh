#!/bin/bash
# Activity 4 - Lost Update and Locking

echo "=== Activity 4: Lost Update and Locking ==="

echo "Step 1: Setting up accounts table..."
docker exec mysql-primary mysql -uroot -proot lab -e "
DROP TABLE IF EXISTS accounts;
CREATE TABLE accounts (
  id INT PRIMARY KEY,
  owner VARCHAR(50),
  balance INT NOT NULL,
  updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
) ENGINE=InnoDB;
INSERT INTO accounts VALUES (1,'Alice',1000,NOW()),(2,'Bob',1000,NOW());"

echo "=== Accounts created ==="
docker exec mysql-primary mysql -uroot -proot lab -e "SELECT * FROM accounts;"

echo ""
echo "NOTE: Lost update and locking demonstrations require 2 interactive terminals."
echo "Open: docker exec -it mysql-primary mysql -uroot -proot lab"
echo "Follow SESSION A / SESSION B instructions in the README."

echo "=== Activity 4 setup complete ==="
