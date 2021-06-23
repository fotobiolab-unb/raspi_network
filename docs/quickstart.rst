Quickstart
==========

The most basic way to send a command and other IO controls to the microcontrollers connected to the clients (here assumed to be Arduinos) is through the `experiment_0.py` module. This module can be duplicated and modified at will to satisfy your needs and it won't yield any problems as long as the copy still resides on the same folder or all its necessary libraries are properly referenced on `$PYTHONPATH` or `sys.path`. The module is composed of the following most important methods and classes:

.. code-block::

    experiment_0
    ├── control
    ├── hanashi.arduino_command
    ├──stage_0_read
    ├──stage_0_set

`hanashi.arduino_command(str command,[list servers],[boolean wait_return])`
---------

Sends an arduino command via serial.

* command(str): Command to be sent to the microcontroller.
* servers[list]: List of urls for the destination hosts.
* wait_return[boolean]: Whether or not to wait for a response.

Example
~~~~~~~

Sending a command `set(brilho,100)` to an Arduino connected to host `192.168.0.1` on port 2000 without waiting for a response:

.. code-block:: python

    import experiment_0 as e0
    
    e0.hanashi.arduino_command("quiet_connect") #Only needs to run once
    e0.hanashi.arduino_command("set(brilho,100)",["http://192.168.0.1:2000"])

`class control`
---------------

Used to periodically increment variable `brilho` and make readings over time.

Example - Reading
~~~~~~~~~~~~~~~~~

Making a reading on reactors 2 and 3 every 30 seconds:

.. code-block:: python
    
    import experiment_0 as e0
    
    C = e0.control()
    C.reactors = [2,3]
    C.time_read = 30
    C.start_read()
    
Cancelling the process:

.. code-block:: python

    C.read_thread.cancel()
    
Since `control` is a class, it is possible to create several objects controlling different microcontroller subsets at different time reading variations.

Example - Brilho
~~~~~~~~~~~~~~~~

Varying the microncontroller's variable `brilho` every minute for reactor 2:

.. code-block:: python

    import experiment_0 as e0
    
    C = e0.control()
    C.reactors = [2]
    C.time_brilho = 60
    C.brilho = 10
    C.start_brilho_ladder()

Canelling the process:

.. code-block:: python

    C.brilho_thread.cancel()
