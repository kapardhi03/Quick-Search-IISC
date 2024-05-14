from goose3 import Goose

g = Goose()

title = g.extract("https://www.thehindubusinessline.com/portfolio/how-previous-general-elections-have-impacted-sensex-and-nifty-50-performance-insights-for-investors/article67857670.ece").title

print(title)
