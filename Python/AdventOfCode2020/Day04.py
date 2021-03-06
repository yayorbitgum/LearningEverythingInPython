# https://adventofcode.com/2020/day/4
import re


keys = ['byr', 'ecl', 'eyr', 'hcl', 'hgt', 'iyr', 'pid']
valid_count = 0
birth_min = 1920
birth_max = 2002
issue_min = 2010
issue_max = 2020
expire_min = 2020
expire_max = 2030
hgt_cm_min = 150
hgt_cm_max = 193
hgt_in_min = 59
hgt_in_max = 76

with open('inputs\day04_input.txt', 'r') as file:
    file = file.read().strip()

# Each passport is separated by a blank line in between.
passports = file.split('\n\n')
# Formatting messy input into nice clean dictionaries --------------------------
passport_master_list = []
for passport in passports:
    fields = re.split('\s', passport)
    passport_dictionary = dict(entry.split(':') for entry in fields)
    passport_master_list.append(passport_dictionary)


# Functions --------------------------------------------------------------------
def validate_passport(pp):
    """ Validates each required field for the passport.
    Returns True if all required fields (7) are present and valid.
    This is big and does many things. Should refactor later?"""
    valid = 0
    birth = pp.get('byr')
    issue = pp.get('iyr')
    expire = pp.get('eyr')
    height = pp.get('hgt')
    hair_color = pp.get('hcl')
    eye_color = pp.get('ecl')
    pp_id = pp.get('pid')
    country_id = pp.get('cid')

    required = [birth, issue, expire, height, hair_color, eye_color, pp_id]

    if None in required:
        return False

    # Birth Year.
    if birth_min <= int(birth) <= birth_max:
        valid += 1
    # Issue Year.
    if issue_min <= int(issue) <= issue_max:
        valid += 1
    # Expiration Year.
    if expire_min <= int(expire) <= expire_max:
        valid += 1

    # Height.
    if height.endswith('cm'):
        cm = int(height.rstrip('cm'))
        if hgt_cm_min <= cm <= hgt_cm_max:
            valid += 1
    elif height.endswith('in'):
        inch = int(height.rstrip('in'))
        if hgt_in_min <= inch <= hgt_in_max:
            valid += 1

    # Hair color.
    if re.findall('(#[a-f0-9]{6})', hair_color):
        valid += 1

    # Eye color.
    eye_colors = ['amb', 'blu', 'brn', 'gry', 'grn', 'hzl', 'oth']
    if eye_color in eye_colors:
        valid += 1

    # Passport ID number.
    if re.findall('\d{9}', pp_id) and len(pp_id) == 9:
        valid += 1

    # Final verification print and return.
    if valid == 7:
        print(f"birth: {birth} | issue: {issue} | passport ID: {pp_id} | "
              f"expire: {expire} | height: {height} | hair: {hair_color} | "
              f"eye: {eye_color} | country: {country_id}")
        return True


# Part one! --------------------------------------------------------------------
for passport in passport_master_list:
    left_overs = keys[:]
    for key in passport.keys():
        if key in left_overs:
            left_overs.remove(key)

    if left_overs == 'cid':
        valid_count += 1
    elif len(left_overs) == 0:
        valid_count += 1

print(f"Valid count for part 1: {valid_count}")


# Part two! --------------------------------------------------------------------
true_true = 0
for passport in passport_master_list:
    if validate_passport(passport):
        true_true += 1

print(f"Valid count for part 2: {true_true}")