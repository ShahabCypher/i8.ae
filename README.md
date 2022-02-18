<div align="center">
 <br />
 <p>
  <a href="https://i8.ae"><img src="https://discord.com/assets/7c13aa0def6ccb6932f47dedd33f59c1.svg" width="150" alt="i8.ae" /></a>
 </p>
</div>

# i8.ae Python Library
<br>

## Table of contents
- [About](#about)
- [Installation](#installation)
- [API key](#api-key)
- [Example Usage](#example-usage)
- [Links](#links)

## About
- Python library that makes your link shorter using [i8.ae](http://i8.ae/) API
- advantages
  - FREE to use
  - able to make links with password

## Installation
```
pip install i8.ae
```

## API key
- You have to first login to [i8.ae](http://i8.ae/) then go to [developers page](https://i8.ae/developers) and copy your API key

## Example Usage
```py
from i8 import i8

# adding api key
i8.add("YOUR_API_KEY")

# link shortener
short = i8.short("https://github.com/")
print(short) # Output: https://i8.ae/ETyxT

# link shortener (with password)
short = i8.short("https://github.com/", "pass")
print(short) # Output: https://i8.ae/WSRdf
```

## Links
- [PyPI]()
- [About me](https://github.com/ShahabCypher/ShahabCypher/)
