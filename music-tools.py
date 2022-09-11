import json
import os
import re

import music_tag
import pykakasi
from pypinyin import lazy_pinyin

# add music file extension to list if not exist here
music_extension = ['mp3', 'flac', 'ape', 'm4a', 'dsf', 'aif']
music_dict = {}

# regex pattern for japanese and chinese character
japanese_pattern = re.compile(r'[\u3040-\u30ff]+')
chinese_pattern = re.compile(r'[\u4e00-\u9fff]+')


def save_to_json():
    # save music_dict to json file
    music_json = open("music_list.json", "w", encoding="utf8")
    json.dump(music_dict, music_json, ensure_ascii=False)
    music_json.close()


# loop through file directory and return file, file name and file extension
def get_file_info():
    files = os.listdir()
    for file in files:
        file_extension = os.path.splitext(file)[1].replace('.', '')
        if file_extension in music_extension:
            file_name = os.path.splitext(file)[0]
            yield file, file_extension, file_name


def chinese_to_pinyin():
    for file, file_extension, file_name in get_file_info():

        # identify chinese character in file name
        chinese_match = chinese_pattern.search(file_name)

        if chinese_match:
            # convert chinese to pinyin
            pinyin = ' '.join(lazy_pinyin(file_name)).title()
            pinyin = pinyin.replace("  ", " ")
            print(f"{file_name} -> {pinyin}.{file_extension}")

            # rename file
            os.rename(file, f'{pinyin}.{file_extension}')

            # rename lrc file if exist
            rename_lrc_file(file_name, pinyin)

            # save pinyin to dictionary as key
            music_dict[pinyin] = file_name
        else:
            print(f"{file_name} is unable to covert pinyin")

    # save original file name to json file
    save_to_json()


def music_list_to_file():

    # read music_list.json file
    with open("music_list.json", "r", encoding="utf8") as music_list:
        music_dict = json.load(music_list)

    for file, file_extension, file_name in get_file_info():

        # try to find file name in music_dict
        try:
            os.rename(file, f'{music_dict[file_name]}.{file_extension}')
            rename_lrc_file(file_name, music_dict[file_name])
        except KeyError:
            print(f"{file_name} not found in music_list.json")
        except FileExistsError:
            print(f"{file_name} already exist")


def tag_to_filename():
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

    for file, file_extension, file_name in get_file_info():

        # get tag info from music file then rename file
        tag_info = music_tag.load_file(file)
        tag_name = f"{tag_info['title']} - {tag_info['artist']}"

        # idetify and replace Windows illegal character
        for i, j in illegal_character.items():
            tag_name = tag_name.replace(i, j)

        if tag_info['title']:
            print(f"{file_name} -> {tag_name}.{file_extension}")
            try:
                # rename file
                os.rename(file, f'{tag_name}.{file_extension}')
            except FileExistsError:
                i = 0
                i = i + 1
                tag_name = f'{tag_name} ({i})'
                os.rename(file, f'{tag_name}.{file_extension}')

            # rename lrc file if exist
            rename_lrc_file(file_name, tag_name)
        else:
            print(f"\n\nNo title for {file_name}\n\n")


def track_to_file():

    # get leading number from user
    print("Enter value 0 for no leading number")
    leading_number = input("Enter leading number: ")

    for file, file_extension, file_name in get_file_info():

        # get track number from music file
        tag_info = music_tag.load_file(file)

        # identify track number is not empty
        track_number = int(tag_info['tracknumber'])

        if track_number:
            if leading_number == "0" or leading_number == "":
                file_with_track_number = f"{track_number:02d}. {file_name}"
            else:
                file_with_track_number = f"{leading_number}.{track_number:02d}. {file_name}"
        else:
            file_with_track_number = f"{file_name}"

        print(f"{file_name} -> {file_with_track_number}.{file_extension}")

        # rename file
        os.rename(file, f'{file_with_track_number}.{file_extension}')

        # rename lrc file if exist
        rename_lrc_file(file_name, file_with_track_number)


def japanese_to_romanji():
    for file, file_extension, file_name in get_file_info():

        # identify japanese character in file name
        japanese_match = japanese_pattern.search(file_name)

        if not japanese_match:
            # identify chinese character in file name
            chinese_match = chinese_pattern.search(file_name)

            if chinese_match:
                # There is a condition that japanese character is same as chinese character
                # So need to prompt user to insit convert or not to convert
                user_input = input(
                    f"\n\nDo you want to convert {file_name} insit? (y/n) ")
                if user_input == "y":
                    chinese_match = chinese_match.group()
            else:
                chinese_match = None

        if japanese_match or chinese_match:
            # Convert Japanese to Romanji
            kks = pykakasi.kakasi()
            convert_result_dict = kks.convert(file_name)
            romanji = ' '.join([item['hepburn'].strip()
                                for item in convert_result_dict])
            romanji = romanji.replace("  ", " ").title()
            print(f"{file_name} -> {romanji}.{file_extension}")

            # rename file
            os.rename(file, f'{romanji}.{file_extension}')

            # save romanji to dictionary as key
            music_dict[romanji] = file_name

            # rename lrc file if exist
            rename_lrc_file(file_name, romanji)
        else:
            print(f"{file_name} is unable to convert romanji")

    # save original file name to json file
    save_to_json()


def remove_leading_number():
    for file, file_extension, file_name in get_file_info():

        # remove leading number with regex
        # removeable pattern are:  01 Song Title  (with or without space)
        #                          01. Song Title (with or without space)
        #                          01- Song Title (with or without space)
        #                          1.11 - Song Title (with or without space)
        #                          1.11 . Song Title (with or without space)

        new_file_name = re.sub('^\d*[-.]?\d*[-.\s]*', '', file_name)

        # get user confirmation before rename file
        print(f"{file_name}.{file_extension} -> {new_file_name}.{file_extension}")

        # rename file
        os.rename(file, f'{new_file_name}.{file_extension}')

        # rename lrc file if exist
        rename_lrc_file(file_name, new_file_name)


def lyrics_to_metadata():
    for file, file_extension, file_name in get_file_info():

        # get metadata from music file
        tag_info = music_tag.load_file(file)

        # check if lrc file exits
        if os.path.isfile(file_name + '.lrc'):
            with open(file_name + '.lrc', 'r', encoding='utf-8') as f:
                if tag_info['lyrics']:
                    print("Conflict: lyrics already exist")
                    print(f"\n\n Lyric from metadata:\n {tag_info['lyrics']}")
                    print(f"\n\n Lyric from lrc file:\n {f.read()}")
                    user_input = input(
                        f"\n\nDo you want to overwrite lyrics? (y/n) ")
                    if user_input == "y":
                        tag_info['lyrics'] = f.read()
                        tag_info.save()
                    else:
                        print("Lyrics not overwritten")
                else:
                    tag_info['lyrics'] = f.read()
                    tag_info.save()
                    print(f"The lyrics of ({file_name}) is embedded.")
        else:
            print(f"{file_name}.lrc not found")


def filename_to_title():
    for file, file_extension, file_name in get_file_info():

        # get metadata from music file
        tag_info = music_tag.load_file(file)

        if not tag_info['comment']:
            # backup tag_info['title'] to tage_info['comment']
            tag_info['comment'] = tag_info['title']

            # save file name to tag_info['title']
            tag_info['title'] = file_name
            print(f"Music Title: {tag_info['title']}")
            tag_info.save()
        else:
            print(f"The comment: {tag_info['comment']} ")
            user_input = input(
                f"\n\nDo you want to overwrite comment? (y/n) ")
            if user_input == "y":
                tag_info['comment'] = tag_info['title']
                # save file name to tag_info['title']
                tag_info['title'] = file_name
                print(f"Music Title: {tag_info['title']}")
                tag_info.save()
            else:
                print("Comment not overwritten")


def rename_lrc_file(old_name, new_name):
    # rename and replace lrc file if exist
    if os.path.isfile(f"{old_name}.lrc"):
        os.rename(f"{old_name}.lrc", f"{new_name}.lrc")


def music_tool_menu():
    tag_to_filename()
    # get user input
    user_input = input("\n\nSelect option: \n\n"
                       "[1] Music tag info to File\n"
                       "[2] Covert Chinese to Pinyin\n"
                       "[3] Convert Japanese to Romanji\n"
                       "[4] Add Track Number to File\n"
                       "[5] Remove Leading Number\n"
                       "[6] Embed Lyrics to Music lyric tag \n"
                       "[7] Embed file name to Music title tag\n"
                       "[8] music_list.json to File\n\n"
                       "Enter option: ")

    # check user input
    if user_input == "1":
        tag_to_filename()
    elif user_input == "2":
        chinese_to_pinyin()
    elif user_input == "3":
        japanese_to_romanji()
    elif user_input == "4":
        track_to_file()
    elif user_input == "5":
        remove_leading_number()
    elif user_input == "6":
        lyrics_to_metadata()
    elif user_input == "7":
        filename_to_title()
    elif user_input == "8":
        music_list_to_file()
    elif user_input == "chinese":
        chinese_to_pinyin()
        lyrics_to_metadata()
        filename_to_title()
    else:
        print("Invalid option")


if __name__ == "__main__":
    while True:
        music_tool_menu()
