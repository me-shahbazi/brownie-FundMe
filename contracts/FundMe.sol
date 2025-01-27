// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

import {AggregatorV3Interface} from "@chainlink/contracts/src/v0.8/shared/interfaces/AggregatorV3Interface.sol";
// chainlink >> contracts >> Search: AggregatorV3Interface.sol

contract FundMe {
    
    address public owner;    
    mapping (address => uint256) public fundAmounts;
    address[] public donors;
    AggregatorV3Interface priceFeed;

    address btcusdSep = 0x1b44F3514812d835EB1BDB0acB33d3fA3351Ee43;
    address ethusdSep = 0x694AA1769357215DE4FAC081bf1f309aDC325306;
    address btcusdFuj = 0x31CF013A08c6Ac228C94551d535d5BAfE19c602a;
    address ethusdFuj = 0x86d67c3D38D2bCeE722E601025C25a575021c6EA;

    constructor(address _priceFeed_Address){
        owner = msg.sender;
        priceFeed = AggregatorV3Interface(_priceFeed_Address);
    }

    function fund() public payable {
        // 18 digit number to be compared with donated amount
        uint256 minimumUSD = 50 * 10**18; // 50$

        require(
            getConversionRate(msg.value) >= minimumUSD,
            "You need to spend more ETH!"
        );
        fundAmounts[msg.sender] += msg.value;
        donors.push(msg.sender);
    }

    function getConversionRate(uint256 ethAmount)
        public
        view
        returns (uint256)
    {
        uint256 ethPrice = getPrice();
        uint256 ethAmountInUsd = (ethPrice * ethAmount) / 1000000000000000000;
        // the actual ETH/USD conversation rate, after adjusting the extra 0s.
        return ethAmountInUsd;
    }

    function getPrice() public view returns (uint256) {
        (, int256 answer, , , ) = priceFeed.latestRoundData();
        // ETH/USD rate in 18 digit
        return uint256(answer * 10000000000);
    }
    
    function getBalance() public view returns (uint) {
    return address(this).balance;
    }

    modifier onlyRecipient {
        require(msg.sender == owner, "Not the contract's Recipient");
        _;
    }    

    function withdrawFunds() public onlyRecipient {
        payable(owner).transfer(address(this).balance);
        
        for (uint donorIndex=0; donorIndex < donors.length; donorIndex++) {
            fundAmounts[donors[donorIndex]] = 0;
            delete fundAmounts[donors[donorIndex]];
        }
        donors = new address[](0); // What does it mean?
    }

    function numDonors() public view returns (uint) { // actually number of Donations
        return donors.length;
    }
} 