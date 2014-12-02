# Rave

## What's Rave?

Rave is a set of tools to create a commenting system server.

For that, Rave use these tools:

  * Isso, a personal commenting system that is an alternative to the famous Disqus
  * Django, a web framework that permit to generate customized website easily and quickly

## Installation

For now, here is what is planned to make Rave being a reality:

  * Nginx installation
  * Fetching Rave Comment
  * Configuring it
  * Nginx configuration
  * Docker installation
  * Fetching Rave Dockerfile
  * Compiling new image of Rave Dockerfile
  * Reloading Nginx configuration
  * Launching Rave and test it

### Docker Installation

First you need to install Docker. You can [read the official installation documentation](https://docs.docker.com/installation/) to install it regarding your GNU/Linux distribution or your server.

Then, add the user that will launch the Django App to the docker group so that it can create docker (for an example with *www-data* user):

    sudo gpasswd -a www-data docker

Now, you can fetch the Isso Docker image:

    docker pull bl4n/isso

Enjoy, you have a docker image for Rave new users!

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

## Troubleshooting

### DNS resolver problem

You can have this problem on Ubuntu servers:

```
Exception: Docker problem: WARNING: Local (127.0.0.1) DNS resolver found in resolv.conf and containers can't use it. Using default external servers : [8.8.8.8 8.8.4.4]
```

To fix that, edit the **/etc/default/docker** file and uncomment this line:

    DOCKER_OPTS="--dns 8.8.8.8"

Then relaunch Docker:

    sudo restart docker

It will now permit to Docker to relaunch with right DNS parameters.

### Cannot access locally to the docker file

If this command return something, you will probably have a docker bridge:

    ifconfig|grep docker

If this is the case, I suggest you to get the IP of this interface.

For an example, my interface seems to be called **docker0**, so I do:

    ifconfig docker0| head -n2

It returns me:

```
docker0   Link encap:Ethernet  HWaddr 00:00:00:00:00:00
          inet addr:172.42.42.1  Bcast:0.0.0.0  Mask:255.255.0.0
```

So you should adapt **conf/nginx.conf** file with this address, like this:

    proxy_pass http://172.17.42.1:$port;

And relaunch the Django App (nginx).

Pay attention that if you already have some nginx configuration with Docker containers that are running, you should adapt all configuration files in /etc/nginx/rave/ directory.

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
