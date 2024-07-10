# Top Hat

Do you know how magicians could pull stuff out of an apparently empty top hat?

I only recently discovered how that worked, and apparently it was dunder methods all along! Who would have thought!

So I decided to implement something similar in Python: you can import any method whatsoever from this magical `magic_top_hat`, even if the module itself seems empty!

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

Do you need to know how the function generated your result? No, right? Implementation is just a detail for the code monkeys! If you really have no trust in this (as you should), you can set the environmental variable `I_DONT_TRUST_ROBOTS` to have each implementation printed out.

*satisfaction not guaranteed. You will need to set a `OPENAI_API_KEY` env parameter for this to work. And even then, it might not work.

## How

Well, I simply send the caller code to OpenAI and ask ChatGPT to generate a function that will fulfill the request, given the context in which it was called, the name it was given and the parameters it received.

So the results may vary from abysmal to groteque.

## Why

It was really fun to try and build something like this, also I had a couple of hours to kill before sleep. Also, I can honestly say that this is AI powered!

### Examples

Look at `scripts/example.py` for a couple of simple examples!
