from flask import Flask, render_template, request, jsonify, redirect, url_for
from web3 import Web3
import json

app = Flask(__name__)

# ---------------- Blockchain Connection ----------------
ganache_url = "http://127.0.0.1:7545"   # Ganache RPC URL
web3 = Web3(Web3.HTTPProvider(ganache_url))

# Load ABI
with open('VotingABI.json') as f:
    contract_abi = json.load(f)

# Deployed contract address (replace with your deployed address)
contract_address = web3.to_checksum_address("0x5FbDB2315678afecb367f032d93F642f64180aa3")

# Load contract
contract = web3.eth.contract(address=contract_address, abi=contract_abi)

# ---------------- Local Data Stores ----------------
voter_list = []
candidate_list = []
admin_list = []

# ---------------- Home ----------------
@app.route("/")
def index():
    return render_template("index.html")

# ---------------- Login Pages ----------------
@app.route("/login/user")
def login_user_page():
    return render_template("login_user_page.html")

@app.route("/login/org")
def login_org_page():
    return render_template("login_org_page.html")

@app.route("/login/admin")
def login_admin_page():
    return render_template("login_admin_page.html")

# ---------------- Dashboards ----------------
@app.route("/dashboard/voter")
def voter_dashboard():
    return render_template("voter_dashboard.html")

@app.route("/dashboard/org")
def org_dashboard():
    return render_template("org_dashboard.html")

@app.route("/dashboard/admin")
def admin_dashboard():
    return render_template("admin_dashboard.html")

# ---------------- Applications ----------------
@app.route("/elections")
def elections():
    return render_template("elections.html")

@app.route("/elections_voter")
def elections_voter():
    return render_template("elections_voter.html")



@app.route("/complaints")
def complaints():
    return render_template("complaints.html")

@app.route("/welcome")
def welcome():
    return render_template("welcome.html")

# ---------------- Voter Login ----------------
@app.route("/login_voter", methods=["GET", "POST"])
def login_voter_action():
    if request.method == "POST":
        name = request.form.get("name")
        if name:
            voter_list.append(name)   # Add voter to list
        return redirect(url_for("voter_list_page"))
    return render_template("login_voter.html")

@app.route("/voter_list_page")
def voter_list_page():
    return render_template("voter_list_page.html", voters=voters)

@app.route("/delete_voter/<int:voter_id>")
def delete_voter(voter_id):
    global voters
    voters = [v for v in voters if v["id"] != voter_id]  
    return redirect(url_for("voter_list_page"))

voters = [
    {"id": 1, "name": "Swarupa", "email": "swarupa@gmail.com", "status": "Active"},
    {"id": 2, "name": "Aditya", "email": "aditya@gmail.com", "status": "Inactive"},
    {"id": 3, "name": "Divya", "email": "divya@gmail.com", "status": "Active"},
]



# ---------------- Organisation Login ----------------
@app.route("/login_org_action", methods=["GET", "POST"])
def login_org_action():
    if request.method == "POST":
        name = request.form.get("name")
        if name:
            candidate_list.append(name)  
        return redirect(url_for("candidate_list_page"))
    return render_template("login_org.html")

@app.route("/candidate_list")
def candidate_list_page():
    return render_template("candidate_list_page.html", candidates=candidate_list)

# ---------------- Admin Login ----------------
@app.route("/login_admin_action", methods=["GET", "POST"])
def login_admin_action():
    if request.method == "POST":
        admin_id = request.form.get("admin_id")
        if admin_id:
            admin_list.append(admin_id)
        return redirect(url_for("admin_dashboard_page"))
    return render_template("login_admin.html")

@app.route("/admin_dashboard_page")
def admin_dashboard_page():
    return render_template("admin_dashboard.html", admins=admin_list)

# ---------------- Cast Vote ----------------
@app.route('/cast_vote', methods=['POST'])
def cast_vote():
    try:
        candidate_id = int(request.form['candidate_id'])
        account = web3.eth.accounts[0]   # First Ganache account

        # Send transaction to contract
        tx_hash = contract.functions.vote(candidate_id).transact({'from': account})
        receipt = web3.eth.wait_for_transaction_receipt(tx_hash)

        return jsonify({
            "status": "success",
            "tx_hash": receipt.transactionHash.hex()
        })
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)})


# ---------------- View Results ----------------
@app.route("/admin_results")
def admin_results():
    # Dummy data (later tum DB se laa sakte ho)
    results = [
        {"name": "MILLER / D", "votes": 522, "percent": 45.55},
        {"name": "WILLIAMS / D", "votes": 387, "percent": 33.77},
        {"name": "JONES / D", "votes": 174, "percent": 15.18},
        {"name": "COOK / D", "votes": 40, "percent": 3.49},
        {"name": "BUTTS JR. / D", "votes": 23, "percent": 2.01},
    ]
    return render_template("admin_results.html", results=results)

@app.route("/org_results")
def org_results():
    # Dummy data (later tum DB se laa sakte ho)
    results = [
        {"name": "MILLER / D", "votes": 522, "percent": 45.55},
        {"name": "WILLIAMS / D", "votes": 387, "percent": 33.77},
        {"name": "JONES / D", "votes": 174, "percent": 15.18},
        {"name": "COOK / D", "votes": 40, "percent": 3.49},
        {"name": "BUTTS JR. / D", "votes": 23, "percent": 2.01},
    ]
    return render_template("org_results.html", results=results)

# ---------- Board of Directors Election ----------
@app.route("/vote_now")
def vote_now ():
    return render_template("vote_now.html")


# ---------------- Run Flask ----------------
if __name__ == '__main__':
    app.run(debug=True)
