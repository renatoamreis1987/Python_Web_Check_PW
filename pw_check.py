import requests
import hashlib


def request_api_data(query_char):
    url = 'https://api.pwnedpasswords.com/range/' + query_char  # First 5 chars only
    res = requests.get(url)
    if res.status_code != 200:
        raise RuntimeError(f'Error fetching: {res.status_code}, check the api and try again')
    return res


# As we will get several results from the 5chars sent to the API, this will compare with the full hash
# and check how many times it was hacked
def get_password_leaks_count(hashes, hash_to_check):
    # https://www.geeksforgeeks.org/python-string-splitlines/
    hashes = (line.split(':') for line in hashes.text.splitlines())
    for h, count in hashes:
        if h == hash_to_check:
            return count
    return 0


def pwned_api_check(password):
    # check password if it exists in API response
    sha1password = hashlib.sha1(password.encode('utf-8')).hexdigest().upper()  # Convert the password in SHA1 Hash
    first5_char, tail = sha1password[:5], sha1password[5:]  # for haveibeenpwned we only need the first 5 chars
    response = request_api_data(first5_char)
    # In the following print it will retrieve all passwords that are similar, including the one we submitted
    # print(response.text)
    return get_password_leaks_count(response, tail)


def main(password):
    count = pwned_api_check(password)
    if count:
        return f'{password} was found {count} times... you should probably change your password'
    else:
        return f'{password} was not found. Carry on!'
    exit()
