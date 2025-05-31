# cparsers

Parser combinator library written in Python.  
It's simple, greedy, and doesn't handle recursion.  

BUT

It works for **me**.

## Installing

1. Download file `.whl` file
    ```
    wget https://github.com/Cieciak/parsers/raw/refs/heads/main/dist/cparsers-0.2.0-py3-none-any.whl
    ```
2. Install using pip3
    ```
    pip3 install cparsers*.whl
    ```

> I can't be bothered to put this on PyPi rigth now, maybe later.

## Building

1. Clone repository
    ```
    git clone https://github.com/Cieciak/parsers.git
    ```

2. Initialize Python virtual enviroment
   ```
   make init
   ```

3. Build the package
   ```
   make
   ```
    
    Output will be in `dist` folder

**If something goes wrong, you can clear the enviroment by using:** `make clearall`