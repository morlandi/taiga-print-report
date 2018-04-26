import sys
import os
try:
    import configparser
except:
    from six.moves import configparser
    from six.moves import input


default_config = """
[general]
host=HOST
username=USERNAME
password=PASSWORD
copyright=YOUR COPYRIGHT HERE ...
[task_headers]
0=Task
1=Description
"""

def read_config_file():
    """
    Parse the config file if exists;
    otherwise, create a default config file and exit
    """

    def query_yes_no(question, default="yes"):
        """Ask a yes/no question via raw_input() and return their answer.

        "question" is a string that is presented to the user.
        "default" is the presumed answer if the user just hits <Enter>.
            It must be "yes" (the default), "no" or None (meaning
            an answer is required of the user).

        The "answer" return value is True for "yes" or False for "no".
        """
        valid = {"yes": True, "y": True, "ye": True,
                 "no": False, "n": False}
        if default is None:
            prompt = " [y/n] "
        elif default == "yes":
            prompt = " [Y/n] "
        elif default == "no":
            prompt = " [y/N] "
        else:
            raise ValueError("invalid default answer: '%s'" % default)

        while True:
            sys.stdout.write(question + prompt)
            choice = input().lower()
            if default is not None and choice == '':
                return valid[default]
            elif choice in valid:
                return valid[choice]
            else:
                sys.stdout.write("Please respond with 'yes' or 'no' (or 'y' or 'n').\n")

    def create_default_config_file(config_filename):

        cwd = os.getcwd()
        project = os.path.split(cwd)[-1]
        text = default_config.format(
            project=project,
        )
        with open(config_filename, 'w') as configfile:
            configfile.write(text)

    #config_filename = './.%s%sconf' % (os.path.splitext(os.path.basename(__file__))[0], os.path.extsep)
    config_filename = os.path.join(os.path.expanduser("~"), '.taiga_print_report.conf')
    config = configparser.ConfigParser()
    success = len(config.read(config_filename)) > 0
    if success:
        sys.stderr.write('Using config file "%s"\n' % config_filename)
    else:
        # if not found, create a default config file and exit
        if query_yes_no('Create default config file "%s" ?' % config_filename):
            create_default_config_file(config_filename)
            print('Default config file "%s" has been created; please check it before running this script again' % config_filename)
        exit(-1)

    return config


