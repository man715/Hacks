#!/usr/bin/python3
from filehash import FileHash
from pwd import getpwnam
import os
import wget
import shutil
import subprocess
import tarfile

# Set up the hash function
md5_hasher = FileHash('md5')

# Rule name you want to download
rule_name = "snortrules-snapshot-3000.tar.gz"
# The rule hash to be compared against
hash_file_name = rule_name + ".md5"
# URLs to download the hashfile and the rules tar
rules_url = "https://snort.org/rules/snortrules-snapshot-3000.tar.gz?oinkcode=99a4dd1bf84712af5e1e8c03fa715e06cddbee1d"
hash_url = "https://snort.org/rules/snortrules-snapshot-3000.tar.gz.md5?oinkcode=99a4dd1bf84712af5e1e8c03fa715e06cddbee1d"

# Download the blocklist file
wget.download("https://www.talosintelligence.com/documents/ip-blacklist", "ip-blacklist")

# Download the rules and the hash file
wget.download(rules_url,rule_name)
wget.download(hash_url,hash_file_name)

# Get the hash from the rules tar and compare it to the hash file
rules_hash = md5_hasher.hash_file(rule_name)
check_hash = open(hash_file_name, 'r').readline()

if rules_hash == check_hash:
    print("\nHashes matched... Now extracting the rules")

# Extract the rules
tarfile.open(rule_name).extractall()

# Copy all the rules to the snort rules location
src = "./rules"
dest = "/usr/local/snort/rules/"
src_files = os.listdir(src)

for file_name in src_files:
    full_file_name = os.path.join(src, file_name)
    if os.path.isfile(full_file_name):
        shutil.copy(full_file_name, dest)

# Set the UID and GID to snort for all the rules files
uid = getpwnam('snort').pw_uid
gid = getpwnam('snort').pw_gid

for root, dirs, files in os.walk(dest):
    for momo in dirs:
        os.chown(os.path.join(root, momo), uid,gid)
    for momo in files:
        os.chown(os.path.join(root, momo), uid,gid)

# Copy the blocklist
shutil.copy("/home/man715/snortrules/ip-blacklist", "/usr/local/snort/intel/ip-blacklist")
os.chown("/usr/local/snort/intel/ip-blacklist",uid,gid)

# Clean up
shutil.rmtree("builtins")
shutil.rmtree("rules")
shutil.rmtree("etc")
os.remove("ip-blacklist")
os.remove(rule_name)
os.remove(hash_file_name)

command = ['service','snort','restart']

subprocess.call(command,shell=False)
