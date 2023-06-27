#!/usr/bin/python3
import sys
import configparser
import json
import os
from os.path import expanduser
import curses

def get_selected_profile(profiles):
    stdscr = curses.initscr()
    curses.noecho()
    curses.cbreak()
    stdscr.keypad(True)

    selected_index = 0
    try:
        while True:
            stdscr.clear()
            stdscr.addstr("Use the arrow keys to select a profile and press Enter:\n")
            for i, profile in enumerate(profiles):
                if i == selected_index:
                    stdscr.addstr(f" > {profile}\n")
                else:
                    stdscr.addstr(f"   {profile}\n")
            key = stdscr.getch()
            if key == curses.KEY_ENTER or key in [10, 13]:
                break
            elif key == curses.KEY_UP:
                selected_index = (selected_index - 1) % len(profiles)
            elif key == curses.KEY_DOWN:
                selected_index = (selected_index + 1) % len(profiles)
    except KeyboardInterrupt:
        # Ctrl+C가 눌렸을 때 정리 작업을 수행
        curses.endwin()
        sys.exit(0)

    curses.endwin()
    return profiles[selected_index]

if len(sys.argv) > 1:
    original_profile = sys.argv[1]
else:
    homeDirectory = expanduser("~")
    awsCred = configparser.ConfigParser()
    awsCred.read('%s/.aws/credentials' % homeDirectory)
    # profiles = awsCred.sections()
    original_profile = get_selected_profile(awsCred.sections())

homeDirectory = expanduser("~")
awsConfig = configparser.ConfigParser()
awsCred   = configparser.ConfigParser()

awsConfig.read("%s/.aws/config" % homeDirectory)
awsCred.read('%s/.aws/credentials' % homeDirectory)

identityResponse = os.popen("aws sts get-caller-identity --profile " + original_profile).read()
try:
    identity = json.loads(identityResponse)
except json.decoder.JSONDecodeError:
    exit("AWS was unable to identify you")

username = identity['Arn'].split('/')[1]
print("You are: " + username)

deviceResponse = os.popen("aws iam list-mfa-devices --user-name '" + username + "' --profile " + original_profile).read()
try:
    mfaDevice = json.loads(deviceResponse)
except json.decoder.JSONDecodeError:
    exit("AWS was unable to find a registered MFA device for you")

deviceNumber = mfaDevice['MFADevices'][0]['SerialNumber']
print("Your device is: " + deviceNumber)

OneTimeNumber = input("Enter your MFA code now: ").replace(" ","")

if not OneTimeNumber.isdigit():
    exit("MFA code can only contain digits and spaces")

response = os.popen("aws sts get-session-token --serial-number  %s --token-code %s --profile %s" % ( deviceNumber, OneTimeNumber, original_profile )).read()

try:
    mfaCreds = json.loads(response)
except json.decoder.JSONDecodeError:
    exit("AWS was not happy with that one")

# reset!

awsCred[original_profile + '-mfa'] = {}
awsCred[original_profile + '-mfa']['aws_access_key_id']     = mfaCreds['Credentials']['AccessKeyId']
awsCred[original_profile + '-mfa']['aws_secret_access_key'] = mfaCreds['Credentials']['SecretAccessKey']
awsCred[original_profile + '-mfa']['aws_session_token']     = mfaCreds['Credentials']['SessionToken']

with open('%s/.aws/credentials' % homeDirectory, 'w') as awsCredfile:
    awsCred.write(awsCredfile)

print("\n==> '" + original_profile + "-mfa' created/updated successfully <==")
print("==> Use '--profile' option with '" + original_profile + "-mfa' <==")
print("==> Use below command to change 'default profile' to '" + original_profile + "-mfa' <==")
print('\n$ export AWS_profile=' + original_profile + '-mfa')
