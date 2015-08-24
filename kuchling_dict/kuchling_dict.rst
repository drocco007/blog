.. ----------------------------

Of Dictionaries and Analysis
----------------------------

I greatly enjoyed reading Andrew Kuchling's `Beautiful Code`_ article “Python's
Dictionary Implementation: Being All Things to All People,” [1]_ in which
Kuchling explores some of the implementation details of what is arguably
CPython's most important data structure: the ``dict``. While these
implementation details themselves are fascinating, the article offers a deft
illumination of the thought process that led to the selection of a given
implementation over its alternatives. The lessons here are not just for open
source hackers working on the performance-critical portions of a popular
language: they offer sound process guidance to anyone needing to make wise
choices in the face of conflicting needs and trade-offs when building any kind
of software.

Kuchling summarizes his main thesis about halfway through the article:

    When trying to be all things to all people — a time- and memory-efficient
    data type for Python users, an internal data structure used as part of the
    interpreter's implementation, and a readable and maintainable code base for
    Python's developers — it's necessary to complicate a pure, theoretically
    elegant implementation with special-case code for particular cases… but not
    too much.

The brilliance of the article rests on how Kuchling shows the available
trade-offs for a given problem explicitly, always couching them in reference to
those user groups and their real-world needs. It's interesting as a postmortem,
but also offers a valuable blueprint for structuring design processes such that
compromises get debated on their specific, explicitly articulated merits and
shortcomings rather than on hidden assumptions, preferences, and biases. Once
the options are on the table, it becomes possible to consider their strengths
and weaknesses in light of the needs of affected users rather than having to
rely solely on theoretical or aesthetic considerations.

With that in mind, here are some specific lessons we can draw from the article
about how to structure the process of analyzing potential software solutions.


Lesson 1: Maintainability Matters, Therefore Maintainers Matter
---------------------------------------------------------------

An important but subtle take away from Kuchling's thesis is that developers
form one of the user groups with a stake in the outcome, and that therefore
code readability and maintainability constitute legitimate, first-order user
concerns that deserve weighted consideration alongside the needs of other user
groups. Although Kuchling doesn't provide specific examples demonstrating this
trade-off in action, this idea forms a theme woven throughout the entire
discussion: unless you have a compelling, measured reason not to, prefer
simplicity.

This can be challenging conversation to have, especially in commercial contexts
with their strong emphasis on feature delivery and satisfying client user
demands. A mechanism we use to allow compromise on this front, which we can
call the “maintainability gradient,” suggests that changes that have broader
reach or usage mandate a higher level of scrutiny with respect to complexity
and maintainability. When considering a client request, for each solution under
discussion the development team offers an assessment of its maintainability:
the solution's inherent complexity, the ease or difficulty of implementing it
within the framework and underlying assumptions of the existing platform,
especially under time constraints, and the likelihood that we will be required
to tinker with it after delivery. This becomes one of the inputs that helps us
determine where in the layered architecture a given solution will be allowed:

    .. figure:: http://2.bp.blogspot.com/-sjTb0Lpd2Ew/Vdpy-RADdEI/AAAAAAAACPE/jxyNGjyALew/s1600/gradient_arch.png
        :align: center

        **Figure 1**: Our layered architecture. The top of the stack is the
        most-specific, least-shared code, while the bottom layers are most
        shared.

In this context, our maintainability gradient provides guidance about where
complication is acceptable and where it is not: while we always strive to
create simple solutions, if an end user insists on something complicated or
messy, it is shunted to client-specific code where its impact on the platform
can be minimized and contained. Conversely, proposed additions to the core
platform must meet a higher standard of maintainability: does this change fit
within the existing context of the platform? Can it be implemented simply and
readably?

Note that this is not an excuse to do slipshod work, even in obscure cul-de-sacs
of custom code. Quite the opposite: this approach empowers developers to
do great work everywhere within the context of a resource-constrained
commercial enterprise. If a solution can't be maintainably generalized under
current constraints, we can implement a smaller, specific version where the
solution is easier to isolate. We don't always get the trade-off right, but
this architecture gives us an axis of compromise that allows maintainability to
have a voice in the conversation.


Lesson 2: Whom Do You Serve?
----------------------------

Another key design process lesson from Kuchling's article is that it is
imperative to understand users and their needs, and to evaluate proposed
solutions in light of those needs. Concretely, this means

    1. listing each alternative explicitly

    2. describing the characteristics of each solution relative to each user
       group

    3. choosing the solution that is the best compromise among the various
       alternatives

The short section on handling hash collisions in the article illustrates this
process nicely. The problem is this: when implementing a hash table, what do we
do when two keys inevitably hash to the same slot?

One option is to use chaining: instead of single values, each slot holds a list
of values with the same hash. CPython does not do this “because creating linked
lists would require allocating memory for each list item, a relatively slow
operation.” In other words, CPython does not use chaining because this solution
fails to meet the needs of at least two of the important user groups identified
earlier: end-users of Python needing an efficient mapping data structure, and the
language implementors who need an efficient platform on which to build objects,
modules, and functions.

The next option up for consideration is linear probing: if a needed hash slot
$i$ is occupied, examine $i+1$, $i+2$, etc. This solution is quite simple to
implement, but again CPython does not use it. Why not? “Many programs use
consecutive integers as keys,” which, due to how CPython hashes integers,
consume contiguous blocks of the hash table that are inefficient for linear
probing. Having identified the performance characteristics of this
solution explicitly, it is easy to see the trade-offs being made here and the
user groups affected by those trade-offs: linear probing is simple to implement
— a boon for the maintainers — but that simplicity yields a solution that does
not serve the performance needs of the language implementors or end-users very
well.

This analysis is predicated on both understanding who the users are and what
their usage patterns look like while simultaneously understanding the spectrum
of available solutions considered in light of the needs of those various user
groups. In the end, CPython's hash collision resolution algorithm is a
pragmatic compromise, guided by experimentation, measurement, and feedback,
that concedes a little code complexity in exchange for good performance
characteristics in the real world.


Lesson 3: … but not too much
----------------------------

My favorite optimization that Kuchling describes is a complexity/performance
trade-off. The dilemma is this: how can the ``dict`` implementation serve a
general audience — by handling non-string keys, rich comparison operators, and
possible exceptions — while also offering good performance for the huge swath
of ``dict`` usages with exclusively string keys, such as those that underlie
the implementation of classes, modules, and functions?

One approach would be to implement separate classes: a specialized, string-only
``dict`` optimized for high-performance for this use case along with a more
general purpose implementation for regular use. In fact this is exactly what
Jython, the Python implementation that runs on the JVM, does: it utilizes
Java's  ``java.util.HashMap`` as the basis for the ``dict`` implementation for
general purpose use but employs a separate, optimized class to handle the
performance-sensitive language implementation bits.

CPython instead uses a single implementation but employs two different lookup
functions. By default, ``dicts`` are assumed to contain only string keys, and
since many of the complexities and failure modes that arise when comparing two
arbitrary objects are impossible when comparing two strings, the default lookup
function can be optimized to eliminate checks for cases or errors that simply
cannot happen. The implementation is a classic use of indirection that relies
on a simple function pointer: if an arbitrary, non-string object is searched
for or inserted into a ``dict`` instance, the search function pointer for that
instance is updated to reference the slower but more general purpose lookup
implementation that can handle the added complexities concomitant with
comparing arbitrary objects.

This example beautifully illuminates a pragmatic, “not too much” compromise
that serves its various users well. For the language implementors, the solution
provides an important performance boost for lookups in classes and modules and
passing of keyword arguments to functions, all of which are exclusively string-
keyed and are the most frequent operations in a running Python program. It is
also fairly simple, easy to understand, and is likely less code than a two-class
solution would be. This in turn helps minimize the potential for
implementation drift and maintains the “fits in your head” quality valued
by the Python community.

The compromise also serves end users very well: string-keyed
``dicts`` are very common in many applications, so end users reap a double
benefit: attribute lookups and function calls are faster, and, as an added
bonus, portions of their systems that rely on string-keyed ``dicts`` are also
sped up.


.. raw:: html

    <p style="text-align: center">* * *</p>


.. _`Beautiful Code`: http://www.amazon.com/Beautiful-Code-Leading-Programmers-Practice/dp/0596510047

.. [1] I couldn't find the article online except at `Safari <https://www.safaribooksonline.com/library/view/beautiful-code/9780596510046/ch18.html>`_ (free trial available).
