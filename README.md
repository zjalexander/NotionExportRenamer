# NotionExportRenamer
When exporting from Notion, there are two problems:
1) Notion adds psuedo-GUID strings to files and links, which looks messy on reimport
2) These identifier strings might cause Windows users to have problems unpacking Notion exports with multiple nested pages. 

If you are expanding a .zip and get a 'Filepath too long' error, you can try using the [MAXPATH registry setting](https://learn.microsoft.com/en-us/answers/questions/4254366/why-isnt-long-paths-enabled-by-default-in-windows?forum=windows-all&referrer=answers) to workaround this error.

Or, you can use this utility python script, which **removes garbage characters from filenames and links**. 

This might break links, especially if you have multiple pages with the same name, but also might make it nicer for reimporting into other tools.


## Prerequisites

This is a Python script and fixes a problem with Windows file paths.
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
