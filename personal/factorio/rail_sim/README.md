


2018-01-30

Need to rewrite the algorithm such that I can make a change that doesnt affect previously checked points and edges
so that I don have to check them again.

2018-01-31

Speed change should be done using acceleration events.
An acceleration event is a window of time and an acceleration.
Must make sure not to exceed the minimum and maximum speed.
The function to calculate point and edge windows will become much more complicated.

When an acceleration is added, all previously checked windows that end before the acceleration event begins are still
valid and dont need to be checked (as they are currently).

Need a way to avoid recursion error.
Could track windows that have been previously been passed and make sure that fixes to conflicts dont conflict with
windows that have already been passed.
This would require that PointWindow and EdgeWindow objects be persistent and unique.


