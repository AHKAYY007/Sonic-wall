// SPDX-License-Identifier: MIT
pragma solidity ^0.8.19;

interface ISonicFirewall {
    function isBlocked(address target) external view returns (bool);
}

interface IERC20 {
    function transfer(address to, uint256 amount) external returns (bool);
}

contract SonicSafeTransfer {
    address public owner;
    ISonicFirewall public firewall;

    event SafeETHTransfer(address indexed from, address indexed to, uint256 amount);
    event SafeTokenTransfer(address indexed from, address indexed to, address token, uint256 amount);
    event TransferBlocked(address indexed from, address indexed to);

    modifier onlyOwner() {
        require(msg.sender == owner, "Not authorized");
        _;
    }

    constructor(address firewallAddress) {
        owner = msg.sender;
        firewall = ISonicFirewall(firewallAddress);
    }

    receive() external payable {}

    function sendETH(address payable to, uint256 amount) external onlyOwner {
        require(address(this).balance >= amount, "Insufficient ETH");
        if (firewall.isBlocked(to)) {
            emit TransferBlocked(msg.sender, to);
            revert("Recipient is blacklisted");
        }

        (bool success, ) = to.call{value: amount}("");
        require(success, "ETH Transfer failed");
        emit SafeETHTransfer(msg.sender, to, amount);
    }

    function sendToken(address token, address to, uint256 amount) external onlyOwner {
        if (firewall.isBlocked(to)) {
            emit TransferBlocked(msg.sender, to);
            revert("Recipient is blacklisted");
        }

        bool sent = IERC20(token).transfer(to, amount);
        require(sent, "Token transfer failed");
        emit SafeTokenTransfer(msg.sender, to, token, amount);
    }

    function setFirewall(address newFirewall) external onlyOwner {
        firewall = ISonicFirewall(newFirewall);
    }

    function getBalance() external view returns (uint256) {
        return address(this).balance;
    }
}
