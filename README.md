# Song Info Finder - User Guide

🎵 **Find and edit song information for your MP3 files automatically!**

Song Info Finder is a simple web application that helps you find missing song information (like artist, album, title, etc.) for your MP3 files and save it directly to the files. It searches the iTunes database to find the most accurate information for your music.

## ✨ What Can Song Info Finder Do?

- **🔍 Find Missing Information**: Automatically search for song details like artist, album, title, genre, and year
- **🖼️ Get Album Covers**: Download and embed album artwork into your MP3 files
- **✏️ Edit Information**: Manually edit any song details before saving
- **💾 Save to Files**: Write all the information directly to your MP3 files
- **🔄 Refresh Results**: Search again with updated information to find better matches

## 🚀 Quick Start Guide

### Step 1: Download and Install

1. **Download the application** from the project page
2. **Extract the files** to a folder on your computer
3. **Open Command Prompt/Terminal** in that folder

### Step 2: Set Up the Application

1. **Create a virtual environment** (this keeps the app separate from other programs):

   ```bash
   python -m venv .venv
   ```

2. **Activate the virtual environment**:

   - **Windows**: `.venv\Scripts\activate`
   - **Mac/Linux**: `source .venv/bin/activate`

3. **Install required packages**:

   ```bash
   pip install -r requirements.txt
   ```

### Step 3: Run the Application

1. **Start the application**:

   ```bash
   python main.py
   ```

2. **Open your web browser** and go to: `http://127.0.0.1:5000`

3. **You should see the Song Info Finder homepage!** 🎉

## 📖 How to Use Song Info Finder

### Finding Song Information

1. **Enter the file path** of your MP3 file

   - Example: `C:\Music\My Song.mp3` (Windows)
   - Example: `/home/user/music/my-song.mp3` (Mac/Linux)

   💡 **Tip**: Use the "Browse" button to select a file and get the filename, then add the full path manually.

2. **Click "Find Song Info"** to search for information

3. **Wait for results** - the app will search iTunes for matching songs

### Understanding the Results

The app will show you:

- **🎯 Best Match**: The most likely match for your song (highlighted in blue)
- **📋 Other Matches**: Additional possible matches
- **📝 Metadata Form**: Where you can edit the song information

Each match shows:

- Album cover (if available)
- Song title
- Artist name
- Album name
- Year

### Editing Song Information

1. **Click on any match** to automatically fill the form with that information
2. **Edit the fields** as needed:

   - **Title**: The name of the song
   - **Artist**: The performer or band
   - **Album**: The album the song is from
   - **Genre**: The music genre (e.g., Rock, Pop, Jazz)
   - **Track Number**: The song's position on the album
   - **Disc Number**: If it's a multi-disc album
   - **Album Artist**: The main artist for the album
   - **Year**: The year the song/album was released

3. **Use the buttons**:
   - **"Use These Tags"**: Fill the form with the selected match
   - **"Reset to File Tags"**: Go back to the original information in your file
   - **"Refresh"**: Search again with your edited information
   - **"Save Metadata"**: Save all changes to your MP3 file

### Saving Your Changes

1. **Review the information** in the form
2. **Click "Save Metadata"**
3. **Wait for confirmation** - you'll see a success message
4. **Your MP3 file is now updated!** 🎉

## 💡 Tips and Tricks

### Getting Better Results

The search relies on the **Title**, **Album**, and **Artist** fields. So, on Metadata Fields, try to:

- **Use the full song title** if possible
- **Try the "Refresh" button** with different information if results aren't good
- **Check "Other Matches"** if the best match doesn't look right

### File Path Tips

- **Windows**: Use backslashes `\`
- **Mac/Linux**: Use forward slashes `/`
- **Avoid spaces**: If your path has spaces, that's fine - the app handles them
- **Check permissions**: Make sure you can read and write to the file

### Troubleshooting

**"File not found" error:**

- Double-check the file path
- Make sure the file exists
- Try copying the path from your file explorer

**"No search results" error:**

- Check your internet connection
- Try a different song title or artist name
- Use the "Refresh" button with different information

**"Could not save metadata" error:**

- Make sure the file isn't open in another program
- Check that you have write permissions for the file
- Try running the app as administrator (Windows)

**Cover art not showing:**

- Not all songs have cover art available
- The app will show "No Cover" if none is found
- Cover art is automatically embedded when you save

## 🔧 Advanced Features

### Refreshing Search Results

If you don't get good results:

1. **Edit the information** in the form
2. **Click "Refresh"** to search again
3. **Try different combinations** of title, artist, and album

### Manual Editing

You can manually edit any field:

1. **Type directly** in any field
2. **Mix and match** information from different results
3. **Add missing information** that wasn't found automatically

## 🆘 Getting Help

### Common Questions

**Q: Does this work with other audio formats?**
A: Currently, the app only works with MP3 files.

**Q: Do I need an internet connection?**
A: Yes, the app needs internet to search for song information.

**Q: Is my music safe?**
A: Yes! The app only reads and writes metadata, it doesn't change your actual music files.

**Q: Can I undo changes?**
A: You can use "Reset to File Tags" to go back to the original information, but once saved, changes are permanent.

**Q: Does this work on mobile?**
A: The web interface works on mobile browsers, but you'll need to enter file paths manually.

### Support

If you're having trouble:

1. **Check the [troubleshooting](#troubleshooting) section** above
2. **Make sure you followed the [installation](#-quick-start-guide) steps** correctly
3. **Try restarting the application**
4. **Check that your MP3 file isn't corrupted**

## 📝 System Requirements

- **Operating System**: Windows, Mac, or Linux
- **Python**: Version 3.7 or higher
- **Internet Connection**: Required for searching song information
- **File Permissions**: Read and write access to your MP3 files

## 🎯 What Song Info Finder Does NOT Do

- ❌ Convert audio formats
- ❌ Download music files
- ❌ Play music
- ❌ Organize your music library
- ❌ Change the actual audio content

## 🎉 Ready to Get Started?

1. **Follow the Quick Start Guide** above
2. **Try with a simple MP3 file** first
3. **Explore the features** and see how it works
4. **Enjoy your properly tagged music!** 🎵

---

**Happy music organizing!** 🎶

_Song Info Finder uses the iTunes API to find song information. No API keys or accounts required._
