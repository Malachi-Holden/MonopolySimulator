# Monopoly Tile Frequency Model

This is an accurate model for estimating the frequency of landing on each tile on a monopoly board. Plays a game by rolling a pair of virtual dice and moving a player around a virtual monopoly board, counting how many times each square is landed on. Takes into account all aspects of the game that affect player movement, such as jail. Does not take money or player competition into account.

It is not necessary to use multiple players, since players don't have any affect on each other's movement. It is equivalent to play multiple games with one player.


# Results
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
