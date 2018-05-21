# CombiChess

CombiChess a "chess engine" that combines 3 engines into one. It works by essentially asking 3 different engines what the they think is the best move for a given position, and then applying some logic to determine what move to actually do.  After initial testing, it seems like it can easily beat the strongest of the 3 engines on its own.

The rules that it uses are fairly simple:
  * If 2 out of 3 engines give the same best move, then do that move and cancel work of the third.
  
  * if all 3 engines say something else, listen to engine 0.
  
  * if all 3 engines agree, do that move.(actually, this never happens as work of the third engine is cancelled when the first two agree)
  
  
For the best results, the 3 engines that are used need to be as equal in strength as possible. If one of the three is slightly better, it is best to use that one as engine0, since CombiChess listens to engine0 when all engines give a different result.
  
  ## Testing 
  
  For testing, i used the [silver suite](https://en.chessbase.com/post/test-your-engines-the-silver-openings-suite) of openings. I used 100 games, with a fixed time of one second per move. More testing will follow. 
  
  The engines that i used, with their elo rating according to [CCRL](http://www.computerchess.org.uk/ccrl/404/cgi/compare_engines.cgi?class=Free+single-CPU+engines&num_best_in_class=1&print=Rating+list&profile_step=50&profile_numbers=1&print=Results+table&print=LOS+table&table_size=100&ct_from_elo=0&ct_to_elo=10000&match_length=30&cross_tables_for_best_versions_only=1&sort_tables=by+rating&diag=0&reference_list=None&recalibrate=no)  are listed below 
  
  
  * StockFish 5 (3244)
  * Komodo 8 (3236)
  * Andscacs 0.93 (3209)
    
As opponent i also used Stockfish 5, to essentially see if StockFish could be improved with the help of two slightly lesser engines.
    
StockFish 5 was used for was used as engine 0, as it is ranked the highest. Testing with other engines as engine0 will follow.  
  
## Initial Results
Tournament 1, 100 games, CombiChess[StockFish5,Komodo8,Andscacs0,93] vs StockFish 5:
  
33 wins for CombiChess, 14 wins for Stockfish5, 53 draws.
