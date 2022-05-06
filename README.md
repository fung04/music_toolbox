# music_toolbox
 A python script to organize and clean up various naming methods for music files

# Prerequisite
+ [music_tag](https://pypi.org/project/music-tag/)
+ [pykakasi](https://pypi.org/project/pykakasi/)
+ [pypinyin](https://pypi.org/project/pypinyin/)

# Features
This script contains 7 function whereas:
 1. Music tag info to File
 2. Covert Chinese to Pinyin
 3. Convert Japanese to Romanji
 4. Add Track Number to File
 5. Remove Leading Number
 6. Embed Lyrics to Music tag
 7. music_list.json to File

 # Usage
 1. Edit the `music-tool.py` and append the `music_extension` list if the extension name is not in the list.
 1. Place the `music-tool.py` under the root directory of music files.
 2. Open up Windows Command Prompt in the directory.
 3. Type `python music-tool.py` to execute the script.

## 1. Music tag info to File
 This funtion will loop through all the  music files under the directory.Then read the tag info of each music files and rename it in `Title - Artist.mp3` manner.

- The music tag info might contain character forbidden to use in Windows. Below are alternate charater to replace it.
 ```
 illegal_character = {
        "/": ", ",
        ":": "-",
        "|": ", ",
        "?": "",
        "*": "",
        "\"": "",
        "<": "(",
        ">": ")",
    }
```
## 2. Covert Chinese to Pinyin
 This funtion will loop through all the  music files under the directory. Then covert all the chinese character to pinyin type.  
 For example:  
 ```
  我爱你.mp3 -> Wo Ai Ni.mp3
  ```

 ## 3. Convert Japanese to Romanji
 This funtion will loop through all the  music files under the directory. Then covert all the japanese character to romanji type.  
 For example:  
 ``` 
 愛してる.mp3 -> Aishiteru.mp3
 ```

 ## 4. Add Track Number to File
This funtion will loop through all the  music files under the directory and read the track number from music tag.  
Then renaming in following manner.
```
// Leading number = 0
I Love you.mp3 -> 01. I Love you.mp3

// Leading number = 1
I Love you.mp3 -> 1.01. I Love you.mp3
```

## 5. Remove Leading Number
This funtion will loop through all the  music files under the directory then remove all the leding number of music files.  
This is done with then help of regex and the pattern are `^\d*[-.]?\d*[-.\s]*`  
Removable pattern as below:

```
01 Song Title  (with or without space)
01. Song Title (with or without space)
01- Song Title (with or without space)
1.11 - Song Title (with or without space)
1.11 . Song Title (with or without space)
```

## 6. Embed Lyrics to Music tag
This funtion will loop through all the  music files and lrc files under the directory then embed the lyric file to music file.   
Note that the lyric file have to be same name as music file.
```
I Love you.mp3
I Love you.lrc
```
## 7. music_list.json to File
This is a revert funtion for `Covert Chinese to Pinyin` and `Convert Japanese to Romanji`. A `music_list.json` file will be generate to save the original file name in key-pair every time the two function is exectue.

```
\\ Current music file name
Wo Ai Ni.mp3

\\ Able to revert back to original name
Wo Ai Ni.mp3 -> 我爱你.mp3
