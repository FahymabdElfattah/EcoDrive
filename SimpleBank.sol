// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;
contract PenaltyContract {
    address public owner;
    address public companyAccount;
    uint256 public gasThreshold = 50;  // exemple de seuil arbitraire
    uint256 public penaltyAmount = 1 ether;  // montant de la pénalité, ici 1 Ether
    constructor(address _companyAccount) {
        owner = msg.sender;
        companyAccount = _companyAccount;
    }
    modifier onlyOwner() {
        require(msg.sender == owner, "Only owner can call this function.");
        _;
    }
    function setGasThreshold(uint256 _newThreshold) external onlyOwner {
        gasThreshold = _newThreshold;
    }
    function applyPenalty(uint256 gasValue) external onlyOwner {
        if (gasValue > gasThreshold) {
            require(address(this).balance >= penaltyAmount, "Contract balance is not sufficient.");
            payable(owner).transfer(penaltyAmount);
        }
    }
    // Fonction pour permettre à l'entreprise de déposer des Ether dans le contrat
    function deposit() external payable {
        require(msg.sender == companyAccount, "Only the company can deposit Ether.");
    }
    // Fonction pour consulter le solde du contrat
    function getBalance() external view returns (uint256) {
        return address(this).balance;
    }
}
