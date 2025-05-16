#!/bin/bash

set -e

# Config
VENV_DIR="venv"
BACKEND_DIR="backend"
CONTRACTS_DIR="contracts"
NETWORK="blazeTestnet"  # or blazeMainnet
TESTNET_ENV="$BACKEND_DIR/.env.testnet"
ACTIVE_ENV="$BACKEND_DIR/.env"

echo "🔧 Setting up Python virtual environment..."
if [ ! -d "$VENV_DIR" ]; then
    python3 -m venv $VENV_DIR
fi
source $VENV_DIR/bin/activate

echo "📦 Installing Python dependencies..."
pip install -r $BACKEND_DIR/requirements.txt

echo "📦 Installing Node.js dependencies..."
if [ ! -d "$CONTRACTS_DIR/node_modules" ]; then
    npm install --prefix $CONTRACTS_DIR
fi

echo "🔨 Compiling contracts for $NETWORK..."
npx hardhat compile --cwd $CONTRACTS_DIR

echo "🚀 Deploying smart contracts to $NETWORK..."
DEPLOY_OUTPUT=$(npx hardhat run scripts/deploy.js --network $NETWORK --cwd $CONTRACTS_DIR)
FIREWALL_ADDRESS=$(echo "$DEPLOY_OUTPUT" | grep "SonicFirewall deployed to:" | awk '{print $4}')
echo "✅ Contract deployed at $FIREWALL_ADDRESS"

# Prepare Blaze Testnet .env
echo "🌍 Writing .env for Sonic Blaze Testnet..."
cat > "$TESTNET_ENV" <<EOF
WEB3_PROVIDER_URL=https://rpc.blaze.soniclabs.com
FIREWALL_CONTRACT_ADDRESS=$FIREWALL_ADDRESS
ETHERSCAN_API_KEY=your_actual_api_key
SENTRY_DSN=
ENVIRONMENT=production
EOF

cp "$TESTNET_ENV" "$ACTIVE_ENV"

echo "🔥 Launching FastAPI backend in production mode..."
uvicorn $BACKEND_DIR.app.main:app --host 0.0.0.0 --port 8000
