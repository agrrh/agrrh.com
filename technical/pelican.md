Title: Pelican - pretty and automated blog
Date: 2016-09-27 19:32
Tags: pelican, git, web, javascript, css

Few words about blog platform I'm using.

[Pelican](http://blog.getpelican.com/) is a static site generator, written in Python and using great [Jinja2](http://jinja.pocoo.org/docs/dev/) template engine.

I store data in a [GitHub repo](https://github.com/agrrh/agrrh.com), so backups and changes history are always there for me or for any visitor, who is interested in.

The way static markdown text files become pretty HTML pages are quite simple, I just executing a single command:

```plain
# "source" is a path where text is stored
pelican source
```

... which results in generated `output` directory.

## Prettify

I am using custom `pelican-bootstrap3` theme, a `tag-cloud` plugin and a custom JavaScript code to zoom-in/out the images.

First, download the themes:

```bash
git clone https://github.com/getpelican/pelican-themes.git
```

Then, take care about the plugins:

```bash
git clone https://github.com/getpelican/pelican-plugins.git
```

Now place the link to the configuration file, which is stored in your repository and is requred by HTML generation routine:

```
ln -s source/pelicanconf.py pelicanconf.py
```

So, the final directory layout should be the following:

```plain
.
├── source/
├── pelican-themes/
├── pelican-plugins/
└── @pelicanconf.py -> source/pelicanconf.py
```

This is when you are ready to run the build command, `pelican` will create the `./output` directory and this should be the one your web-server points to.

## Deploy

The simplest deploy script could look like this one (don't forget to manually clone the repo to the `${PATH_BASE}/${PATH_RAW}` for the first time):

```bash
#!/bin/bash

PATH_BASE=/var/www/example.org
PATH_RAW=source

cd ${PATH_BASE}/${PATH_RAW}
git pull

cd ${PATH_BASE}
rm -rf ./output
pelican ${PATH_RAW}

chown -Rf nginx: ${PATH_BASE}

service nginx reload
```

You could save this as Git `post-update` hook or something.

## Customizing the view

Feel free to edit the theme static files. For example, I did so to enable on-click zoomig for images.

First, let's tell the browser, that images with `alt=preview` property should be treated as thumbnails. We want to make them small:

**./pelican-themes/pelican-bootstrap3/static/css/style.css**

```css
img[alt=preview] {
    width: 180px;
    cursor: pointer;
}
```

Now telling browser to toggle full-width property for specific elements on click:

**./pelican-themes/pelican-bootstrap3/static/js/custom.js**

```javascript
$(document).ready(function(){
   var flag = true;
   $('img[alt=preview]').click(function() {
       $(this).stop().animate({width: (flag ? "100%" : "180px") }, 'fast');
       flag = !flag;
   });
 });
```

Enabling JavaScript by adding it to the page:

**./pelican-themes/pelican-bootstrap3/templates/base.html**

```html
<script src="{{ SITEURL }}/{{ THEME_STATIC_DIR }}/js/custom.js"></script>
```

Then I'm just marking the images with "preview" tag:

```markdown
![preview]({filename}/media/photo.jpg)
```

And voila! You can resize image to full width available by clicking on them.
