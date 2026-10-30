# f1-high-level-scraper

This is a scraper to find the Driver & Constructor champs of each Formula One season, pulling
from Wikipedia; the scraper writes the information to f1_champions.csv. To give more color: the program starts by following a link to each season and reads the champions from that infobox. I used libraries we covered in the course, such as requests to fetch and re to parse. In accordance with the instructions, I also used concurrent.futures to fetch in parallel; see below for timed runs with varying numbers of cores.

## How to use the scraper

pip install -r requirements.txt

./scraper.py
./scraper.py -n 1                # 1 thread
./scraper.py -n 2 out.csv  # 2 threads
./scraper.py -h                  # usage

## Real output

$ ./scraper.py

<img width="679" height="60" alt="image" src="https://github.com/user-attachments/assets/bee2a0cf-7aba-4b56-91bf-80c6839bcccc" />

$ head -7 f1_champions.csv

<img width="657" height="152" alt="image" src="https://github.com/user-attachments/assets/a69c15df-6786-43a7-b06b-808a193303ef" />

## Performance impacts

| workers | seconds | speedup (x) |

| 1  | 14.79 | 1.0  |

| 8  | 2.28  | 6.5  |

| 16 | 1.14  | 13.0 |

concurrent.futures: As we have said in class, while there is certainly benefit to using multiple threads, the gain starts to flatten because of bottlenecks.

functional programming: helps keep the threads safe. Allows copies to run simultaneously without deadlocks or race conditions (as the terminology is in our course slides).

(Side note: I filled out this README based on the sections outlined in the assignment instructions; I also used online tools to help me on the GitHub end)
