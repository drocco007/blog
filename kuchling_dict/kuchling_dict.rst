============================
Of Dictionaries and Analysis
============================

I greatly enjoyed reading Andrew Kuchling's `Beautiful Code`_ article “Python's
Dictionary Implementation: Being All Things to All People,” in which Kuchling
explores some of the implementation details of what is arguably CPython's most
import and data structure: the ``dict``. While these implementation details
themselves are fascinating, the article offers a deft illumination of the
thought process that led to the selection of a given implementation over its
alternatives. The lessons here not just for open source hackers working on the
performance-critical portions of a popular language: they offer sound process
guidance to anyone needing to make wise choices in the face of conflicting
needs and trade-offs when building software.

Kuchling summarizes his main thesis about halfway through the article:

    When trying to be all things to all people — a time- and memory-efficient
    data type for Python users, an internal data structure used as part of the
    interpreter's implementation, and a readable and maintainable code base for
    Python's developers — it's necessary to complicate a pure, theoretically
    elegant implementation with special-case code for particular cases… but not
    too much.

The brilliance of the article rests on how Kuchling shows the available trade-
offs for a given problem explicitly, always couching them in reference to those
user groups and their real-world needs. It's interesting as a postmortem, but
also offers a valuable print for structuring design processes such that
compromises get debated on their specific, explicitly articulated merits and
shortcomings rather than on hidden assumptions, preferences, and biases. Once
the options are on the table, it becomes possible to consider their strengths
and weaknesses in light of the needs of affected users rather than having to
rely solely on theoretical or aesthetic considerations.

With that in mind, here's some specific lessons we can draw from the article
about how to conduct solution analysis.


Lesson 1: Maintainability Matters, Therefore Maintainers Matter
---------------------------------------------------------------

An important but subtle take away from Kuchling's thesis is that developers
form one of the user groups with a stake in the outcome, and that therefore
code readability and maintainability constitute legitimate, first-order user
concerns that deserve weighted iteration alongside the needs of other user
groups. Although Kuchling doesn't provide specific examples demonstrating this
trade-off in action, this idea forms of theme woven throughout the entire
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
within the framework and underlying assumptions of the existing platform, and
the likelihood that we will be required to tinker with it after delivery.
