let userWallet;

async function connectWallet() {
    if (window.ethereum) {
        try {
            const accounts = await window.ethereum.request({ method: 'eth_requestAccounts' });
            userWallet = accounts[0];
            document.getElementById("wallet-address").innerText = "Connected Wallet: " + userWallet;
        } catch (error) {
            console.error("User denied MetaMask connection");
        }
    } else {
        alert("Please install MetaMask!");
    }
}

async function submitVote(event) {
    event.preventDefault();
    const selected = document.querySelector('input[name="candidate"]:checked');
    if (!selected) {
        alert("Select a candidate first!");
        return;
    }

    const candidateId = selected.value;

    const provider = new ethers.providers.Web3Provider(window.ethereum);
    const signer = provider.getSigner();
    const contract = new ethers.Contract("0x5FbDB2315678afecb367f032d93F642f64180aa3", VotingABI, signer);

    const tx = await contract.vote(candidateId);
    await tx.wait();

    alert("Vote submitted successfully!");
}

async function fetchResults() {
    const response = await fetch('/results');
    const results = await response.json();
    const resultsList = document.getElementById('results');
    resultsList.innerHTML = '';
    results.forEach(candidate => {
        const li = document.createElement('li');
        li.innerText = `${candidate.name}: ${candidate.votes} votes`;
        resultsList.appendChild(li);
    });
}
