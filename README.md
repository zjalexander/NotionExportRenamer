# NotionExportRenamer
Windows users might have problems unpacking Notion exports with multiple nested pages. 
If you are expanding a .zip and get a 'Filepath too long' error, you can try using the [MAXPATH registry setting](https://learn.microsoft.com/en-us/answers/questions/4254366/why-isnt-long-paths-enabled-by-default-in-windows?forum=windows-all&referrer=answers) to workaround this error.
Or, you can use this utility python script to strip the pseudo-guid from files to allow you to continue exporting (which will break links, but also might make it nicer for reimporting into other tools).

## Prerequisites

This is a Python script and fixes a problem with Windows.
You will need Python, installed on Windows, which is [An Experience](https://learn.microsoft.com/en-us/windows/python/faqs#what-is-py-exe-). 

Make sure you can open a cmdline and invoke either 'python3' or 'py'.

To explicitly use with a Notion export file, first [export your entire workspace](https://www.notion.com/help/export-your-content).
Download and unzip that file. 
Note the path of the unzipped location.

## Usage
To run the utility, download or copy the script to ```renamer.py```

You may replace 'py' with 'python3', [depending](https://learn.microsoft.com/en-us/windows/python/faqs#what-is-py-exe-).

```py script.py "C:\path\to\your\directory"```

This will do a test and let you know what the results of the rename will be.

```py script.py "C:\path\to\your\directory" --no-dry-run```

This will rename the files for real. Do the dry run first. 
