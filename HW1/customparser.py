import ConfigParser


class ConfigReader(object):

    def __init__(self, config_path):
        self.Config = ConfigParser.ConfigParser()
        self.Config.read(config_path)

    def get_config_section_map(self, section):
        dict1 = {}
        options = self.Config.options(section)
        for option in options:
            try:
                val = self.Config.get(section, option)
                # Check if its an array of values
                if ',' in val:
                    dict1[option] = self.parse_array(val)
                else:
                    dict1[option] = self.Config.get(section, option)
                if dict1[option] == -1:
                    print "skip: %s" % option
            except:
                print "exception on %s!" % option
                dict1[option] = None
        return dict1

    def parse_array(self, array_string):
        array = array_string.split(',')
        return array
