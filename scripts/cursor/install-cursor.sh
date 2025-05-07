# Remove any previously installed versions if they exist
sudo rm -rf ./squashfs-root || true
sudo rm -rf /opt/cursor || true
sudo rm -f /usr/share/applications/cursor.desktop || true
sudo rm -f cursor-*.AppImage

# Download the latest version
# curl -JLO https://downloader.cursor.sh/linux/appImage/x64
curl -JLO https://downloads.cursor.com/production/0781e811de386a0c5bcb07ceb259df8ff8246a52/linux/x64/Cursor-0.49.6-x86_64.AppImage

BASE_CURSOR_NAME=$(ls -1 | grep Cursor-0.49.6-x86_64.AppImage)
# Rename the downloaded file to cursor.AppImage
mv $BASE_CURSOR_NAME cursor-latest.AppImage

# Extract AppImage and fix permissions
chmod +x ./cursor-*.AppImage # Make executable
./cursor-*.AppImage --appimage-extract # Extract appimage
rm ./cursor-*.AppImage # Remove the appimage
sudo mv ./squashfs-root /opt/cursor # Move extracted image to program directory
sudo chown -R root: /opt/cursor # Change owner to root

# Find the actual path to chrome-sandbox (it might be in a different location)
SANDBOX_PATH=$(find /opt/cursor -name "chrome-sandbox" -type f)
if [ -n "$SANDBOX_PATH" ]; then
  sudo chmod 4755 "$SANDBOX_PATH" # Fix permissions for the sandbox file
  echo "Set permissions for sandbox at: $SANDBOX_PATH"
else
  echo "Warning: chrome-sandbox not found. This may affect application functionality."
fi

# Find the icon file (might have a different name)
ICON_PATH=$(find /opt/cursor -name "*.png" -o -name "icon.png" -o -name "cursor.png" -o -name "Cursor.png" | head -1)
if [ -n "$ICON_PATH" ]; then
  sudo chmod 644 "$ICON_PATH" # Make sure the app icon has permission to be viewed
  echo "Set permissions for icon at: $ICON_PATH"
else
  echo "Warning: cursor icon not found. Using a default path."
  ICON_PATH="/opt/cursor/resources/app/dist/icon.png" # Try common location
fi

# Fix directory permissions
sudo find /opt/cursor -type d -exec chmod 755 {} \; # Some directories are only accessible by root which prevents application from launching

# Create Desktop entry
cat > cursor.desktop <<EOL
[Desktop Entry]
Name=Cursor AI IDE
Exec=/opt/cursor/AppRun
Icon=${ICON_PATH}
Type=Application
Categories=Development;
EOL

# Set permisisons for .desktop file and move it to the correct directory
sudo chown root: cursor.desktop
sudo chmod 644 cursor.desktop
sudo mv cursor.desktop /usr/share/applications

echo "Installation complete!"