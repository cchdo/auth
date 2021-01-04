Configuring
===========

If there is an existing uow config file, it will be migrated automatically to the locations used by ``cchdo.auth``.

.. warning::
    You must update ``cchdo.uow`` to the earliest version which also uses ``cchdo.auth``, v1.4.1.

There are several ways the library can get the API key, choose the method most appropriate for your environment.

Local File Config
-----------------
This method will create a config file that will persist between running programs that use this library.
Since the location of this file is platform specific, you must use the tools provided to create/change this file.

Using Command Line
``````````````````
``cchdo.auth`` is an executable module.
Once it is installed it can be run in a shell using:

.. code-block:: shell

    python -m cchdo.auth

This has a single command ``apikey``

.. code-block:: shell

    python -m cchdo.auth apikey <key>

Replace the entirety of ``<key>`` with your CCHDO api key.

Using the API
`````````````
You can create the config file from inside python.

>>> from cchdo.auth import write_apikey
>>> write_apikey("key")

Be sure to pass in the correct apikey as a string.


Environment Variable Config
---------------------------
The library will attempt to load the value of the envar ``CCHDO_AUTH_API_KEY``.

.. code-block::

    $ CCHDO_AUTH_API_KEY=test python
    
    Python 3.8.6 (default, Dec 18 2020, 05:24:40) 
    [GCC 8.3.0] on linux
    Type "help", "copyright", "credits" or "license" for more information.
    >>> from cchdo.auth import get_apikey
    >>> get_apikey()
    'test'
    >>> 

.. warning::

    If present, the envar will take precedence over the local config file.

Google Colab Config
-------------------
Configuring inside google colab is a little tricky due to the non persistence of the sessions.
We also want to be able to share the notebooks without worrying about secrets leaking out, i.e. we don't want to put api keys directly in the notebooks.
To accomplish this, there is a mechanism to load a file from google drive and inject its contents into environment variables inside the google colab session.

.. note::

    Since you can have multiple accounts in google colab and google drive, make sure to use the same account in both locations.

Create a text (utf8) file with the exact filename ``vars.env`` containing the following contents:

.. code-block:: none

    COLAB_ENV = Active
    CCHDO_AUTH_API_KEY = replace_with_apikey

Where your actual api key is in place of ``replace_with_apikey``.

Then upload this file to the "root" of your google drive, which is the location when you click on "My Drive" on the left menu/nav area of google drive.
Do not put it anywhere else (e.g. in a folder, team drive, etc..)
Because this file does not have a .txt extension, google drive will think it is "binary" and refuse to show you a preview when it is clicked on.

The first time you do something in colab which tries to find an api key, you will be walked though an authentication workflow to give the current colab session access to your google drive.
Access to your google drive will persist until the underlying colab session is stopped, you can restart the runtime and not need to go though the authentication workflow.