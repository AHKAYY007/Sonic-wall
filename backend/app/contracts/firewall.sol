// SPDX-License-Identifier: MIT
pragma solidity ^0.8.19;

contract SonicFirewall {
    address public owner;
    mapping(address => bool) public blacklist;

    event Blacklisted(address indexed malicious);
    event RemovedFromBlacklist(address indexed addr);

    modifier onlyOwner() {
        require(msg.sender == owner, "Not authorized");
        _;
    }

    constructor() {
        owner = msg.sender;
    }

    function addToBlacklist(address malicious) public onlyOwner {
        require(!blacklist[malicious], "Already blacklisted");
        blacklist[malicious] = true;
        emit Blacklisted(malicious);
    }

    function removeFromBlacklist(address addr) public onlyOwner {
        require(blacklist[addr], "Not blacklisted");
        blacklist[addr] = false;
        emit RemovedFromBlacklist(addr);
    }

    function isBlocked(address target) public view returns (bool) {
        return blacklist[target];
    }
}
