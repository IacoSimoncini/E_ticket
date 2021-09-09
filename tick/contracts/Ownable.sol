// SPDX-License-Identifier: GPL-3.0
pragma solidity >0.5.0;

contract Ownable {
    address public owner;
    
    event OwnershipTransferred(address indexed previousOwner, address indexed nerOwner);
    
    constructor() {
        owner = msg.sender;
    }
    
    modifier onlyOwner() {
        require(msg.sender == owner);
        _;
    }
    
    function transferOwnership(address newOwner) public onlyOwner returns(bool) {
        require(newOwner != address(0));
        emit OwnershipTransferred(owner, newOwner);
        owner = newOwner;
        return true;
    }
}