Smooth the graph
================
Because the graphs have many spikes it’s hard to determine trends without a processing step.
A easy way is to eliminate local maxima and minima is replacing the value with the mean of the neighbours

SAX Conversion
==============

SAX Conversion converts a series of continuous data into a discrete string of symbols from a given alphabet.
1 2 3 4 5 => abcdd
	
It uses the normal distribution of the given values to create the conversion. By intuition it splits the normal distribution curve in len(alphabet) chunks

For the alphabet [a, b, c, d] d will label the highest values.

Another parameter used is sconds/symbol which says how many seconds from the series will be converted to a symbol.

Determine local maxima using SAX conversion
===========================================

To determine if a timestamp is a candidate for being part of a spike I use a sliding window of H hours and count how many times a timestamp is a ‘d’ in that window (high value in that window)

When the value is a 'd' in all the windows it becomes a candidate.

Determine Spikes
================
Spikes will be the timestamps that have a smoothed value larger than the mean of all local maxima from the initial series.

Example for a graph
http://swarm.cs.pub.ro/~mbivol/fig.png

 - green - actual series
 -  blue - smoothed series
 -  red line - treshold
 -  red squares - candidates
