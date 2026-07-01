## Horizons Timeline journal

1. Set up the project and initialized git
2. Read the Badgeware docs and setup the Python file
3. Created a class for Progress Bars
4. Tested the class and it didn’t work
5. Created a simple grayscale icon version of the Horizons logo and resized it
6. Put it onto my badge - it doesn’t do anything, just crashes :(
7. Realized I forgot the run(update) which triggers the code - finally, something displays!
8. Got the outline and white fill to display, but the progress fill itself is off
9. Realized I have to translate it to 0,0, then transform, then translate back
10. That didn’t work either so I had to just redraw the shape every time
11. There was a small cutout so I had to use a normal rectangle instead of rounded for the fill, but got it to work!
12. Wrote a calculate percentage time until event function (AI helped me figure out the formula)
13. Got the Horizons logo to show up
14. It works when running from the IDE now but not when I launch it from the badge’s menu 
15. Wrote a function to calculate the hours & days left to the event
16. Used this function to show the days & hours remaining above the time bar
17. Wrote a function to get Hackatime project details from the API
18. Created an inherited class (learned about this for the first time) of progress bar specifically to show Hackatime projects
19. Got this to work!
20. Added text for the Hackatime project status
21. Wrote a function to create a key with project name, hours and color
22. Added an outline to the boxes and rearranged the page to make sure everything fits!
23. Added a feature to wrap text of the key onto the next line
24. It didn’t launch from the Home Screen (I struggled with this for the longest time) so I re-copied the file, ignoring git related files and then it worked!
25. Fixed the RTC sleep/wake cycle
26. Wrote the README and shipped!
