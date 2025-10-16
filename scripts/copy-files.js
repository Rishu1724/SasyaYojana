import { copyFileSync, existsSync, mkdirSync } from 'fs';
import { join } from 'path';

// Files to copy to dist directory
const filesToCopy = [
  'public/_headers',
  'public/_redirects',
  'public/404.html',
  'public/robots.txt'
];

// Create dist directory if it doesn't exist
const distDir = 'dist';
if (!existsSync(distDir)) {
  mkdirSync(distDir);
}

// Copy files
filesToCopy.forEach(file => {
  const source = join(process.cwd(), file);
  const destination = join(process.cwd(), distDir, file.split('/').pop());
  
  if (existsSync(source)) {
    copyFileSync(source, destination);
    console.log(`Copied ${file} to ${destination}`);
  } else {
    console.warn(`File not found: ${source}`);
  }
});

console.log('File copying completed!');