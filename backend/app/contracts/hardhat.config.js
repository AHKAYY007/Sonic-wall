require("dotenv").config();
require("@nomiclabs/hardhat-ethers");

module.exports = {
  solidity: "0.8.20",
  networks: {
    localhost: {
      url: "http://127.0.0.1:8545",
    },
    sonicblaze: {
      url: "https://rpc.blaze.soniclabs.com",
      chainId: 57054,
      accounts: [process.env.PRIVATE_KEY]
    },
    // Mainnet placeholder
    sonicmainnet: {
      url: "https://rpc.soniclabs.com", // Replace when available
      chainId: 12345, // Replace with mainnet ID
      accounts: [process.env.PRIVATE_KEY]
    }
  }
};
