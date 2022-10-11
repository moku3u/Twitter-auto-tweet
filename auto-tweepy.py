import threading
import time
from tkinter import filedialog
from PIL import Image
from tkinter import *
from twitter import *
from os import system

system("title Twitter Auto Tweet tools")
Tk().withdraw()

def main():
    while True:
        auth_token = input("auth_token: ")
        if util.check_auth_token(auth_token):
            break
    while True:
        tweet_text = input("Tweet Text: ")
        if len(tweet_text) > 130:
            print("Content must be 125 characters or less")
        else:
            tweet_text = util.indention_replace(tweet_text)
            break
    use_image = util.limit_input("Would you like to attach an image?(y/n)", ["y", "n"], "input must be y or n")
    repetitions_count = util.limit_input("How many times do you tweet?", int, "input must be only number")
    wait = util.limit_input("How long do you wait to tweet?", int, "input must be only number")
    if use_image == "y":
        while True:
            filepath = filedialog.askopenfilename(filetypes=[("Image file", "*.png")])
            if Image.open(filepath).format != "PNG":
                print("Only supports png files")
            else:
                with open(filepath, "rb") as f:
                    media = f.read()
                break
        twitter = Tweet(auth_token, tweet_text, media)
        twitter.upload_image()
    else:
        twitter = Tweet(auth_token, tweet_text)
    count = 0
    twitter.post()
    while count < int(repetitions_count)-1:
        count += 1
        time.sleep(int(wait)*60)
        twitter.post()
    print("finish")
    time.sleep(5)

if __name__ == "__main__":
    main()
