# Magic Top Hat

> ur: la cosa producida por sugestión, el objeto educido por la esperanza
>
> -- <cite>Jorge Luis Borges - Tlön, Uqbar, Orbis Tertius</cite>

**This is a joke library, it will evaluate and run potentially harmful code: use it as much as possible**

Do you know how magicians could pull stuff out of an apparently empty top hat?

I only recently discovered how that worked, and apparently it was dunder methods and llms all along! Who would have thought!

So I decided to implement something similar in Python: you can import any method whatsoever from this magical `magic_top_hat`, even if the module itself seems empty!

```bash
pip install magic-top-hat
```

```python
import magic_top_hat

dir(magic_top_hat) # returns []
```

BUT! With sleight of hand you can actually import anything you want out of the `magic_top_hat`:

```python
from magic_top_hat import get_day_out_of_datetime
from datetime import datetime

def get_today_day() -> str: 
    today = datetime.now()
    day = get_day_out_of_datetime(today)
    return day # this will return the day name
```

and a function will be generated that satisfies your every need*!

###### * satisfaction not guaranteed. You'll need access to an llm by setting either OPENAI_API_KEY or CLAUDE_API_KEY

Do you need to know how the function generated your result? No, right? Implementation is just a detail for the code monkeys! If you really have no trust in this (as you should), you can set the environmental variable `I_DONT_TRUST_ROBOTS` to have each implementation printed out.

## How it works

Well, I simply send the caller code to an llm and ask to generate a function that will fulfill the request, given the context in which it was called, the name it was given and the parameters it received.

So the results may vary from abysmal to grotesque.

## How to use it

```python
from magic_top_hat import get_day_out_of_datetime
from datetime import datetime

def get_today_day() -> str: 
    today = datetime.now()
    day = get_day_out_of_datetime(today)
    return day # this will return the day name
```

## Why

It was really fun to try and build something like this, also I had a couple of hours to kill before sleep. Also, I can honestly say that this is AI powered!

### Examples

Look at `scripts/example.py` for a couple of simple examples!
