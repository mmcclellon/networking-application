# networking-application
<h1>SOLD! – Online Auction House</h1>

<h3>Roles and Responsibilities</h3>

**Vedaant:** Project Manager / Documentation / Developer
- Keep track of project deadlines and requirements. Coordinate group meetings and make sure tasks are being completed. Maintain the team contract and project documentation. Help in development also.\

**Mahin:**
- Develop the auction server and core server-side. Handle user ​​​connections, bids, and auction logic. Make sure the server correctly ​​​determines and records the highest bidder.

**Mckenzee:**
- Design and maintain the database structure. Manage user, auction, ​​​and bid information. Ensure bids and auction data are stored ​​​​correctly. Help test data consistency and database functionality.

**Terrance:**
- Develop the client interface and user interactions. Implement ​​​features for viewing auctions and submitting bids. Test the system ​​​from a user's perspective. Identify bugs and work with the other ​​members to fix them.

<h3>Project Description</h3>
SOLD! is an online auction house server that allows users to create auctions, view available items, and place bids against other users. The server will manage multiple auctions and process bids in real time, keeping track of the current highest bidder. When an auction ends, the server will determine the winning bidder based on the highest valid bid. The system will also manage user accounts, auction information, and bid history. The users will create and login with a username and password, username will be displayed to other users. The server will also have a timeout detection feature where if a user has bid for a certain amount of time they will be kicked out of the server.

<h3>Planned Features</h3>

* User registration and login
* Auction creation and browsing
* Real-time bidding
* Tracking of highest valid bids
* Auction results and bid history
* User, auction, and bid data management
* User timeout detection

<h3>Main Conflict Resolution</h3>
Online auctions require a reliable system to manage multiple users placing bids at the same time. Our project will address this by creating a server that can receive and process bids, determine the highest valid bid, and prevent issues such as incorrect bid information or multiple users being recorded as the winner. The system will provide an organized way to manage auctions and their results.

<h3>Targeted Users</h3>
University of Memphis students that are interested in buying or selling items through an online auction platform. Sellers will be able to create auctions and provide information about their items, while buyers can browse auctions and compete with other users by placing bids. The system is designed for users who want a simple way to participate in auctions without needing to manage the bidding process themselves.


<h3>How to Run</h3>

**Requirements:** Python 3.8 or newer. No extra packages are needed. Run every command from the project's root folder.

**1. Start the server (server machine)**
```
python -m server.server
```
- `python server/server.py` does not work. The server imports from the `database` package, so it must be started with `-m` from the root folder.
- The accounts database `database/sold.db` is created automatically the first time the server runs.
- Find the server's IP address with `ipconfig` (Windows) or `ip a` (Mac/Linux).
- If the firewall asks, allow Python on private networks (port **5001**).

**2. Start a client (on a different machine on the same network)**
1. Open `client/client.py` and set `HOST` to the server's IP address, e.g. `HOST = '192.168.1.25'`
2. Run:
```
python -m client.client
```
Start more clients on other machines to test multiple users at once.

**3. Client commands**

| Command | What it does |
|---|---|
| `REGISTER` | Create an account. Username: 3–20 letters, digits or `_`. Password: 8–128 characters. |
| `LOGIN` | Log in. The password is hidden while typing. |
| `PING` | Check the connection. The client also sends a heartbeat automatically every 10 seconds. |
| `LOGOUT` | Log out and disconnect. |
| `QUIT` | Close the client. |

All commands except `REGISTER`, `LOGIN` and `PING` require logging in first.

**Auction interface prototype**
`auction_interface.py` previews the auction menu (view auctions, place bids, refresh) using sample data. It is not connected to the server yet. Run it with `python auction_interface.py`.
