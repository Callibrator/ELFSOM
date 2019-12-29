# ELFSOM

<p align="center">
  <img src="/res/logo.png">
</p>

Easy Launcher For Servers Of Minecraft. ELFSOM! it is a way of allowing server owners distribute mods to their players!

<p align="center">
  <img src="/res/window.png">
</p>

What basically Allows you to do, is updating the mods of your users dynamically with a launcher that you will be able to control! You will be able to remove & add mods like it is some kind of RPG Game!

Note that this does not replace the old minecraft launcher, it is just as launcher for the launcher! But before launching the minecraft launcher the ELFSOM (This Launcher) will sync mod files with that of your server!

# How can I use this on my server?

Great Question! First you will have to setup the server instance of the launcher!

This will allow the launcher to connect to the server and check/sync/update the necessary files! After that you do not have to do anything else!

# Setting Up The Server

Now, there are a lot of ways to set up this server, one can be as a service on linux the other one can be way simpler like just double clicking on an icon...

For this demostration we are going to do it the simple way! Although, it is recommended to deploy it the "normal" way at some point! This is the simplest practise but not the best one!

### We are going to need python 3.x For the Server

You can download python 3.x for windows from [here](https://www.python.org/downloads/windows/).

After downloading and installing python3. The next thing you will have to do will be to execute server.py (inside server folder) with the following command:
`python.exe server.py`

Done! Now the server is running and it is ready to use! It was that simple :P 

Well, Let's now see what we actually did!

By starting the server, we are letting clients to connect to us and download our minecrafts files (configurations files, mods, forge version etc!)

### But how do we choose what files we want our users to download?

The answer to that questions is the following: All minecraft files that you want your users to have inside their minecraft working directory, should be placed inside the `minecraft_files folder`

More Specifically!

A somewhat normal minecraft_files folder should have the following subfolders and files:

- config
- libraries
- mods
- resourcepacks
- versions
- launcher_profiles.json


Let's break down the purpose of each folder!

- Config, Contains all configuration files needed for mods
- libraries, contains all libraries that are needed by either forge or mods
- mods, all mod files
- resourcepacks, obviously any resourcepack you would like to share with your users
- versions This one is tricky! It contains the forge version that is needed by your server
- launcher_profiles.json Be carefull with this file! Do not copy paste the file from your launcher there! It should act as a simple guide for only few parameters to help the user start minecraft more easily

Example of launcher_profiles.json

```
{
  "profiles": {
    "(Default)": {
      "name": "(Default)",
      "lastVersionId": "1.7.10-Forge10.13.4.1558-1.7.10"
    }
  }
}
```

Notice that I only have some parameters for the default profile and what version should be pre-selected! Nothing else!

### How Should I fresh Install A forge Version?

The best way to do it is to clean/remove all files inside the minecraft_files folder.

After that, create a simple file and name it `launcher_profiles.json`
If you have no idea what to put in there put the following:
```
{
  "profiles": {
    "(Default)": {
      "name": "(Default)",
      "lastVersionId": "1.7.10-Forge10.13.4.1558-1.7.10"
    }
  }
}
```

Download the forge windows installer from their official website, Select install client and direct the installer to the minecraft_files folder and then install it!
That was it. You have now installed forge and all your users will have that same version on their minecraft instance if they start it from your (ELFSOM) launcher!

Now you can start adding mods and making any configurations you want! You will probably copy the mods that exist inside your server mods folder to minecraft_files/mods and you will do the same with configurations!

You can make any changes you want to the `launcher_profiles.json` and you are good to go!
Although this is optional, again if you have no idea what to put there put the following (remove the data that are already there):
```
{
  "profiles": {
    "(Default)": {
      "name": "(Default)",
      "lastVersionId": "1.7.10-Forge10.13.4.1558-1.7.10"
    }
  }
}

```

* Replace "1.7.10-Forge10.13.4.1558-1.7.10" with your version of forge!!!

### Important Notes!!!

The server.py (or server, in general) needs restart every time you change the files! I designed it this way because I believed it uses less resources and therefore it is better optimized!

Do not place your minecraft server inside the minecraft_files folder. Unless you want all your users to end up with a copy of the server!!!

You should copy on the launcher's server the mods & other files, do not mix everything together, it is a bad idea!!!

### Configuration!

Obviously, you are wondering if you are able to configure parts of the server!
Anything that can be configured is located inside the config/config.py

`config.py`

| Variable  | Purpose |
| ------------- | ------------- |
| host  | The host of the launcher server  |
| Port  | The port of the launcher Server  |
| max_clients_in_queue  | Maximum Clients that can wait in queue to connect to the server in case it maxes out  |
| minecraft_files_path  | The path to the folder that contains all the necessary files that will be retrieved from the client |
| file_buffer_size  | Maximum size of buffer in bytes for sending files to clients|


# Client Preparations

The way the client works is simple! It connects to the launcher (ELFSOM) server and downloads locally (in ./minecraft folder) all the necessary files that the server owner have carefully placed with care there!

After that it launches the Minecraft Launcher but replaces the working dir (temporarily obviousy, we do not want to cause any damage to the original files of the game!) with the directory that the files are downloaded! Thereby we have all the necesarry files ready (mods,configs,maybe user settings etc)

All necessary files are synced everytime the launcher starts to ensure that every user will be kept up to date!

### Configuring the Client for your users!

Firstly you need a compiled version of the client (unless you want your users to run it with python every time!) You can either download a compiled version or just compile it yourself

You can download the latest compiled release of launcher from [here](https://github.com/Callibrator/ELFSOM/releases/tag/V1.0).

After you have your compiled version of the client, you have to configure it!
You can make any changes to the configuration by chaninging the json file name config.json inside the config folder of the client!

Let's examine the json file!

On first look, it looks like this
```
{
  "server_host":"127.0.0.1",
  "port":3741,
  "window_title":"ELFSOM Laucnher",
  "server_url": "https://minecraft.gamepedia.com/Minecraft_launcher",
  "minecraft_files_skip_checks":["/saves","/logs","/versions/1.7.10","/assets","/libraries", "/servers.dat", "/options.txt"],
  "minecraft_files_download_only":["/launcher_profiles.json"],
  "launcher_extra_buttons":[{"name":"Website", "type":"link", "url":"https://www.google.com"}],
  "minecraft_server_details":"127.0.0.1:25565"

}
```


| Variable  | Purpose |
| ------------- | ------------- |
| server_host  | The host of the launcher server (your server)  |
| port  | The port of your launcher server  |
| window_title  | The tile of the window of ELFSOM Launcher  |
| server_url  | The url that will be loaded when the launcher starts, usually a news page, if you do not know what to put there, try monty python youtube vids xD  |
| minecraft_files_skip_checks  | Those files will not be removed if do not exist on the server but they will be updated if there are on the server and they are not the same! |
| minecraft_files_download_only  | Those files will be downloaded only if they do not exist locally, if they exist (Even if they are different in the server) they will not be changed! |
| launcher_extra_buttons  | Extra buttons for the launcher |
| minecraft_server_details  | Server details such as ip:port of your minecraft server |


Most of the stuff here are self explenatory such as server_host,port,window_title

I will leave some notes for the following:
* minecraft_files_skip_checks There are files such as saves that you do not want to be deleted if they do not exist on the server. Those files (or folders) can be included here! Such files usually are user-specific configs (such as servers.dat or gui options that exist inside options.txt or the most important of all! saves!) Keep in mind though, if files with the same location exist on the server, the clients file will be updated normally! as a result the clients files will be replaced with the server files!
* minecraft_files_download_only There are files that exist on the server but are different in each client too. This files will be contianed here! What it does is the following: if the file does not exist, it will download it normally but if exists, even if it is different from the one on the server, it wont update it! This can be usufull for default configurations while still allowing the users the freedom to make local changes! The best example is the launcher_profiles.json! We can use it to make the life of the user easier by pre-selecting versions but still allowing him to play with minecraft arguments if he likes!
* launcher_extra_buttons This is usefull because you can add buttons to your server web site or an online eshop with minecraft skins or even products! You can have multiple buttons

### PyInstaller Hint

```
pyinstaller --onefile --hidden-import PyQt5.sip --windowed -i icon.ico .\launcher.py

```
