# Activity 1 - Start Docker topology (PowerShell)

Write-Host "=== Activity 1: Starting Docker topology ===" -ForegroundColor Cyan
Write-Host "Starting 3 MySQL containers: primary, replica, shard2"

Set-Location 
docker compose up -d

Write-Host ""
Write-Host "Waiting 15 seconds for containers to initialize..."
Start-Sleep -Seconds 15

Write-Host ""
Write-Host "=== Container status ===" -ForegroundColor Cyan
docker ps

Write-Host ""
Write-Host "=== Verifying each node accepts connections ===" -ForegroundColor Cyan
Write-Host "Pinging mysql-primary..."
docker exec mysql-primary mysqladmin ping -uroot -proot

Write-Host "Pinging mysql-replica..."
docker exec mysql-replica mysqladmin ping -uroot -proot

Write-Host "Pinging mysql-shard2..."
docker exec mysql-shard2 mysqladmin ping -uroot -proot

Write-Host ""
Write-Host "=== Activity 1 complete ===" -ForegroundColor Green
