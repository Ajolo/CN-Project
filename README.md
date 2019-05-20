Project Description:
Name -- Money Grab!
Objective -- This will be a simple and familiar multiplayer CLI mind game. The objective is to have the most amount of money by the end of the game, with the “pot” of money available for anyone to take during a turn. The constraints of this game are that if all users decide to take the money from the pot, no one gets money. This will involve discussion and strategy among players, and may involve deceit in order for a user to get ahead (specifics regarding rules and allowed ‘moves’ are still to be decided).
Tech -- This game will require an instance of a server to handle multiple connections, and will leverage the chat application examples we had covered previously this quarter, using Python and TCP. Because clients should be able to connect from individual laptops/clients, this app will more than likely be hosted on the luke.cs.spu.edu server and will need to differentiate clients based on IP. Another aspect to add small complications to the game will be an in game timer, with the intention of encouraging decisions in a timely manner, requiring additional information to be sync’d between all clients and would introduce ‘real-time’ consequences. For players that may not be able to play directly with one another in person, there should also be a chat option that is broadcast to all clients connected so that gameplay and coordination is still possible. 

Timeline: 
Week 1: Have framework (or working) TCP server / clients that represent something like what the final product would look like. Ensure that multiple clients are able to connect via IP to the Luke server and these are properly differentiated. 

Week 2: Finish up progress from previous week and begin implementing game logic to clients and server

Week 3: Finish up game logic, make improvements to gameplay so that it’s actually somewhat fun (hopefully)

Week 4: Bug testing, exception handling, generally make the connections as ‘robust’ as time allows






