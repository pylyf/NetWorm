# NetWorm
[![forthebadge made-with-python](http://ForTheBadge.com/images/badges/made-with-python.svg)](https://www.python.org/)

> Python network worm that spreads on the local network and gives the attacker control of these machines.

This code is not finished and works more like a "worm template" for you to get inspiration at the moment. 

You can bruteforce ssh servers, spread with USBs, etc..

## Screenshots
![bruteforcing local machines](https://github.com/pylyf/NetWorm/blob/master/screenshots/pic1.PNG)
_Bruteforcing local machines with port 22 open._

## Downloading necessary libraries

```
pip install -r requirements.txt
```

## Executing

Windows & Linux:

```
python worm.py
```

## Compilation (.exe)

Targeted machines won´t probably have python and the required libraries instead. 
To run this code on other machines, you need to convert it into an executable.

I recommend the ![https://www.pyinstaller.org/](Pyinstaller library).

To use it, simply write these commands in your terminal:
```
pip install pyinstaller

pyinstaller worm.py
```



## Meta

[https://github.com/pylyf/NetWorm](https://github.com/pylyf/NetWorm)

Distributed under the MIT license. 

## Contributing

1. Fork it (<https://github.com/pylyf/NetWorm/fork>)
2. Create your feature branch (`git checkout -b feature/fooBar`)
3. Commit your changes (`git commit -am 'Add some fooBar'`)
4. Push to the branch (`git push origin feature/fooBar`)
5. Create a new Pull Request

## Legal Advice
This repository and every script included in it is for educational and testing purposes only.
The owner nor any contributor is not responsible for your actions.

