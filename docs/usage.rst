Usage
=====
Once :ref:`installed <Installation>` and :ref:`configured <Configuring>` usage should be simple, even for existing code which relies on requests.

Preconfigured Session
---------------------

The recommended way of using ``cchdo.auth`` is with the preconfigured ``session`` object.

>>> from cchdo.auth.session import session
>>>

If you haven't configured ``cchdo.auth`` yet, you will probably get the following warning:

>>> from cchdo.auth.session import session
An API Key could not be loaded from any source, many (not all) CCHDO API calls will fail
>>> 

If this happens, do the :ref:`configuration <Configuring>` steps and restart your python session.

The ``session`` object is a standard requests Session which has been configured with an auth provider:

>>> session
<requests.sessions.Session object at 0x7f1e2ea67a60>
>>> 

The full requests API is available on it.
When a request is sent to the CCHDO API, authentication credentials will automatically be added.

>>> session.get("https://cchdo.ucsd.edu/api/v1/cruise").json()

.. note::

    It is safe to use this session with non CCHDO API URIs, the api key headers are only added when a request is sent to CCHDO.

.. danger::

    Do not alter the ``.auth`` property of the imported ``session`` object.
    If you need to make authenticated requests to non CCHDO URIs, directly use ``requests``.


Direct Auth Class Usage
-----------------------
The custom Auth class can also be used with ``requests``.

>>> import requests
>>> from cchdo.auth import CCHDOAuth
>>> cchdo_auth = CCHDOAuth()
>>> requests.get("https://cchdo.ucsd.edu/api/v1/cruise", auth=cchdo_auth).json()

This is more useful if you need to override the API Key for some reason:

>>> import requests
>>> from cchdo.auth import CCHDOAuth
>>> cchdo_auth = CCHDOAuth("custom_api_key")
>>> requests.get("https://cchdo.ucsd.edu/api/v1/cruise", auth=cchdo_auth).json()


Use in Existing Code
--------------------
Assuming you want to use the preconfigured ``session`` object everywhere, two things need to happen with existing code.

Use cchdo.auth.session instead of requests
``````````````````````````````````````````
All get, post, put, patch, etc... method calls need to be switched to use the session object.
This can be accomplished somewhat easily by aliasing the import.
For example, if you do something like the following:

>>> import requests as r
>>> r.get("some_api_call")

You can simply alias the session object:

>>> from cchdo.auth.session import session as r
>>> r.get("some_api_call")

If you use requests directly:

>>> import requests
>>> requests.get("some_api_call")

Just alias the session to requests:

>>> from cchdo.auth.session import session as requests
>>> requests.get("some_api_call")

Remove Existing Auth Code
`````````````````````````
Since the preconfigured ``session`` object will handle putting http headers in the right place, you need to remove all existing API auth machinery from existing code.
This will most likely result in less code since the relevant parts just need to be deleted.

For example:

.. code-block:: python

    import requests
    API_KEY = "some_key here"

    result = requests.get("https://cchdo.ucsd.edu/api/v1/cruise", headers={
        "X-Authentication-Token": API_KEY
    }).json()

should be changed to the following:

.. code-block:: python

    from cchdo.auth.session import session as requests

    result = requests.get("https://cchdo.ucsd.edu/api/v1/cruise").json()