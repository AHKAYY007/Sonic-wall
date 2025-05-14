# 🔥 Sonic Wallet Firewall

A FastAPI + Solidity-based wallet firewall to protect users on the Sonic Network. It checks if a transaction is going to a blacklisted address using a smart contract and provides API access for real-time firewall validation.

---

## 📦 Requirements

- Python 3.8+
- Node.js + Hardhat (for smart contract compilation/deployment)
- Sonic-compatible EVM RPC (e.g. `https://rpc.sonic.xyz`)
- Optional: Prometheus, Grafana, and Sentry for observability
- MetaMask or other Web3 wallet for deploying contracts

---

## 🚀 Getting Started

### 1. Clone and Navigate

```bash
git clone https://github.com/your-org/sonic-wallet-firewall.git
cd sonic-wallet-firewall/backend

python3 -m venv env
source env/bin/activate
pip install -r requirements.txt

### 3. Paste this template into a .env file in your backend folder:

# Required
SONIC_RPC_URL=https://rpc.sonic.xyz
FIREWALL_CONTRACT_ADDRESS=0xYourDeployedContract

# Optional
PRIVATE_KEY=0xYourPrivateKey               # Only needed if sending signed txs
SENTRY_DSN=https://your-sentry-dsn         # Optional: Sentry for logging
ENVIRONMENT=development                    # Set to production/staging as needed



### 4.  Run the FastAPI App

uvicorn app.main:app --reload


# Smart contract
### 1. Install Node.js dependencies
npm install

### 2 . Compile
npx hardhat compile

### 3 . Deploy to Sonic Network
npx hardhat run scripts/deploy.js --network sonic

### 4 . Copy the deployed contract address into .env:
FIREWALL_CONTRACT_ADDRESS=0xYourContractAddress





🐳 Coming Soon
Docker & docker-compose support

CI/CD GitHub Actions pipeline

Frontend dashboard for managing blacklist




