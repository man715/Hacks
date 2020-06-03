# headerGuessing
This script is a hacked together script to test a set of given headers (in the headers.lst file) agains an original request to see if adding th header along with an arbitrary value changes the response. Although there is a free BurpSuite Plugin that does this much better than I can with this script, I do not use BurpSuite and have not found a plugin for ZAP that does this. (If one exists, please let me know.)

## Options
-d or --delay allows you to set a delay if the repsonse is a 404. The script with retry the request three times before giving up on it (At the moment there is zero notifications of this issue.
-f or --file allows you to choose the requests file. By default the script will look in the same folder for a file named "request".
-o or --outputFile will allow you to name the file the script will write any findings to. By default it will create a file with the name of the host along with the date and time in the same folder as the script.

## Requirements
You must provide a request that is in the format that OWASP ZAP provides. Namely, the first line must have the full url after the request method.
The headers that you want to check for must be in a file named: "headers.lst" in the same direcotry the script is running in.

## Notes
This script does not implement any type of delay feature so you will probably get stopped by any rate limiting. It also does not do any waf detection or evasion

As of right now the boring_headers list is not being used for anything.

## Shoutout
I grabed the headers lists from https://github.com/PortSwigger/param-miner This does what I am doing here and much more and much better as a BurpSuite plugin. 

## Disclosure
Use this at your own risk. And do not do anything malicous with whatever information you may find out with this.
