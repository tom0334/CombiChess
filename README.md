
# CombiChess

CombiChess a "chess engine" that combines 3 engines into one. It works by essentially asking 3 different engines what the they think is the best move for a given position, and then applying some logic to determine what move to actually do.  After initial testing, it seems like it can easily beat the strongest of the 3 engines on its own.

The rules that it uses are fairly simple:
  * If 2 out of 3 engines give the same best move, then do that move and cancel work of the third.
  
  * if all 3 engines say something else, listen to the 'Master engine'. The master engine is simply engine0
  
  * if all 3 engines agree, do that move.(actually, this never happens as work of the third engine is cancelled when the first two agree)
  
  
For the best results, the 3 engines that are used need to be as equal in strength as possible. If one of the three is slightly better, it is best to use that one as master/engine0, since CombiChess listens to the master when all engines give a different result.
  
  ## Testing 
  
  For testing, i used the [silver suite](https://en.chessbase.com/post/test-your-engines-the-silver-openings-suite) of openings. I used 100 games, with a fixed time of one second per move. More testing will follow. 
  
  The engines that i used, with their elo rating according to [CCRL](http://www.computerchess.org.uk/ccrl/404/cgi/compare_engines.cgi?class=Free+single-CPU+engines&num_best_in_class=1&print=Rating+list&profile_step=50&profile_numbers=1&print=Results+table&print=LOS+table&table_size=100&ct_from_elo=0&ct_to_elo=10000&match_length=30&cross_tables_for_best_versions_only=1&sort_tables=by+rating&diag=0&reference_list=None&recalibrate=no)  are listed below 
  
  
  * StockFish 5 (3244)
  * Komodo 8 (3236)
  * Andscacs 0.93 (3209)
  
    
As opponents i also used those engines, to essentially see if they can be improved with the help of two other engines similar in strength. Later on i plan on playing against other engines as well.

Testing was done for each engine as master, against all opponents. For example: Combichess with Stockfish as master/engine0 and the other two engines as engine1 and engine2, was first tested against Stockfish on its own, then against komodo and then against Andcacs. I did the same for the other engines as master.

  
## Results(so far, still in progress):

This table shows all results so far. The scores are all from the POV of Combichess, 33 -14 means that Combichess won 33 games, the opponent won 14 and the rest of the 100 games were draws.

| ↓OPPONENT↓  →MASTER ENGINE→| Stockfish 5 	| Komodo 8 	| Andscacs 0.93 	|
|----------------------------|-------------	|----------	|---------------	|
|**Stockfish 5**             | 33 - 14     	| 32 - 18  	|46 - 9          |
|**Komodo 8**                | 27 - 20     	| 36 - 15  	|               	|
|**Andscacs 0.93**           | 39 - 16     	| 38 - 11  	|               	|



## Initial Conclusion
Combichess with both Stockfish 5 and Komodo8 as master seems to  be quite significantly stronger than any of the 3 engines that it uses! More testing with other engines as master is coming soon!  
