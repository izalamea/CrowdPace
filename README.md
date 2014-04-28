CrowdPace
=========

I presented a method to estimate how fast a person can run a distance based on a recent race result. For details about this method please see http://frommorningside.blogspot.com/2014/04/let-crowd-suggest-pace.html and http://frommorningside.blogspot.com/2014/04/introducing-crowdpace.html

With this python script you can input the distance you have ran and the time it took you to ran it. Then you can enter another distance for which you want to know your estimated finishing time.

There are some caveats to keep in mind. If the time that you input was for a race on a hilly course, or during a hot day, then the estimated time will be longer than what you could run on ideal conditions or on a flat course. It's also important to keep in mind that CrowPace compares your time to the time of tens of thousands of runners to make the prediction. Some distances are more popular than others, this makes the prediction more accurate when comparing times between popular distances. As more data becomes available the estimated times will become more accurate. Finally, when calculating a time for a distance that is much smaller or much longer than the distance of the input race, please keep in mind that CrowdPace assumes that you have done equivalent training for both distances.
