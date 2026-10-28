const fs = require('fs');
fs.mkdirSync('static/js', {recursive:true});
fs.copyFileSync('node_modules/lucide/dist/umd/lucide.min.js', 'static/js/lucide.min.js');
fs.copyFileSync('node_modules/lucide/dist/umd/lucide.min.js.map', 'static/js/lucide.min.js.map');
fs.copyFileSync('node_modules/lucide/LICENSE', 'static/js/lucide.LICENSE');
