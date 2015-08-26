var app = require('app');
var BrowserWindow = require('browser-window');
require('crash-reporter').start();
var win = null;
app.on('window-all-closed', function() {
  app.quit();
});

app.on('ready', function() {
  var subpy = require('child_process').spawn(__dirname + '/pyvenv/bin/python', [__dirname + '/main.py']);

  win = new BrowserWindow({width: 800, height: 600});
  win.maximize();
  win.loadUrl('file://' + __dirname + '/index.html');

  // Emitted when the window is closed.
  win.on('closed', function() {
    win = null;
    subpy.kill('SIGINT');
  });
});
