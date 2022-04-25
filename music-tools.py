from pypinyin import lazy_pinyin
import pykakasi
import os
import json
import re
import music_tag

# add music file extension to list if not exist here
music_extension = ['mp3', 'flac', 'wav', 'ape']
music_dict = {}


def save_to_json():
    # save music_dict to json file
    music_json = open("music_list.json", "w", encoding="utf8")
    json.dump(music_dict, music_json, ensure_ascii=False)
    music_json.close()


def chinese_to_pinyin():
    files = os.listdir()
    for file in files:
        file_extension = os.path.splitext(file)[1].replace('.', '')
        if file_extension in music_extension:
            file_name = os.path.splitext(file)[0]

            # identify chinese character
            chinese_pattern = re.compile(r'[\u4e00-\u9fff]+')
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
    files = os.listdir()

    # read music_list.json file
    with open("music_list.json", "r", encoding="utf8") as music_list:
        music_dict = json.load(music_list)

    for file in files:
        file_extension = os.path.splitext(file)[1].replace('.', '')
        if file_extension in music_extension:
            file_name = os.path.splitext(file)[0]

            # try to find file name in music_dict
            try:
                os.rename(file, f'{music_dict[file_name]}.{file_extension}')
                rename_lrc_file(file_name, music_dict[file_name])
            except KeyError:
                print(f"{file_name} not found in music_list.json")
            except FileExistsError:
                print(f"{file_name} already exist")


def tag_to_filename():
    files = os.listdir()
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

    for file in files:
        file_extension = os.path.splitext(file)[1].replace('.', '')

        if file_extension in music_extension:
            file_name = os.path.splitext(file)[0]

            # get tag info from music file then rename file
            tag_info = music_tag.load_file(file)
            tag_name = f"{tag_info['title']} - {tag_info['artist']}"

            # idetify and replace Windows illegal character
            for i, j in illegal_character.items():
                tag_name = tag_name.replace(i, j)
            print(f"{file_name} -> {tag_name}.{file_extension}")

            # rename file
            os.rename(file, f'{tag_name}.{file_extension}')

            # rename lrc file if exist
            rename_lrc_file(file_name, tag_name)


def track_to_file():
    files = os.listdir()

    # get leading number from user
    print("Enter value 0 for no leading number")
    leading_number = input("Enter leading number: ")

    for file in files:
        file_extension = os.path.splitext(file)[1].replace('.', '')

        if file_extension in music_extension:
            file_name = os.path.splitext(file)[0]

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
    files = os.listdir()
    for file in files:
        file_extension = os.path.splitext(file)[1].replace('.', '')
        if file_extension in ['mp3', 'flac', 'wav', 'ape']:
            file_name = os.path.splitext(file)[0]

            # identify japanese character
            japanese_pattern = re.compile(r'[\u3040-\u30ff]+')
            japanese_match = japanese_pattern.search(file_name)

            chinese_pattern = re.compile(r'[\u4e00-\u9fff]+')
            chinese_match = chinese_pattern.search(file_name)

            if japanese_match:
                # Convert Japanese to Romanji
                kks = pykakasi.kakasi()
                convert_result = kks.convert(file_name)
                romanji = ' '.join([item['hepburn'].strip()
                                    for item in convert_result])
                romanji = romanji.replace("  ", " ").title()
                print(f"{file_name} -> {romanji}.{file_extension}")

                # rename file
                os.rename(file, f'{romanji}.{file_extension}')

                # save romanji to dictionary as key
                music_dict[romanji] = file_name

                # rename lrc file if exist
                rename_lrc_file(file_name, romanji)
            else:
                print(f"\n\n{file_name} is unable to convert romanji")
                # There is a condition that japanese character is same as chinese character
                # So need to prompt user to insit convert or not to convert
                if chinese_match:
                    user_input = input(
                        "Do you want to convert it insit? (y/n) ")
                    if user_input == "y":
                        # Convert Japanese to Romanji
                        kks = pykakasi.kakasi()
                        convert_result = kks.convert(file_name)
                        romanji = ' '.join([item['hepburn'].strip()
                                            for item in convert_result])
                        romanji = romanji.replace("  ", " ").title()
                        # rename file
                        os.rename(file, f'{romanji}.{file_extension}')

                        # save romanji to dictionary as key
                        music_dict[romanji] = file_name

                        # rename lrc file if exist
                        rename_lrc_file(file_name, romanji)

    # save original file name to json file
    save_to_json()


def remove_leading_number():
    files = os.listdir()
    for file in files:
        file_extension = os.path.splitext(file)[1].replace('.', '')
        if file_extension in music_extension:
            file_name = os.path.splitext(file)[0]

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


def rename_lrc_file(old_name, new_name):
    if os.path.isfile(f"{old_name}.lrc"):
        os.rename(f"{old_name}.lrc", f"{new_name}.lrc")


def music_tools():
    while True:
        print("\n[1] Music Tag info to File")
        print("[2] Covert Chinese to Pinyin")
        print("[3] Convert Japanese to Romanji")
        print("[4] Add Track Number to File")
        print("[5] Remove Leading Number")
        print("[6] music_list.json to File")

        user_choice = int(input("\nChoose your option: "))

        if user_choice == 1:
            tag_to_filename()
        elif user_choice == 2:
            user_opt = input("Do you want to convert to pinyin? (Y/N) : ")
            if user_opt == 'Y' or user_opt == 'y':
                chinese_to_pinyin()
            else:
                print("Converting back to chinese")
                music_list_to_file()
        elif user_choice == 3:
            user_opt = input("Do you want to convert to romanji? (Y/N) : ")
            if user_opt == 'Y' or user_opt == 'y':
                japanese_to_romanji()
            else:
                print("Converting back to japanese")
                music_list_to_file()
        elif user_choice == 4:
            track_to_file()
        elif user_choice == 5:
            remove_leading_number()
        elif user_choice == 6:
            music_list_to_file()
        else:
            print("Invalid option")


music_tools()
