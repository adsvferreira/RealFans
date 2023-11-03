// SPDX-License-Identifier: MIT
pragma solidity 0.8.21;

interface INFTGifts {
    function mintGift(address to, string calldata badgeURI) external payable;

    function addNewGiftURI(string memory badgeURI, uint256 ethValue) external;

    function getAllURIs() external view returns (string[] memory);

    function getTokenIdCounter() external view returns (uint256);

    function getEthBalanceOf(
        address account
    ) external view returns (uint256 ethBalanceOf);

    function getTotalEthBalance()
        external
        view
        returns (uint256 totalEthBalance);
}
