# Rave

## What's Rave?

Rave is a set of tools to create a commenting system server.

For that, Rave use these tools:

  * Isso, a personal commenting system that is an alternative to the famous Disqus
  * Django, a web framework that permit to generate customized website easily and quickly

## Installation

For now, here is what is planned to make Rave being a reality:

  * Nginx installation and configuration
  * Rave Django App installation and configuration
  * Docker installation
  * Fetching Rave Dockerfile
  * Compiling new image of Rave Dockerfile
  * Launching Rave and test it

NB:

  * Add user in docker group so that it can create dockers
  * Add chmod 755 on /etc/nginx/rave
  * Edit sudoers with ```sudo visudo``` and add these line:

```
username ALL=NOPASSWD: /usr/sbin/nginx
```

Be sure to adapt by changing *username* by the username that will launch the script.

### Nginx Installation

Nginx was choosed by default for our project, but you can use another one like [HAProxy](http://www.haproxy.org/).

First install it:

    apt-get install nginx

Then create a directory named *rave*:

    sudo mkdir /etc/nginx/rave

Make it available for the user that will launch the django application (for an example, www-data user):

    sudo chown www-data /etc/nginx/rave

And finally add the user to sudoers to allow it to reload nginx:

    sudo visudo

And add this line (in this example, the user is www-data):

```
www-data ALL=NOPASSWD: /usr/sbin/nginx
```

We need now a directory in which all users will be created.

### Fetch this repository as directory for web result

Time to fetch rave so that you can have the application.

I suggest you to fetch it in **/srv/www/ravecomment**, but you can choose another one:

    sudo mkdir -p /srv/www
    sudo git clone http://github.com/blankoworld/rave-comment /srv/www/ravecomment
    sudo chown www-data:www-data /srv/www/ravecomment -R

### Configuring the Django App

FIXME: explain how to configure the file that give information for creating dockers, etc.

You can now configure Nginx to point out the Django App directory.

### Nginx configuration

To simplify the installation, we create a default nginx configuration in this repository. You can use it and **adapt it**:

    sudo cp /srv/www/ravecomment/conf/nginx.general.conf /etc/nginx/sites-enabled/ravecomment

Then edit the file **/etc/nginx/sites-enabled/ravecomment** and change the serveur_name line and the root line, for an example:

```
server_name "comments.something.com";
root /srv/www/ravecomment/app;
```

You just have to relaunch your Nginx and it will work.

## TODO

Talk about:

  * Docker management system (to relaunch docker container, etc.)
  * Rave Django App configuration possibilities (for email, dockers, etc.)

## License

The project is under the [MIT License](http://opensource.org/licenses/MIT).

## Contact

If you encount any problem, please explain it here : https://github.com/blankoworld/rave-comment/issues

Some info are also available in [our Wiki](https://github.com/blankoworld/rave-comment/wiki).

Default website : http://github.com/blankoworld/rave-comment
