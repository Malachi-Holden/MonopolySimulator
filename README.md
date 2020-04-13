# Monopoly Tile Frequency Model

This is an accurate model for estimating the frequency of landing on each tile on a monopoly board. Plays a game by rolling a pair of virtual dice and moving a player around a virtual monopoly board, counting how many times each square is landed on. Takes into account all aspects of the game that affect player movement, such as jail. Does not take money or player competition into account.

It is not necessary to use multiple players, since players don't have any affect on each other's movement. It is equivalent to play multiple games with one player.


## Results
These are the results after running 1000 games of 1000000 moves each. Real games may differ because of random variations in dice rolls, especially since real games play fewer rounds than 1000000. However these are close to the expected results over a large number of games

```
Go is on the top left
|2.9235%|2.0201%|2.0376%|2.0481%|2.2062%|2.8006%|2.1402%|2.1825%|2.1961%|2.1751%|2.1501%|
|2.4859%|                                                                       |2.5554%|
|2.0617%|                                                                       |2.4637%|
|2.0709%|                                                                       |2.2461%|
|2.1855%|                                                                       |2.3316%|
|2.3014%|                                                                       |2.7639%|
|2.3672%|                                                                       |2.6388%|
|2.5577%|                                                                       |2.8084%|
|2.4843%|                                                                       |2.7765%|
|2.5330%|                                                                       |2.9225%|
|3.7519%|2.4472%|2.6550%|2.5348%|2.5601%|2.8995%|3.0126%|2.5894%|2.6426%|2.6828%|2.7281%|

brown: 4.0681%. Average: 2.0341%
light blue: 6.5114%. Average: 2.1705%
pink: 7.1331%. Average: 2.3777%
orange: 8.3378%. Average: 2.7793%
red: 8.2849%. Average: 2.7616%
yellow: 7.5420%. Average: 2.5140%
green: 7.3845%. Average: 2.4615%
dark blue: 4.5567%. Average: 2.2784%
railroads: 10.7654%. Average: 2.6913%
utilities: 5.1187%. Average: 2.5593%
```
### How to read the results
The table of percentages is a representation of a monopoly board, with go on the top left and preceeding clockwise. So 'Jail' is on the top right, 'Free Parking' on the bottom right, and 'Go to Jail' on the bottom left. Each number represents the percentage of hits that tile got out of all the tiles landed on. So if a player made 100 moves, and free parking was landed on 7 times, the bottom right corner would say 7.0000%. Adding up all the tiles should result in 100%, although this may be slightly different because of rounding errors.

The list of colors below just recombines the data from the table and organizes it by monopoly. This information might be useful when deciding whether to make a trade.

## Interpretation

You might be surprised by how close these numbers are. In fact, without special cards or elements like going to jail, all of the tiles get landed on almost exactly the same amount. You can see this for yourself with the following code:

```python
from monopoly_probability_sim import *
game = BaseMonopolySim()
game.averageOverNPlays(10, 10000) # choose higher numbers for a slower but more accurate result
print(game)
```
This plays the game with no monopoly elements accept a blank board and a die. Without any special rules to bias things, all tiles eventually average out to the same frequency.

Rolling doubles three times in a row sends you to jail, which means that tiles directly after jail get a boost in popularity. Also, cards like 'go to boardwalk' slightly increase the popularity of boardwalk, which has a similar effect on spots after boardwalk. This has a cyclic effect -- since 7 is the most common die roll, and there is a 'Chance' tile 7 steps after jail, that tile gets landed on disproportionally, sometimes sending you to jail. This increases the chances even more of going to jail and landing on Chance again. All these mechanisms mean that in a real game, some tiles are landed on more frequently than others.

However, the difference in frequency is small. Going to jail is rare: you have to either chance to land on the tile, get three doubles in a row (1/216 chance of three die rolls getting three doubles), or draw a go to jail card. The other effects, like getting sent to boardwalk, are even rarer. This is why "bad" tiles like Baltic Avenue are still less than a percentage point away from "good" tiles like Kentucky Avenue.

If you weren't surprised by how close the numbers are, maybe you are surprised by how far apart they are. While the difference between 2.0201% and 3.0126% may not seem like much, it means the best tile is almost 1.5 times as good as the worst. From a monetary perspective, if you were charging the same rent on both tiles (unlikely) you would get 1.5 times as much money from the better tile. Those are game winning numbers. In reality, the red tiles give you more in rent per visit as well as being more frequented. The browns are clearly worse.

My biggest takeaway is how good the railroads are! While they aren't as frequented as the reds or oranges, they come in at #3 in the list. Along with the other in game benefits (cost vs rent, no need to buy houses) they seem liking game winnng properties to me. 