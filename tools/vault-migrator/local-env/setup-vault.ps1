# Script to spin up Vault and inject a test secret

Write-Host "Starting Vault Docker container..." -ForegroundColor Cyan
docker-compose up -d

Write-Host "Waiting for Vault to initialize..." -ForegroundColor Yellow
Start-Sleep -Seconds 5

Write-Host "Injecting test secret into Vault at path 'secret/data/my-app'..." -ForegroundColor Cyan

# We use docker exec to run the vault command directly inside the container!
# This means you don't even need the vault CLI installed on your host Windows machine.
docker exec -e VAULT_TOKEN="test-root-token" -e VAULT_ADDR="http://127.0.0.1:8200" vault-dev vault kv put secret/data/my-app password="HelloFromDockerVault!"

Write-Host "`nVault is ready for testing!" -ForegroundColor Green
Write-Host "--------------------------------"
Write-Host "VAULT_ADDR:  http://127.0.0.1:8200"
Write-Host "VAULT_TOKEN: test-root-token"
Write-Host "VAULT_PATH:  secret/data/my-app"
Write-Host "--------------------------------"
