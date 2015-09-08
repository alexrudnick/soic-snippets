If you're running Linux and not afraid of installing and configuring Apache, these instructions are for you.

If you have a Mac, and aren't afraid of configuring Apache, please see GettingStartedDevelopmentMac.

Otherwise, you probably want GettingStartedDevelopmentSimple.


---


In these instructions, we'll walk through getting set up so that you can run Snippets on your own computer, so you can help with development. It's written with Ubuntu in mind, but it should be easy to adapt to another Linux, and straightforward for other Unix-like systems. You'll also need Python 2.6, which you probably already have.

In general, replace "me" with your username.

# Checking out the code #

Go here for how to check out the code:
http://code.google.com/p/soic-snippets/source/checkout

Let's assume that you check it out to `~/soic-snippets`.

# Setting up Apache #

On Ubuntu, you'll need the package `apache2`. So type:
```
$ sudo aptitude install apache2
```

Now we have to make some small changes to your Apache configs...

```
$ sudo ln -s /etc/apache2/mods-available/userdir.conf /etc/apache2/mods-enabled/userdir.conf
$ sudo ln -s /etc/apache2/mods-available/userdir.load /etc/apache2/mods-enabled/userdir.load
$ sudo ln -s /etc/apache2/mods-available/cgi.load /etc/apache2/mods-enabled/cgi.load
```

Now we'll edit the `userdir.conf` file. Replace "gedit" with your favorite editor.

```
$ sudo gedit /etc/apache2/mods-available/userdir.conf
```

Just before the line that says `</IfModule>`, add this block:
```
        <Directory /home/*/public_html/cgi>
                AllowOverride None
                Options ExecCGI +FollowSymLinks
                AddHandler cgi-script .cgi
        </Directory>
```

Having made those changes, restart Apache.
```
$ sudo /etc/init.d/apache2 restart
```

# Setting up the database #
Right now, Snippets uses sqlite for its database, so while it may not be high-performance, it's certainly easy to set up.

Go into your soic-snippets directory and type:
```
$ ./makedbdir.sh
```

It may ask you for your password (possibly twice), because the script has to do a `sudo` to change the permissions of the database file so that Apache can use it.

# Making snippets available to the webserver #
Now we'll create a `public_html` directory in your home and make a link from that to your checkout of the Snippets code.

```
$ cd ~
$ mkdir -p public_html
$ chmod ugo+rx public_html
$ ln -s /home/me/soic-snippets/ /home/me/public_html/cgi
```

# Testing your setup #
Go here, replacing "me" with your username, of course:
http://localhost/~me/cgi

Hopefully that should work! Now edit the code and send us patches!