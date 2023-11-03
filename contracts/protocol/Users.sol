// SPDX-License-Identifier: MIT
pragma solidity 0.8.21;

import {IUsers} from "../interfaces/IUsers.sol";
import {Ownable} from "@openzeppelin/contracts/access/Ownable.sol";

error AlreadyAssociatedAddress(address address_);
error AlreadyAddociatedTwitterHandle(string twitterHandle_);

contract Users is Ownable, IUsers {
    mapping(string twitterHandle_ => address address_) private _getAddress;
    mapping(address address_ => string twitterHandle_) private _getTwitter;

    constructor() Ownable(msg.sender) {}

    function getAddressFromTwitterHandle(
        string calldata handle_
    ) external view returns (address) {
        return _getAddress[handle_];
    }

    function getTwitterHandleFromAddress(
        address address_
    ) external view returns (string memory) {
        return _getTwitter[address_];
    }

    function writeTwitterHandle(
        address address_,
        string calldata twitterHandle_
    ) external onlyOwner returns (bool) {
        if (
            keccak256(abi.encodePacked(_getTwitter[address_])) !=
            keccak256(abi.encodePacked(""))
        ) {
            revert AlreadyAssociatedAddress(address_);
        }
        if (_getAddress[twitterHandle_] != address(0)) {
            revert AlreadyAddociatedTwitterHandle(twitterHandle_);
        }
        _getAddress[twitterHandle_] = address_;
        _getTwitter[address_] = twitterHandle_;
        return true;
    }
}
