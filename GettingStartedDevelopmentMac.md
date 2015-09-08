# Introduction #

Here's how to get your development environment set up on a Mac, particularly Snow Leopard. These instructions are courtesy of the illimitable [Mark Wilson](http://www.cs.indiana.edu/~mw54/).

# Details #

Check out the code [as described](http://code.google.com/p/soic-snippets/source/checkout).  Let's assume you check it out to `~/soic-snippets/` -- if you check it out to another location, just use that location wherever we use `~/soic-snippets/`.

Mac OS X Snow Leopard comes with an Apache webserver installed;  however, its configuration is somewhat different to accommodate OS X.

To turn on the webserver, open System Preferences and navigate to the Sharing screen.  Check the "Web Sharing" checkbox if it isn't already checked.

To make sure your webserver is running, you can type "http://localhost" into your browser's address bar.

Once you have your browser running, edit the `httpd.conf` file.  To do this, open Terminal and enter the following (replace "nano" with your favorite editor).  You will need to enter your password for administrative access.
```
sudo nano /private/etc/apache2/httpd.conf
```

Make sure this line is present and uncommented (it should be by default).
```
LoadModule userdir_module libexec/apache2/mod_userdir.so
```

As an aside, while you're in here, if you're just going to use your Mac as a sandbox or development machine, you may want to limit access to your webserver from other computers.  To have your machine serve only to itself, change the ServerName line and the Listen line:
```
ServerName localhost
...
Listen 127.0.0.1:80
```

Now, edit the httpd-userdir.conf file.
```
sudo nano /private/etc/apache2/extra/httpd-userdir.conf
```

By default, user-specific webpages are served from the users' `Sites/` directories.  That is, if someone browses to localhost/~USERNAME/, the system looks in `/Users/USERNAME/Sites/` for files to serve.  Let's assume you want to serve the snippets system from `/Users/USERNAME/Sites/snippets/` -- again, replace with the location of your choice from here on out.

To configure users' individual web directories, you can set up individual `USERNAME.conf` files.  To allow this, add or uncomment the following line from httpd-userdir.conf if it's not already present:
```
Include /private/etc/apache2/users/*.conf
```

Now edit your `USERNAME.conf`.
```
sudo nano /private/etc/apache2/users/USERNAME.conf
```

Your conf file should contain a Directory block something like this (add it if it doesn't).
```
<Directory "/Users/USERNAME/Sites/">
    Options Indexes MultiViews +FollowSymLinks
    AllowOverride None
    Order allow,deny
    Allow from all
</Directory>
```

Then add this Directory block below that:
```
<Directory "/Users/USERNAME/Sites/snippets/">
        Options +ExecCGI
        AllowOverride AuthConfig
        AddHandler cgi-script .cgi
</Directory>
```

Note that the "+FollowSymLinks" option is less safe and should be placed at the lowest possible level of the directory tree;  however, that's in the parent directory of our snippets/ directory which will be linked to the source directory.  The "AllowOverride AuthConfig" directive is necessary only if you want to play around with multiple users.

That's it for Apache configuration!  Now exit the editor and restart Apache:
```
sudo apachectl restart
```

Now we need to create the database file.  Mac uses "www" as the user and group for Apache execution by default.  Change to your code directory (~/soic-snippets/ in our example) and edit makedbdir.sh:
```
nano makedbdir.sh
```

Change the line "sudo chgrp -R www-data db" to this:
```
sudo chgrp -R www db
```

Exit the editor and run makedbdir.sh:
```
./makedbdir.sh
```

Now move up one directory and change the group for the entire source tree:
```
cd ../
chgrp -R www soic-snippets
```

Now all we have to do is link the directory we want to serve from to the source directory:
```
ln -s ~/soic-snippets /Users/USERNAME/Sites/snippets
```

Now you should be able to visit your own copy of the snippets site by visiting: http://localhost/~USERNAME/snippets/index.cgi