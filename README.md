
# CombiChess

CombiChess a "chess engine" that combines 3 engines into one. It works by asking 3 different engines what they think the best move is for a given position, and then applying some logic to determine what move to actually do.  After initial testing, it seems like it can easily beat the strongest of the 3 engines on its own.

The rules that it uses are fairly simple:
  * If 2 out of 3 engines give the same best move, then do that move and cancel work of the third.
  
  * if all 3 engines say something else, listen to the 'Master engine'. The master engine is simply engine0
  
  * if all 3 engines agree, do that move.(actually, this never happens as work of the third engine is cancelled when the first two agree)
  
  
For the best results, the 3 engines that are used need to be as equal in strength as possible. If one of the three is slightly better, it is best to use that one as master/engine0, since CombiChess listens to the master when all engines give a different result.
  
  ## Testing 
  
  For testing, the [silver suite](https://en.chessbase.com/post/test-your-engines-the-silver-openings-suite) was used, which resulted in 100 games per matchup. At first, a fixed time of 1 second per move was chosen, because then all engines would take the same amount of time to think.
  
  Currently, testing is being done with a time control of 1 minute plus 0,5 seconds per move extra. The engines can decide for themselves how long they think, which results in CombiChess sometimes waiting for the last engine to finish. 
  
  The engines that that were used, with their elo rating according to [CCRL](http://www.computerchess.org.uk/ccrl/404/cgi/compare_engines.cgi?class=Free+single-CPU+engines&num_best_in_class=1&print=Rating+list&profile_step=50&profile_numbers=1&print=Results+table&print=LOS+table&table_size=100&ct_from_elo=0&ct_to_elo=10000&match_length=30&cross_tables_for_best_versions_only=1&sort_tables=by+rating&diag=0&reference_list=None&recalibrate=no)  are listed below 
  
  
  * StockFish 5 (3244)
  * Komodo 8 (3236)
  * Andscacs 0.93 (3209)
  
    
As opponents, the same engines were used, to see if they can be improved with the help of two other engines similar in strength. Later on i plan on playing against other engines as well.

Testing was done for each engine as master, against all opponents. For example: Combichess with Stockfish as master/engine0 and the other two engines as engine1 and engine2, was first tested against Stockfish on its own, then against komodo and then against Andcacs. The same was done for the other engines as master.

  
## Results:

This table shows all results of the fixed time testing. The scores are all from the POV of Combichess, 33 -14 means that Combichess won 33 games, the opponent won 14 and the rest of the 100 games were draws.

| ↓OPPONENT↓  →MASTER ENGINE→| CombiChess With Stockfish 5 	|  CombiChess with Komodo 8 	| CombiChess with Andscacs 0.93 	|
|----------------------------|------------------------------|----------------------------|--------------------------------|
|**Stockfish 5**             | 33 - 14                 	    | 32 - 18  	                 | 46 - 9                         |
|**Komodo 8**                | 27 - 20     	                | 36 - 15  	                 | 52 - 14        	               |
|**Andscacs 0.93**           | 39 - 16     	                | 38 - 11  	                 | 46 - 9         	               |


The following (in progress) table shows the same games, but played with a non fixed time per move. As discussed above, this means some engines are done earlier than others. Time control was set to 1 minute plus 0,5 seconds per move.

| ↓OPPONENT↓  →MASTER ENGINE→| CombiChess With Stockfish 5 	|  CombiChess with Komodo 8 	| CombiChess with Andscacs 0.93 	|
|----------------------------|------------------------------|----------------------------|--------------------------------|
|**Stockfish 5**             | 32 - 12                 	    | -  	                       | -                         |
|**Komodo 8**                | 25 - 16      	               | -  	                       | -         	               |
|**Andscacs 0.93**           | 32 - 18      	               | -  	                       |  -          	               |



## Initial Conclusion
Combichess with Stockfish 5, Komodo8 and Andscacs as master seems to  be quite significantly stronger than any of the 3 engines that it uses! For now, non- fixed time looks a little weaker, but not as much as I initially expected.  

## Using CombiChess
To use combichess, clone the project or download it as a zip. Unzip it if needed, and then place the engines you want to use in the engines folder. Open launcher.py and change the filenames to the ones in the engines folder you want to use.

Combichess has one dependency: python-chess. Assuming you have python on your computer, you can install it by opening a terminal and typing the following:

```
pip install python-chess
```

To run CombiChess, execute the launcher.py, NOT the combichess.py!
