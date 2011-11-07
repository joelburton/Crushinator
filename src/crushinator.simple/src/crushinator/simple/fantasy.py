from crushinator import SimpleRecipe, ...

# Fantasy:
#
# A optimistic pseudo-implementation of a "simple recipe"
# that consists of straightforward interrogators, probles, and simple
# Python-template-replacing skeletons.
#
# This code should be revisited as the underlying compontents are built with
# the expectation that one day there will be a simple recipe class that
# allows for easy creation of "standard" kind of recipes.
#
# Author: Joel Burton <joel@joelburton.com>
#
# Written and discussed at Crushinator sprint, SF Conference Nov 2011
#
# Names of presumptive classes/factory methods here ("TemplateSkeleton", et al)
# are merely under-thought-out suggestion; don't read these as canonical.


# We'll have one interrogator with one one "probe" (question)

interrogators = [

    Interrogator(
        name='crushinator.simple.license.choices',
        label='License Choices',
        description=None,

        probes = [ 
            # "SelectionProbe" will be the simple-list-of-choices probe subtype
            SelectionProbe(
                name='crunshinator.simple.license.choice',
                label='License Choice',
                description='Choose a license: BSD, GPL, or MIT',
                vocab=['BSD','MIT', 'Communism'],
                )
            ],
        )
    ]

# here our list of "producers" (common name for skeletons/injectors) is just one
# thing--a single instance of the simple python-template-replacing skeleton

producers = [ TemplateSkeleton('templates/doc/', 'somewhere/in/output/') ]


recipe = SimpleRecipe(
        name='crushinator.simple.license',
        label='License Choice',
        description='Pick a license choice',

        # the "simple runner" will just walk the list of interrogators and
        # producers

        runner = SimpleRunner( interrogators=interrogators, producers=producers )


# We don't need to explicitly register any of the components here; instead, the
# egg machinery will say that fantasy.recipe is an entry point and therefore
# can show up int the list of recipes. In addition, the SimpleRecipe class
# should do any neccessary registration of the interrogators and producers.






