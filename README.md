# python-tail - Unix tail follow implementation in Python #

An UNIX-like asyncronous tailing with glob pattern matching.

## Installation ##

python setup.py install

## Basic Usage ##
    import tail

    # A callback function for each row:
    def do_something(row, filename):
        print(filename, ':', row)

    # Create a tail instance:
    t = tail.Tail('logs/*.txt', callback=do_something, sleep=1)

    # Start tailing:
    t.start()

    # Wait for an ENTER, and stop trailing:
    input()
    t.stop()
