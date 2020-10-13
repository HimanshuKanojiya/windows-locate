# Windows locate
Windows Locate is a python script that is mainly working to find your files and folders paths quickly in the windows. It searches through a database that is built by the Script manually via passing some commands & arguments and configuring the configuration file. 

As of now, windows Locate does not update the database in realtime, so each time, you need to run it to update the database.

Currently, Windows Locate is in an early stage, lot's of improvements need to do.

Windows Locate is a portable program, and it does not require any software or programs to run. You can run it directly via using cmd. To use this, you need to follow these steps:
1. Extract windows-locate.exe
2. Make sure that config.json is in the same folder.
3. Open config.json and give some required information like
  - In drive_path, you can give a directory path to index and save in the database.
  - Suppose you don't want to index some folders or path, then you can specify them in the disallow_paths.
  - If you want to index only some folders, you can specify them in the allowed_paths. If you don't give any paths there, then the indexer will consider drive_path and scan the     full drive.
  - If you want to index only folders and some pdf or other files, then you can specify an extension in allowed_extensions.
  - If you want to ignore some files formats to be indexed, then you can specify them in disallow_extensions
  - Important: Don't make changes in db_name

Format to specify things in config.json file, all required information will be saved between square braces [ ] and under double quotes:
1.  In drive_paths, disallow_paths, allowed_paths, the path should mention between " " (double quotes). Example:  "D:/"
2.  In allowed_extensions and disallow extensions, all extensions should mention between " " (double quotes) and without the prefix "." (dot).

Note: In paths, don't give backlash, if presents, then replace them with the forward-slash (/). If you have more than one path & extensions, then separate them with "," comma separator, and each of them should be in double-quotes.

For example, Please see the below sample of the config.json file.

Sample of config.json file:
{
    "drive_paths":["D:/","C:/"],
    "disallow_paths":["D:/i am programmer/code files"],
    "allowed_paths":["D:/i am programmer"],
    "allowed_extensions":["pdf","jpg","txt"],
    "disallow_extensions":["mkv","mp4"],
    "db_name":"local-db"
}


Windows Locate program inspired by the Linux Locate command. You can read more about it at https://en.wikipedia.org/wiki/Locate_(Unix)





