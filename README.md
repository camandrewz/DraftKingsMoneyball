# DraftKingsMoneyball
A Quantitative Approach to DraftKings Daily Fantasy Sports


Approach:

- Calculate the expected values of a variety of individual player statistics using their last 10 games. (Pts, Steals, Assists, Rebounds, etc.)
- Brute force the best 250 lineups that maximize projected fantasy points while remaining under the $50,000 DraftKings budget.
- Run a Monte Carlo simulation by randomly selected individual player statistics from the normal distribution of their past performance in each category.
- Display the best performing teams after the simulation ends.
