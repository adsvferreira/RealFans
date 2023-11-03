// SPDX-License-Identifier: MIT
pragma solidity 0.8.21;

import "@openzeppelin/contracts/utils/Strings.sol";
import "@openzeppelin/contracts/access/Ownable.sol";
import "@openzeppelin/contracts/token/ERC721/ERC721.sol";
import {INFTGifts} from "../interfaces/INFTGifts.sol";
import "@openzeppelin/contracts/token/ERC721/extensions/ERC721URIStorage.sol";

contract NFTGifts is ERC721, ERC721URIStorage, Ownable, INFTGifts {
    using Strings for string;

    string[] private _giftURIs;
    uint256 private _tokenIdCounter;

    mapping(string => uint256) private _totalGiftQty;
    mapping(string => uint256) private _ethValuePerGiftURI;
    mapping(address => mapping(string => uint256)) private _GiftQtyPerAddress;

    constructor() ERC721("NFTGifts", "NFTG") Ownable(msg.sender) {}

    function mintGift(
        address to,
        string calldata giftURI
    ) external payable onlyOwner {
        require(_isGiftURIWhitelisted(giftURI), "tokenURI noy whitelisted yet");
        uint256 tokenIdCounter = _tokenIdCounter + 1;
        _safeMint(to, tokenIdCounter);
        _setTokenURI(tokenIdCounter, giftURI);
        // TODO: send eth to community pool
        _tokenIdCounter = tokenIdCounter;
        ++_totalGiftQty[giftURI];
        ++_GiftQtyPerAddress[to][giftURI];
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
