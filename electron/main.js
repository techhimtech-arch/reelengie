const { app, BrowserWindow } = require('electron');
const path = require('path');
const { spawn } = require('child_process');

let mainWindow;
let pythonProcess = null;

function startPythonBackend() {
  let backendPath;
  if (app.isPackaged) {
    backendPath = path.join(process.resourcesPath, 'app.asar.unpacked', 'backend', 'dist', 'main.exe');
    // If not using asar unpacked, it might just be:
    // backendPath = path.join(__dirname, '../backend/dist/main.exe');
    // But usually electron-builder puts binaries outside asar if configured, or just inside.
    // For simplicity, let's use the relative path since we bundled it in "files"
    backendPath = path.join(__dirname, '../backend/dist/main.exe');
    pythonProcess = spawn(backendPath);
  } else {
    backendPath = path.join(__dirname, '../backend/app/main.py');
    // In dev we assume python is in PATH
    // Actually we should use the venv python if possible, but python is fine for now
    pythonProcess = spawn('python', [backendPath]);
  }

  pythonProcess.stdout.on('data', (data) => {
    console.log(`Backend: ${data}`);
  });

  pythonProcess.stderr.on('data', (data) => {
    console.error(`Backend Error: ${data}`);
  });
}

function createWindow() {
  mainWindow = new BrowserWindow({
    width: 1200,
    height: 800,
    minWidth: 900,
    minHeight: 600,
    title: "Reel Engine",
    webPreferences: {
      preload: path.join(__dirname, 'preload.js'),
      contextIsolation: true,
      nodeIntegration: false
    }
  });

  const devServerUrl = process.env.VITE_DEV_SERVER_URL;
  
  if (devServerUrl) {
    // Development mode: load Vite dev server
    mainWindow.loadURL(devServerUrl);
    mainWindow.webContents.openDevTools();
  } else {
    // Production mode: load built React app
    mainWindow.loadFile(path.join(__dirname, '../frontend/dist/index.html'));
  }

  mainWindow.on('closed', () => {
    mainWindow = null;
  });
}

app.whenReady().then(() => {
  startPythonBackend();
  createWindow();

  app.on('activate', () => {
    if (BrowserWindow.getAllWindows().length === 0) {
      createWindow();
    }
  });
});

app.on('window-all-closed', () => {
  if (process.platform !== 'darwin') {
    app.quit();
  }
});

app.on('will-quit', () => {
  if (pythonProcess) {
    pythonProcess.kill();
  }
});
