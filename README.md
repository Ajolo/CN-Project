# CSC 4750 Final Project 

## Project Name:
Cash Grab!

## Objective:
This will be a simple and familiar multiplayer CLI mind game. The objective is to have the most amount of money by the end of the game, with the “pot” of money available for anyone to take during a turn. The constraints of this game are that if all users decide to take the money from the pot, no one gets money. This will involve discussion and strategy among players, and may involve deceit in order for a user to get ahead (specifics regarding rules and allowed ‘moves’ are still to be decided).
Tech -- This game will require an instance of a server to handle multiple connections, and will leverage the chat application examples we had covered previously this quarter, using Python and TCP. Because clients should be able to connect from individual laptops/clients, this app will more than likely be hosted on the luke.cs.spu.edu server and will need to differentiate clients based on IP. Another aspect to add small complications to the game will be an in game timer, with the intention of encouraging decisions in a timely manner, requiring additional information to be sync’d between all clients and would introduce ‘real-time’ consequences. For players that may not be able to play directly with one another in person, there should also be a chat option that is broadcast to all clients connected so that gameplay and coordination is still possible. 

## How To Install:
This application requires Python 3.X and was tested on MacOS Mojave as well as the leia.cs.spu.edu SPU linux server. 

## How To Run:
Multiple clients are able to be handled with this application. On the desired server (leia.cs.spu.edu recommended), you may start the server by running:
> python3 server.py 4002

The third command line argument being the TCP port of choice. 

The client application may be run by using the following command:
>python3 client.py leia.cs.spu.edu 4002

With the 3 argument being the server FQDN from where the server is running, and the same corresponding port. 

## How To Use:
On launch, the user may be prompted with a suggested /help command, which prints a few of the more important commands that the user may find helpful in using this application. Content typed into the chat that is not prepended with a '/' character will be read directly into the chat, and broadcasted to all connected clients. 

## Timeline: 
Week 1: Have framework (or working) TCP server / clients that represent something like what the final product would look like. Ensure that multiple clients are able to connect via IP to the Luke server and these are properly differentiated. 

Week 2: Finish up progress from previous week and begin implementing game logic to clients and server

Week 3: Finish up game logic, make improvements to gameplay so that it’s actually somewhat fun (hopefully)

Week 4: Bug testing, exception handling, generally make the connections as ‘robust’ as time allows






