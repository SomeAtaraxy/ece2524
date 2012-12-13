#BASH Scrip

*Due:* Sometime in the future

In this assignment you will construct a BASH script. This script with check for changes in a website that is specified as a command line argument.

##Problem 1
###First
You will first need to figure out how to create an infinite while loop that will continuously run the contained code until a 'CTRL+C' is received. There is an example of one [here](http://tldp.org/LDP/Bash-Beginners-Guide/html/sect_09_02.html). Also, do forget about your sha-bang!

You could also implement a check to make sure exactly one command line argument is passed for extra credit.


###Second
You will need to look through the 'man' page of 'wget' to determine usage and the proper flags needed to make the web page be stored in a particular file quietly. You will need to supply the command line argument to 'wget'. Save the downloaded html file into 'file1.html'.


###Third
You should remove the html tags from 'file1.html' file and save what is left over into 'file1'. Your best bet at accomplishing this would be to use the 'sed' command.


###Fourth
The terminal should sleep for some amount of time. For this assignment, you should make it sleep for 2 seconds, however in any other application, a higher sleep time would be beneficial for memory and power consumption.


###Fifth
Repeat the second and third step using 'file2'.


###Sixth
Use the 'man' page for 'diff' and determine what would be an appropriate output. The output should then be piped to 'sed' in order to achieve the final formatting.


##Testing
To test the script, you may use the site: [http://www.xav.com/time.cgi](http://www.xav.com/time.cgi)

Here is what a sample solution would produce:

	$ ./WebsiteChecker.sh http://www.xav.com/time.cgi
		2012-12-13 01:22:47  >  2012-12-13 01:22:49
		1355361767  >  1355361769


		2012-12-13 01:22:49  >  2012-12-13 01:22:52
		1355361769  >  1355361772


		2012-12-13 01:22:52  >  2012-12-13 01:22:54
		1355361772  >  1355361774


		2012-12-13 01:22:55  >  2012-12-13 01:22:57
		1355361775  >  1355361777


	^C
	$
