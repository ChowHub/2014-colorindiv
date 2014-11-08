Change Detection Task (modeled after Fukuda et al, 2010)
=====================
Data is located in `data`.

Important Columns
-----------------

* resp: z = match, slash = no match
* stim.probe: letters A-F are one class of shape, while M-R are different shapes.
  However, the current task only used 2 different patterns for each shape class (4 stimuli in total)
* stim.corr: correct shape and pattern
* block: Practice or number referring to block number
* RT: response time in seconds

Unfortunately, while I piloted the task and checked that trial presentation and probe were working as expected,
I didn't notice that the task was logging only the first 4 stimuli identities and positions until after collecting
all of the data.

