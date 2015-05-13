# qd

. used egain instead of gain for label
. used price > 10 to generate gain (label) to avoid surviver bias, tested
  by comparing mean gain after filtering to R3000 and asserted no big diff

AIs:
- add volume features similar to pgain and pegain (but instead of sampling,
  use aggregated volume over a month)
- interact volume and price features
. try using excess return as label; motivation: if there is a major market
  correction at t + predictionWindow, then the data point right before t
  is likely to have a big positive gain and the one right after t is likely
  to have a big negative gain even though two points share similar features
- try classification
- try "personalization" by training separate models by sector or per-ticker
  offset models

