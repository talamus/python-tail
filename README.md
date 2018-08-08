# python-tail - Unix tail follow implementation in Python #

## Installation ##

python setup.py install

## Basic Usage ##
    import tail

    # Create a tail instance:
    t = tail.Tail('file-to-be-followed', callback=print, sleep=1)
    # (Optionally you can register a callback function and set the sleep time.)

    # Start tailing:
    t.start()

    # Wait for an ENTER, and stop trailing:
    input()
    t.stop()
