"""
VerboseCall class is useful for debugging purposes.
"""


def dict_to_parameters(d):
    """{'k': 1, 'a': 2} -> k=1, a=2"""
    kwargs = []
    for x, y in d.items():
        if isinstance(y, str):
            y = "'%s'" % y
        kwargs.append('%s=%s' % (x, y))
    return ', '.join(kwargs)


class VerboseCall(object):
    """Wrapper class, which prints extra information when the actual class'
    methods are accessed.
    """

    guide_text = 'Press enter to call(Ctrl-C to stop) '

    def __init__(self, obj, emulate=False, prompt=True):
        """obj: Object which methods are going to be called.
        emulate: If True, methods are not actually called
        """
        self.obj = obj
        self.emulate = emulate
        self.prompt = prompt

    def __getattr__(self, name):
        """If class' attribute is accessed and it does not exist, this
        method will be called.

        Returns:
            A function that will return self.obj's attribute named name.
            If the attribute is callable:
                - Print the method that will be called
                - Prompt if the method should be called
                - Call the method if emulate=False
                - Print and return the return value
        """
        def func(*args, **kwargs):
            # Python gives arguments as a tuple, convert them to list.
            f = getattr(self.obj, name)
            if not callable(f):
                return f

            # Print the function call as it would be written in code.
            a = ', '.join([str(x) for x in args])
            kw = dict_to_parameters(kwargs)
            if len(kw):
                kw = ', ' + kw
            print('Calling \'%s(%s%s)\'..' % (name, a, kw))

            if self.prompt:
                raw_input(self.guide_text)

            response = None
            if not self.emulate:
                response = f(*args, **kwargs)
                print '->', response

            return response

        return func


class Test(object):
    """Just to demonstrate VerboseCall."""

    def do_thing(self, a, k=1):
        b = a + k
        return b

    def do_else(self, i):
        return [i] * 4



if __name__ == '__main__':
    test = Test()
    t = VerboseCall(test)

    print('Demonstrating how the VerboseCall works..')
    t.do_thing(1, k=2)
    t.do_else('a')

    print('\nYou can now try it yourself inside a Python prompt.')
    print('\'t\' is instance of VerboseCall, which wraps Test.')
    print('E.g. t.do_thing(2, k=4)\n')
    import code
    code.interact(local=locals())
