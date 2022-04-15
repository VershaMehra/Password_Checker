import hashlib
import sys

import requests  # this is like a browser without having actual browser


# url = 'https://api.pwnedpasswords.com/range/' + 'cbfda'  # if we write full hash code it will give 400 as a response code
# res = requests.get(url)  # response codes
# print(res)

def request_api_data(query_char):
    url = 'https://api.pwnedpasswords.com/range/' + query_char
    res = requests.get(url)  # response codes
    if res.status_code != 200:
        raise RuntimeError(f'error fetching: {res.status_code}, check the api and try again')
    return res


# this method converts our pwd to sh1 hash
def pwned_api_check(password):
    # print(hashlib.sha1(password.encode('utf-8')).hexdigest().upper())
    sha1password = hashlib.sha1(password.encode('utf-8')).hexdigest().upper()
    print(sha1password)
    first_5_characters = sha1password[:5]
    # print(first_5_characters)
    tail = sha1password[5:]
    # print(tail)
    response = request_api_data(first_5_characters)
    # print(response.text)  # will print all the matching passwords
    return get_pwd_leaks_count(response, tail)


def get_pwd_leaks_count(hashes, hash_to_check):
    hashes = (line.split(':') for line in hashes.text.splitlines())
    # print(hashes)
    for hash_val, count in hashes:
        # print(hash_val, count)
        if hash_val == hash_to_check:
            return count
    return 0


# pwned_api_check('123') - directly call the method or we can write main() too

def main(args):
    for pwd in args:
        count = pwned_api_check(pwd)
        if count:
            print(f'the {pwd}  was found {count} time. You should probably change your pwd.')
        else:
            print(f'{pwd} was not found. Carry on.')

    return 'done'


if __name__ == '__main__':
    sys.exit(main(sys.argv[1:]))

# run command in terminal- python password_checker.py 123
