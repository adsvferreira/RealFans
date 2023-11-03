// SPDX-License-Identifier: MIT
pragma solidity 0.8.21;

import "@openzeppelin/contracts/utils/Strings.sol";
import "@openzeppelin/contracts/access/Ownable.sol";
import {INFTGifts} from "../interfaces/INFTGifts.sol";
import "@openzeppelin/contracts/token/ERC721/ERC721.sol";
import {CommunityVault, IERC20} from "./CommunityVault.sol";
import "@openzeppelin/contracts/token/ERC721/extensions/ERC721URIStorage.sol";
import {SafeERC20} from "@openzeppelin/contracts/token/ERC20/utils/SafeERC20.sol";

contract NFTGifts is ERC721, ERC721URIStorage, Ownable, INFTGifts {
    using Strings for string;
    using SafeERC20 for IERC20;

    // TODO:
    // min/redeem by handle

    CommunityVault communityVault;
    string[] private _giftURIs;
    uint256 private _tokenIdCounter;
    address[] private _donators;
    address[] private _receivers;

    mapping(uint256 => bool) private _isRedeemed;
    mapping(string => uint256) private _totalGiftQty;
    mapping(string => uint256) private _ethValuePerGiftURI;
    mapping(address => mapping(string => uint256)) private _GiftQtyPerAddress;
    mapping(address => mapping(string => uint256))
        private _DonatedQtyPerAddress;

    event Donation(
        address indexed donator,
        address indexed receiver,
        string giftURI,
        uint256 ethValue
    );

    event Redemption(
        address indexed receiver,
        string giftURI,
        uint256 ethValue
    );

    constructor(
        address _vaultAddress
    ) ERC721("NFTGifts", "NFTG") Ownable(msg.sender) {
        communityVault = CommunityVault(_vaultAddress);
    }

    function mintGift(
        address to,
        string calldata giftURI
    ) external payable onlyOwner {
        require(_isGiftURIWhitelisted(giftURI), "tokenURI noy whitelisted yet");
        uint256 newTokenIdCounter = _tokenIdCounter + 1;
        uint256 ethValue = _ethValuePerGiftURI[giftURI];
        address depositAsset = communityVault.asset();
        _receivers.push(to);
        _donators.push(msg.sender);
        _isRedeemed[newTokenIdCounter] = false;
        _tokenIdCounter = newTokenIdCounter;
        ++_totalGiftQty[giftURI];
        ++_GiftQtyPerAddress[to][giftURI];
        _safeMint(to, newTokenIdCounter);
        _setTokenURI(newTokenIdCounter, giftURI);
        SafeERC20.safeTransferFrom(
            IERC20(depositAsset),
            msg.sender,
            address(this),
            ethValue
        );
        IERC20(depositAsset).approve(address(communityVault), ethValue);
        communityVault.deposit(ethValue, address(this));
        emit Donation(msg.sender, to, giftURI, ethValue);
    }

    function addNewGiftURI(
        string memory giftURI,
        uint256 ethValue
    ) external onlyOwner {
        require(
            !_isGiftURIWhitelisted(giftURI),
            "tokenURI already whitelisted"
        );
        _giftURIs.push(giftURI);
        _ethValuePerGiftURI[giftURI] = ethValue;
    }

    function redeemDonation(uint256 tokenId) external {
        require(msg.sender == ownerOf(tokenId));
        string memory giftTokenURI = tokenURI(tokenId);
        uint256 ethValue = _ethValuePerGiftURI[giftTokenURI];
        _isRedeemed[tokenId] = true;
        communityVault.withdraw(ethValue, msg.sender, address(this));
        emit Redemption(msg.sender, giftTokenURI, ethValue);
    }

    function isRedeemed(uint256 tokenId) external view returns (bool) {
        return _isRedeemed[tokenId];
    }

    function _isGiftURIWhitelisted(
        string memory giftURI
    ) private returns (bool) {
        string[] memory giftURIs = _giftURIs;
        uint256 giftURIsLength = giftURIs.length;
        for (uint256 i = 0; i < giftURIsLength; ) {
            if (giftURI.equal(giftURIs[i])) {
                return true;
            }
            unchecked {
                ++i;
            }
        }
        return false;
    }

    function getAllURIs() external view returns (string[] memory) {
        return _giftURIs;
    }

    function getTokenIdCounter() external view returns (uint256) {
        return _tokenIdCounter;
    }

    function getEthValueOfGift(
        string memory giftURI
    ) public view returns (uint256 ethValue) {
        ethValue = _ethValuePerGiftURI[giftURI];
    }

    function getTotalQtyOfGift(
        string memory giftURI
    ) public view returns (uint256 totalSupply) {
        totalSupply = _totalGiftQty[giftURI];
    }

    function getGiftQtyOf(
        address account,
        string memory giftURI
    ) public view returns (uint256 giftQtyOf) {
        giftQtyOf = _GiftQtyPerAddress[account][giftURI];
    }

    function getEthBalanceOfPerGift(
        address account,
        string memory giftURI
    ) public view returns (uint256 ethBalanceOfPerGift) {
        ethBalanceOfPerGift =
            getGiftQtyOf(account, giftURI) *
            getEthValueOfGift(giftURI);
    }

    function getEthBalanceOf(
        address account
    ) external view returns (uint256 ethBalanceOf) {
        string[] memory giftURIs = _giftURIs;
        uint256 giftURIsLength = giftURIs.length;
        for (uint256 i = 0; i < giftURIsLength; ) {
            ethBalanceOf += getEthBalanceOfPerGift(account, giftURIs[i]);
            unchecked {
                ++i;
            }
        }
    }

    function getTotalEthBalance()
        external
        view
        returns (uint256 totalEthBalance)
    {
        string[] memory giftURIs = _giftURIs;
        uint256 giftURIsLength = giftURIs.length;
        for (uint256 i = 0; i < giftURIsLength; ) {
            totalEthBalance +=
                getTotalQtyOfGift(giftURIs[i]) *
                getEthValueOfGift(giftURIs[i]);
            unchecked {
                ++i;
            }
        }
    }

    function getAllDonators() external view returns (address[] memory) {
        return _donators;
    }

    function getAllReceivers() external view returns (address[] memory) {
        return _receivers;
    }

    // The following functions are overrides required by Solidity:

    /**
     * @dev See {IERC165-supportsInterface}.
     */
    function supportsInterface(
        bytes4 interfaceId
    ) public view override(ERC721, ERC721URIStorage) returns (bool) {
        return
            interfaceId == type(IERC721).interfaceId ||
            interfaceId == type(IERC721Metadata).interfaceId ||
            super.supportsInterface(interfaceId);
    }

    function tokenURI(
        uint256 tokenId
    ) public view override(ERC721, ERC721URIStorage) returns (string memory) {
        return super.tokenURI(tokenId);
    }
}
