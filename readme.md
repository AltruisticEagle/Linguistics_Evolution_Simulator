## Features
This is an attempt at representing linguistic evolution in a human civilisation! It evolves 20 words through 100-year iterations across a 3000 year interval (that being 30 iterations in this program).

The game loop is in main(); at the beginning, a "civilisation" is generated with random parameters related to geography so as to give it unique words for resources; this might also become a game mechanic in the future. Afterwards, a quantity of words "evolve" depending on the modifiers that randomly selected events produce.

With regards to the string of "plague" messages, this is to ensure that the population doesn't spiral out of control and lead to many word mutations all at once.


## AI use declaration
As I said in the project description, virtually none of the code had AI input; as far as I can remember, all the code was written myself, with AI only acting occasionally as a tool that I use for better-quality brainstorming and planning. 

However, there was one major task that I had to rely on AI for guidance, which is the publishing to PyPI step in preparation for shipping. I am personally very inexperienced with the whole project lifecycle, and especially shipping, so I had to rely on it to guide me through this process of packing everything in and replacing some file paths in the source code. In any case, this is good project experience and something that I learned! It is a somewhat difficult process for sure, in my experience.


## Installation
Install with pipx:

```bash
pipx install linguistics-evolution-simulator
```

Then run ```linguistics-sim```.

So far as I am aware some ship reviewers have had issues running this program on Windows, so you are advised to use Mac to run this project. 
