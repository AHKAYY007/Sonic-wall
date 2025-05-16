#!/bin/bash

set -e

# Paths
VENV_DIR="venv"
BACKEND_DIR="backend"
CONTRACTS_DIR="contracts"
HARDHAT_PORT=8545
LOCAL_ENV="$BACKEND_DIR/.env.local"
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

echo "🔨 Compiling smart contracts..."
npx hardhat compile --cwd $CONTRACTS_DIR

echo "🚀 Launching local Hardhat node..."
npx hardhat node --cwd $CONTRACTS_DIR > hardhat.log 2>&1 &
HARDHAT_PID=$!
sleep 3

echo "📡 Deploying smart contracts to local network..."
DEPLOY_OUTPUT=$(npx hardhat run scripts/deploy.js --network localhost --cwd $CONTRACTS_DIR)
FIREWALL_ADDRESS=$(echo "$DEPLOY_OUTPUT" | grep "SonicFirewall deployed to:" | awk '{print $4}')

echo "✅ Contract deployed at $FIREWALL_ADDRESS"

# Prepare local .env and copy to active
echo "🌍 Setting environment variables for local use..."
cat > "$LOCAL_ENV" <<EOF
WEB3_PROVIDER_URL=http://127.0.0.1:$HARDHAT_PORT
FIREWALL_CONTRACT_ADDRESS=$FIREWALL_ADDRESS
ETHERSCAN_API_KEY=dummy_local_key
SENTRY_DSN=
ENVIRONMENT=development
EOF

cp "$LOCAL_ENV" "$ACTIVE_ENV"

echo "🧪 Running unit tests..."
pytest $BACKEND_DIR/tests

echo "🔥 Starting FastAPI backend on http://localhost:8000 ..."
uvicorn $BACKEND_DIR.app.main:app --reload

# Cleanup on exit
trap "echo '🧹 Killing Hardhat node...'; kill $HARDHAT_PID" EXIT
echo "🧹 Cleaning up..."