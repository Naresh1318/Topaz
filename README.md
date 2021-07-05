# Topaz
[![Actions Status](https://github.com/Naresh1318/topaz/workflows/Topaz/badge.svg)](https://github.com/Naresh1318/Topaz/actions)

<p align=center>
    <img src="https://files.naresh1318.com/public/topaz/index.png" alt="simplyServe"/>
    <p align="center"> <b>A configurable, easy to maintain personal website</b> </p>
</p>


**Live example**: https://naresh1318.com

After working on a project the last thing I usually think of is updating my personal website. 
Adding links, images, description and pushing changes to the server every single time I work 
on something new is kinda boring especially if you are lazy like me. What do we do when we're lazy?
we automate things. Thereby giving us time to, idk, complain about our laziness. I designed Topaz 
to automatically update as much of my website as possible.

### Recent updates:
* Added ability to write and publish blogs
* Revamped home, project and blog pages

## Here's what it can currently do:

1. Automatically fetch public repos from your github account

<p align=center>
    <img src="https://files.naresh1318.com/public/topaz/projects.png" alt="simplyServe"/>
    <p align="center"> <b>Projects from github</b> </p>
</p>

2. Admin page that lets you easily add blogs and publication details

<p align=center>
    <img src="https://files.naresh1318.com/public/topaz/admin.png" alt="simplyServe" width="400px"/>
    <p align="center"> <b>Add blogs and publications details</b> </p>
</p>

3. Choose what gets shown

<p align=center>
    <img src="https://files.naresh1318.com/public/topaz/admin_projects.png" alt="simplyServe"/>
    <p align="center"> <b>Manage what gets shown</b> </p>
</p>

4. Ability to modify/write content using markdown

5. Customize website by editing `theme.json` file

```json
{
  "name": "Naresh Nagabushan",
  "profile_picture_url": "https://files.naresh1318.com/public/Me/IMG_2831_low.jpg",
  "nav_bar_footer": {
      "github": {
        "link": "https://github.com/Naresh1318",
        "icon": "fa-github"
      },
      "medium": {
        "link": "https://medium.com/@rnaresh.n",
        "icon": "fa-medium"
      },
      "linkedin": {
        "link": "https://www.linkedin.com/in/naresh-nagabushan-2946b013a",
        "icon": "fa-linkedin"
      },
      "twitter": {
        "link": "https://twitter.com/Naresh_Reddy_",
        "icon": "fa-twitter"
      }
  }
}
```
6. Mobile friendly (currently working on this)

<p align=center>
    <img src="https://files.naresh1318.com/public/topaz/mobile.png" alt="simplyServe" width="50%"/>
    <p align="center"> <b>Mobile friendly</b> </p>
</p>

## Here are the things that I'm still working on:

* Ability to publish and write blogs using markdown
* 



## Install
Super easy as always. Clone before you start!

1. Edit `data/theme.json` file to reflect what you want. Here's another example:

```json
{
  "name": "Naresh Nagabushan",
  "profile_picture_url": "https://files.naresh1318.com/public/Me/IMG_2831_low.jpg",
  "nav_bar_footer": {
      "github": {
        "link": "https://github.com/Naresh1318",
        "icon": "fa-github"
      },
      "medium": {
        "link": "https://medium.com/@rnaresh.n",
        "icon": "fa-medium"
      },
      "linkedin": {
        "link": "https://www.linkedin.com/in/naresh-nagabushan-2946b013a",
        "icon": "fa-linkedin"
      },
      "twitter": {
        "link": "https://twitter.com/Naresh_Reddy_",
        "icon": "fa-twitter"
      }
  }
}
```

2. Generate a github token by visiting this link: https://github.com/settings/tokens 
and select the repo checkbox. Give it a name if you want and copy the token.

3. cd into the project root dir and paste the key into a keys.txt file
```bash
echo "token <your key>" >> keys.txt
```

**Note: ** Do not ignore the "token " prefix

4. Install docker if you don't have it already using this link: 
https://docs.docker.com/install

5. Add an admin account

   * Modify `Dockerfile` under project root:

     ```bash
        ENV USERNAME "<username>"
        ENV PASSWORD "<password>"
     ```

4. Build your image:

   ```bash
   docker build -t <image name>:<tag> .
   ```

   Here's how mine looks:

   ```bash
   docker build -t topaz:latest .
   ```

5. Run your image:

   ```bash
   docker run -p <port to forward>:5000 -v absolute path to data dir in project:/app/data/ <image name>:<tag>
   ```

   Here's mine:

   ```bash
   docker run -p 4000:5000 -v /home/naresh/Projects/Topaz/data/:/app/data/ topaz:latest

6. Finally, go to `localhost:<port forwarded to>` on your browser

7. You can access the login page using `localhost:<port forwarded to>/login`. Example `localhost:4000/login`. 
Login using the username and password you setup earlier.

**Note:** *You could also modify the `docker-compose.yml` file to install topaz*


## Concluding thoughts
1. Feel free to do a pull request if you fix bugs
2. Email me rnaresh.n@gmail.com if you have any suggestions!
