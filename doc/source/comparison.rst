Comparison to TabPy
===================

Maintenance and Ideology
~~~~~~~~~~~~~~~~~~~~~~~~
AltTabPy focuses on a small subset of the functionality offered by TabPy. Whereas TabPy offers a component to publish, create and manage endpoints containing code samples, AltTabPy does no such thing. Instead, AltTabPy leaves it to the user to configure their Python environment with everything they need and simply execute code within Tableau, rather than trying to configure it through any extra means.

The advantage here is that the code base for AltTabPy is significantly smaller than that of TabPy; as of authorship TabPy was close to 6000 lines of code whereas AltTabPy was less than 300, or less than 5% of the size of TabPy.

AltTabPy also had the advantage of starting with a clean code base with no compatability concerns. TabPy still manages a large amount of code from Python2 and has not yet evolved to some of the more recent Python3 offerings like type hinting.

Use Cases
~~~~~~~~~
AltTabPy aims to get a single user up and running as fast as possible using Tableau and Python in tandem. This can be done on virtually any platform in a few minutes at most.

By contrast, TabPy aims to be a larger enterprise solution which as of writing requires managing dependencies, targeting specific platforms and going through a rather complex installation process.

This does not mean that AltTabPy can't extend beyond single-use applications and that TabPy couldn't streamline it's installation processses, but in any case both projects are tackling this area from different angles.

Security
~~~~~~~~
AltTabPy offers no extra security configurations. Because it's initial goal is for single-use computing, it simply would be overkill to offer an authentication system on top of that.

TabPy has a new authentication system under development which may be more suitable when trying to manage a large team of users.
