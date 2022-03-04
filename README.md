# Telegraph - Bachelor thesis of Valentin Peter
This is the repository of the Bachelor Thesis: **'Methods for communication research on Telegram: examining the network of COVID-19 sceptics in Germany.'**

## Setup project on Mac OS
To install the required dependencies and packages run:
1. Run Setup script `sh setup.sh`
2. Activate virtual enviroment `source televenv/bin/activate`
3. Start jupyter notebook `jupyter-notebook`

## Scraper 
The Scraper uses a technique called discriminative snowball sampling to sample Telegram channels given a seed. It can be accessed from within the repository as such:

```python
# This is an example how the code could be used
from scraper.scraper import Scraper
from scraper.client import Client

Client(api_id=123456,
       api_hash="***********",
       phone="+49***********")

scraper = Scraper(num_messages=None,
                  step_size=200,
                  maximum_iterations=1)

scraper.scrape(["some_channel", "some_other_channel"])
```



## Data analysis 
The analysis of over 50 million messages is conducted in the two notebooks [Data Preprocessing](Data Preprocessing.ipynb) and [final_analysis](final_analysis.ipynb). The Data Preprocessing notebook needs to be executed first, the analysis notebook second. Due to privacy reasons the data wont be published. When using the same seed as described in the thesis on the scraper it is possible to reproduce the data set. The code for reproducing the data is provided in the file [example.py](example.py).

The original execution ist still maintained in [final_analysis](final_analysis.ipynb), therefore code and results can be inspected simultaneously. 
