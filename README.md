<h1>ChessMate</h1>

<p>A chess program designed for a physical chessboard that uses reed switches to determine movement and LEDs to communicate computer movement.</p>
<p>Uses the <a href="https://stockfishchess.org/">Stockfish engine</a> to generate and validate moves, Stockfish is open source software that can be run on linux and more specifically the Raspberry Pi 3. I'm using the <a href="https://github.com/zhelyabuzhsky/stockfish">stockfish python package</a> to communicate between my program and the engine, this does not unfortunately support checking for check or stalemate so I will have to search for another module that take a board's current state and detect check or write my own.</p>
<p>I aim to develop a web application to go alongside this program</p>

<br>

<h2>main.py</h2>
<p>
Contains the main game logic for the chess program, it can:
<ul>
  <li>Start a game</li>
  <li>Detect player movement</li>
  <li>Generate moves for AI </li>
  <li>Check the physical board is set up correctly</li>
</ul>
</p>

<br>

<h2>charlieplexing.py</h2>
<p>
Called by the main program and contains functions to control the 16 LEDs via charlieplexing:
<ul>
  <li><b>turnOn</b> - Takes an int from 0-16 as a parameter and turns on the given LED, passing 0 turns off any currently on LED as it calls an unused GPIO configuration</li>
  <li><b>allFlash</b> - Flashes all LEDs three times</li>
  <li><b>slide</b> - Lights up each LED one at a time in order, takes speed parameter either "fast" or "slow"</li>
  <li><b>bounce</b> - Has the lights slide from one side to the other and goes in reverse once it reaches the end</li>
</ul>
</p>

<h2>TODO</h2>
<ul>
  <li>Prevent movement to same position - (completed)</li>
  <li>Flash LEDs when illegal move is made - (completed)</li>
  <li>Add promotion - (in progress)</li>
  <li>Add castling</li>
  <li>Add LCD functionality and buttons (new file to control LCD?)</li>
  <li>Add difficulty settings for AI</li>
  <li>Get program to understand when board is in check/checkmate/stalemate</li>
  <li>Make program run on boot</li>
</ul>
