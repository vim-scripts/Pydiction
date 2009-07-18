Pydiction 1.0 by Ryan Kulla (http://www.vim.org/scripts/script.php?script_id=850)
-------------

Pydiction is a filetype plugin for python files to be able to tab-complete Python code, including Python's keywords, standard library and even third-party libraries.  

It consists of three main files: 
    python_pydiction.vim -- This is the ftplugin you put in your non-system ftplugin directory. (i.e., ~/.vim/after/ftplugin/, on Unix or C:\vim\vimfiles\ftplugin\, on Windows)
    complete-dict -- This is a vim dictionary file that consists of Python keywords and modules. This is what python_pydiction.vim looks at to know which things are completeable.
    pydiction.py -- This is a Python script that was used to generate complete-dict. You can optionally run this script to add more modules to complete-dict to be able to complete them.


Installing
----------
Unix/Linux: Put python_pydiction.vim in ~/.vim/after/ftplugin/   (if that directory doesn't exist, create it. Vim will know to look there automatically.)
Windows: Put python_pydiction.vim in C:\vim\vimfiles\ftplugin  (assuming you installed vim in C:\vim\).

You may install the other files (complete-dict and pydiction.py) anywhere you want. For this example, we'll assume you put them in "C:\vim\vimfiles\ftplugin\pydiction\" (Do not put any file but python_pydiction.vim in the ftplugin\ directory, only .vim files should go there. It's ok to make a subdirectory in it though, like I just did.)

In your .vimrc file, first add the following line to enable filetype plugins:

    filetype plugin on

then make sure you set "g:pydiction_location" to the full path of where yo uinstalled complete-dict. Ie:

    let g:pydiction_location = 'C:/vim/vimfiles/ftplugin/pydiction/complete-dict'

You can optionally set the height of the completion menu by setting "g:pydiction_menu_height" in your vimrc. The default height is 15:

    let g:pydiction_menu_height = 20

By default, pydiction ignores case while doing Tab-completion. If you want it to do case-sensitive searches, then set noignorecase (:set noic).


Pydiction versus other forms of completion 
------------------------------------------
Pydiction can complete Python Keywords, as well as Python module names, and their attributes and methods. It can also complete both the fully-qualified module names such as "module.method(", as well as non-fully qualified names such as "method(".

Pydiction only uses the Tab-key to complete, uses a special dictionary file to complete from, and only attempts to do it on python files. This has the advantages of only requiring one keystroke to do completion and of not polluting all of your completion menus that you may be using for other types of completion, such as Vim's regular omni-completion, or other completion scripts that you may be running.

Since pydiction uses a dictionary file of possible completion items, it can complete 3rd party modules much more accurately than other ways. You have full control over what it can and can't complete. If it's unable to complete anything you can either use pydiction.py to automatically add a new module's contents to the dictionary or you can even manually add them using a text editor. The dictionary is just a normal text file, which also makes it portable across all platforms.  For example, if you're a PyQT user, you can add all the PyQT related modules to the dictionary file (complete-dict) by using pydiction.py.

Also, because pydiction uses a dictionary file, You don't have to import a module before you can complete it. Nor do you even have to have the module installed. This frees you up to use pydiction as a way of looking up what a module attribute is called without having to install it first.

Pydiction is smart enough to know when you're completing callable method or not and if you are, it will automatically insert an opening parentheses for you.

The Tab key will work as normally expected for everything else. Pydiction will only try to use it to complete python code if you're editing a python file and you first type part of some python code, as specified in complete-dict.

Pydiction doesn't even require that python support be compiled into your version of vim!

python_pydiction.vim
--------------------
Pydiction will make it so your the Tab key on your keyboard is able to complete python code (as long as the functionality has been added to complete-dict).

Version 1.0 of pydiction uses a new file called python_pydiction.vim, which is an ftplugin that only activates when you're editing a python file (e.g., you're editing a file with a ".py" extension or you've manually typed ":set filetype=python").  Past versions of pydiction didn't use a plugin and instead just required you to change the value of "isk" in your .vimrc, which was not desirable. Version 1.0 and greater do not require you to manually change the value of isk, it changes it for you safely by only setting it while you're doing tab completion (of python code only), and automatically changes isk back to its original value whenever tab completion isn't being activated.

Pydiction works by using Vim's omni-completion functionality by temporarily remapping the Tab key to do the same thing as I_CTRL-X_CTRL_K (dictionary only completion). This means, whenever you're editing a Python file and you start typing the name of a python keyword or module, you can press the Tab key to complete it. For example, if you type "os.pa" and then press Tab, pydiction will pop up a completion menu in vim that will look like:
    os.pardir
    os.path
    os.pathconf(
    os.pathconf_names
    os.path.
    os.path.__all__
    os.path.__builtins__
    os.path.__doc__
    ...
Pressing Tab again while the menu is open will scroll down the menu so you can choose whatever item you want to go with, using the normal omni-completion keys:
    <Ctrl-y> will accept the current word.
    <Space> will accept the current word and insert a space.
    <Ctrl-e> will close the menu and not accept any word.

pydiction.py
------------
This is the Python script used to create the "complete-dict" vim dictionary file.  I have created and bundled a default complete-dict for your use. I created it in Ubuntu 9.04 Linux, so there won't be any win32 specific support in it. You're free to run pydiction.py to add as many more modules as you want.  The dictionary file will still work if you're using windows, but it won't complete win32 related modules unless you tell it to.      

Usage: In a command prompt, run: 
    $ python pydiction.py <module> ... [-v]
You have to have python 2.x installed.


Say you wanted to add a module called "mymodule" to complete-dict, do the following:
    $ python pydiction.py mymodule

You can input more than one module name on the command-line, just separate them by spaces:
    $ python pydiction.py mymodule1 mymodule2 mymodule3

The -v option will just write the results to stdout (standard output) instead of the complete-dict file.

If the backfup file "complete-dict.last" doesn't exist in the current directory, pydiction.py will create it for you. You should always keep a backup of your last working dictionary in case anything goes wrong, as it can get tedious having to recreate the file from scratch.

If complete-dict.last already exists, pydiction will ask you if you want to overwrite your old backup with the new backup.

If you try to add a module that already exists in complete-dict, pydiction will tell you it already exists, so don't worry about adding duplicates. In fact, you can't add duplicates, everytime pydiction.py runs it looks for and removes any duplicates in the file.

When pydiction adds new modules to complete-dict, it does so in two phases. First, it adds the fully-qualified name of the module. For example:
    module.attribute
    module.method(

then it adds the non-fully qualified name:
    attribute
    method(

this allows you to complete your python code the way that you imported it in the first place. E.g.:
    import module
or:
    from module import method

Say you want to complete "pygame.display.set_mode". If you imported Pygame using "import pygame", then you can Tab-complete using:
    pygame.di<Tab>
to expand to "pygame.display.". Then type:
    se<Tab> 
to expand to "pygame.display.set_mode("

Now say you imported using "from pygame import display". To expand to "display.set_mode(" just type:
    display.se<Tab>

And if you imported using "from pygame.display import set_mode" just type:
    se<Tab>

Keep in mind that if you don't use fully-qualified module names that you may get a lot of possible menu options popping up and so you may want to use more than just two letters to try to narrow it down. 


complete-dict
-------------
Again, this is the vim dictionary file that python_pydiction.vim reads from and pydiction.py writes to. Without this file, pydiction wouldn't know what python keywords and modules it can Tab-complete.

complete-dict is only an optional file in the sense that you can create your own if you don't want to use the default one that is bundled with pydiction.  The default complete-dict gives you a major headstart as far as what you can Tab-complete because I did my best to put all of the Python keywords, standard library and some popular third party modules in it for you. 

It currently contains:

    Python keywords:

        and       del       for       is        raise    
        assert    elif      from      lambda    return   
        break     else      global    not       try      
        class     except    if        or        while    
        continue  exec      import    pass      yield    
        def       finally   in        print
    
    Most of the standard library and builtins:  __builtin__, __future__, os, sys, time, re, sets, string, math, Tkinter, hashlib, urllib, etc... 

    It also contains some popular third-party libraries: pygame, wxPython, twisted, numarray and OpenGL.

If you open complete-dict in your text editor you'll see sections in it for each module, such as:
 
    --- os module with "os." prefix ---
    os.EX_CANTCREAT
    os.EX_CONFIG
    os.EX_DATAERR
    ...

    --- os module without "os." prefix ---
    EX_CANTCREAT
    EX_CONFIG
    EX_DATAERR
    ...

if certain attributes seem to be missing, it's probably because pydiction removed them because they were duplicates. This mainly happens with the non-fully qualified module sections. So first try searching the entire file for whatever string you assume is missing before you try adding it. For example, if you don't see "__doc__" under "--- sys module without "sys." prefix ---", it's because a previous module, such as "os" already has it.
    
If you try to recreate complete-dict from scratch, you'll need to manually add the Python keywords back to it, as those aren't generated with pydiction.py.

