# Assets sources

Assets sources located in `assets-src` folder.

Scripts and styles are compiled to `static/generated-assets/{js,css}` folders.

Template blocks are copied to `static/blocks` folder.

To run in watch/dev mode you need to start in 3 consoles:

```
npm run start-django
npm run gulp-assets-watcher
npm run livereload-assets-server
```

To just update all assets, run:

```
gulp-assets-update
```
