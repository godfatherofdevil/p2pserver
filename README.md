# P2P Server

the sole purpose of this point to point server is to enable two parties (host, guest) to exchange
their public addresses which can be used by them to negotiate and establish a point to point connection.

this server is based on REST and hence it is clients responsibility to poll the server and get status updates
for this purpose, the server exposes two endpoints- 
1. _**/games/poll**_ - this is meant to be used by host who wishes to host and 
have already registered a game session with the server   

`request model:
    {
    "name": <game_name>,
    "peerId": <peerId>,
    "addresses": <host_candidate_addresses>,
    }
`
2. _**/games/start**_ - this is meant to be used by the guest who wishes to join 
one of the existing game session already registered.   

`request model:
    {
    "name": <game_name>,
    "peerId": <peerId>,
    "addresses": <guest_candidate_addresses>,
    }`
    
    
3. _**/games/register**_ - this is meant to be used by host of a game session to register a game   
`request model:
    {
    "name" : <game_name>,
    "peerId: <peer_id>
    }`    
    
4. _**/games**_ - this endpoint give a guest list of all available game sessions
this endpoint does not take any payload or query parameters

5. /games/<name_of_game>   - this is meant to be used for maintenance operation 
such updating name of games, deleting games etc.
 
 ## assumptions:
 hosts have one to many mapping to guests - 
 one client can host a game session and more than one clients can try to connect to this game session
 
 both hosts and guests have http clients on their side.
 both hosts and guests are behind some kind of NAT or firewall and can use some sort of STUN server
 to get their public ip addresses.
 p2p server doesn't try to make the connection b/w the hosts and guest but rather it merely facilitates
 a mechanism to supply the public address to each other (guest address to host, host addresses to guest)
 
 once both host and guest get the candidate addresses for each other they are capable enough to negotiate a connection.
 basically, this step involves lot of steps including the hole punching step - didn't had enough time to implement
 
 
 ## build and run instruction:
 1. p2pserver 
 build the docker image - `docker build . -t p2pserver -f Dockerfile`
 run the server - `docker run --rm -p 8000:8000 --name p2pserver`
 
 2. there are two files to simulate host and guest behavior - 
 simulate_hosts.py, simulate_guest.py   
 
 to run both of these, API should already be running and python should be installed,  
 after that following instructions apply.   
 a. create virtual env -  `python -m venv .venv`   
 b. activate virtual env - `source .venv/bin/activate`    
 c. install dependencies - `pip install -r requirements.txt`   
 
 after this open one more terminal and just activate the virtual env - 
 this is required because we need two processes to simulate hosts and guests   
 
 `python simulate_hosts.py`  -> in one terminal   
 `python simulate_guest.py`  -> in another terminal
 

 
    
 


