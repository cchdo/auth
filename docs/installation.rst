Installation
============

Python Requirements
-------------------
This package is tested on python 3.10 through 3.12 on a linux environment, it has been run in a macOS environment and should also work on Windows.

Install With pip
----------------
Installation in your preferred python 3.10~3.12 environment should be as simple as:

.. code-block:: console
    
    pip install cchdo.auth

This should download the package from PyPI and resolve and install the dependencies for you.

Dependencies
------------
The current dependencies are:

* requests>=2.23.0
* click>=7.0.0
* appdirs>=1.4.0

Installation in an IPython Env (like colab)
-------------------------------------------
This can be installed in a Jupyter/IPython/Google Colab environment by using the "Shell execute" `magic command <https://ipython.readthedocs.io/en/stable/interactive/magics.html>`_.
Simply run this in an empty cell in the notebook:

.. code-block:: console

    !pip install cchdo.auth

.. note::
    The ``!`` prefixing the pip command is required in a Jupyter/IPython/Google Colab cell.