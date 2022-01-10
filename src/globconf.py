# coding: latin-1

"""

Generic Global Config manager. 
Supports simple parsing of various file types and a straight forward way 
to provide global configuration for everyone


"""

import json
from ast import literal_eval
from configparser import ConfigParser
from fnmatch import fnmatch
from pprint import pformat

try:
    import yaml
except ImportError:
    # Optional support of a third party package
    yaml = None


def is_config(class_):
    try:
        return issubclass(class_, Config)
    except TypeError:
        return False


# #############################################################################
#
# Reader classes. Respsonsible to parse given data or update them from file
#


class Dict(object):
    """Has nothing to do just pass trough the configuration dict."""

    def read(self, data):
        return data

    def write(self, target, data):
        target.update(data)


class Json(object):
    """Load Json file and give back the data as dict."""

    def read(self, path):
        with open(path) as fp:
            return json.load(fp)

    def write(self, path, data):
        with open(path, "w") as fp:
            return json.dump(data, fp, indent=2)


class Yaml(object):
    """Load Yaml file and give back the data as dict."""

    def read(self, path):
        with open(path) as fp:
            return yaml.full_load(fp)

    def write(self, path, data):
        with open(path, "w") as fp:
            return yaml.dump(data, fp)


class Python(object):
    """Load Python file and give back the data as dict."""

    def read(self, path):
        locals_ = {}
        exec(open("./filename").read(), {}, locals_)
        # execfile(path, {}, locals_)
        return locals_


class Ini(object):
    """Load Ini file and give back the data as dict."""

    class _Parser(ConfigParser):
        def as_dict(self, convert=True):
            d = dict(self._sections)
            for k in d:
                d[k] = dict(self._defaults, **d[k])
                d[k].pop("__name__", None)
            if convert:
                self.auto_convert(d)
            # All settings in section globals are on the top level.
            d.update(d.pop("globals", {}))
            return d

        def auto_convert(self, data):
            for section, opt_value in data.items():
                for option, value in opt_value.items():
                    try:
                        data[section][option] = literal_eval(value)
                    except (ValueError, SyntaxError):
                        data[section][option] = value
            return data

    def read(self, path):
        parser = Ini._Parser(allow_no_value=True)
        parser.read(path)
        return parser.as_dict()

    def write(self, target, data):
        cfgwriter = ConfigParser()
        with open(target, "w") as fp:
            cfgwriter.add_section("globals")
            for key, value in sorted(data.items()):
                if hasattr(value, "items"):
                    if not cfgwriter.has_section(key):
                        cfgwriter.add_section(key)
                    for key2, value2 in value.items():
                        cfgwriter.set(key, key2, self._handle_unicode(value2))
                else:
                    cfgwriter.set("globals", key, self._handle_unicode(value))
            cfgwriter.write(fp)

    def _handle_unicode(self, value):
        """We use Pythons quoting here"""
        return repr(value)


class Guess(object):
    """
    Helper class to detect automatically what type of config file is given.
    This Reader is the default of our major config class.

    """

    def __init__(self):
        """ """
        self.dispatch = {}
        self.dispatch["*.py"] = Python()
        self.dispatch["*.json"] = Json()
        if yaml is not None:
            self.dispatch["*.yaml"] = Yaml()
        self.dispatch["*.ini"] = Ini()
        self.default = Dict()

    def find_handler(self, conf):
        if isinstance(conf, str):
            for pattern, reader in self.dispatch.items():
                if fnmatch(conf.lower(), pattern):
                    return reader
        return self.default

    def read(self, source):
        reader = self.find_handler(source)
        return reader.read(source)

    def write(self, target, data):
        writer = self.find_handler(target)
        return writer.write(target, data)


class Config(object):
    """
    Our major Class implementing the configuration handling on attribute and
    key level.
    It's possible to use either the attribute or the key notation

    Example usage:

        >>> from globcon import config
        >>> config.load('examples/configfile.json')
        <Config {u'a': 1,
                 u'b': 2,
                 u'details': {u'x': u'value of x', u'y': u'value of y'},
                 u'names': [u'foo', u'bar'],
                 u'on': True} >
        >>> config['b'] == config.b
        True
        >>> config.c = 'New value'
        >>> config.dump('examples/configfile.json')

    """

    @classmethod
    def fromconfig(cls, conf, name=None, link=True):
        """
        Use this class function to create new instance with the data from the
        given source configuration.

        Parameters:
          conf<Config>   The source configuration.
          name<str>      Optional name of the sub configuration.
          link<bool>     Either copy the data from the source configuration or
                         link to the given object.

        """
        new = cls()
        new.link_with(conf=conf, name=name, link=link)
        return new

    def link_with(self, conf, name=None, link=True):
        """
        Either copy the data from the source configuration or link to the
        given object

        Parameters:
          conf<Config>   The source configuration.
          name<str>      Optional name of the sub configuration.
          link<bool>     This flag decides whether we link or copy.

        """
        if name:
            if name not in conf and link is True:
                conf[name] = self
            conf = conf.get(name)
        if conf is None:
            return self
        dict_ = getattr(conf, "__dict__", conf)
        if link:
            self.__dict__ = dict_
        else:
            self.load(dict_)
        return self

    def __init__(self, conf=None, reader=Guess()):
        """
        Create a new configuration instance.

        Parameters:
          conf<object>    Optional parameter which could be a file link, a dict
                          or another configuration object.
          reader<object>  Optional paramerte used to load the given conf path
                          or object. By default a Guess instance is used which
                          knows various file extensions and which Read/Write
                          class to use.

        """
        if conf is not None:
            self.load(conf, reader=reader)

    def init_defaults(self):
        """
        It is allowed to define defaults on class level. On calling this method
        such default attributes will be copied to the attributes in case they
        are not yet defined.

        It's necessary to call this function if you have sub configurations
        defined or you want to dump the defaults to a config file.

        """
        for k, v in self.__class__.__dict__.items():
            if k.startswith("_"):
                continue  # no private members
            if k not in self.__dict__:
                if isinstance(v, property):
                    continue
                if is_config(v):
                    v = v()
                    v.init_defaults()
                self.__dict__[k] = v

    def __setitem__(self, key, value):
        """
        Item assignment (e.g. config['x'] = 1 )

        """
        setattr(self, key, value)
        return value

    def __getitem__(self, key):
        """
        Item get (e.g. x = config['x'] )

        """
        try:
            # Note: Using getattr to ensure the default lookup on class level.
            return getattr(self, key)
        except AttributeError as e:
            # The user expects a KeyError exception.
            raise KeyError(str(e))

    def __contains__(self, key):
        """
        Supports 'in' syntax (e.g. 'x' in config )

        """
        return hasattr(self, key)

    def get(self, key, default=None):
        """
        Get the value of the given attribute, false otherwise.

        """
        return getattr(self, key, default)

    def load(self, conf=None, reader=Guess(), clear=True):
        """
        Load the given configuration.

        Parameters:
          conf<object>    Optional parameter which could be a file link, a dict
                          or another configuration object.
          reader<object>  Optional paramerte used to load the given conf path
                          or object. By default a Guess instance is used which
                          knows various file extensions and which Read/Write
                          class to use.
          clear<bool>     Cleanup the configuration before loading the given.
                          A load() with clear=False is like an update().

        """
        if clear:
            self.clear()
        if conf is not None:
            data = reader.read(conf)
            if data and hasattr(data, "items"):
                for key, value in data.items():
                    default = getattr(self.__class__, key, None)
                    if is_config(default):
                        value = default(value, reader=reader)
                    if default is None:
                        # Workaround to update an existing instance.
                        # Otherwise it's defaults will be killed.
                        # Todo: Check this change with the existing unittests.
                        obj = getattr(self, key, None)
                        if isinstance(obj, Config):
                            obj.load(value, clear=clear)
                            continue
                    self._set_attribute(key, value, default, clear=clear)
        return self

    def _set_attribute(self, key, value, default, clear=True):
        """helper method handling the load() of sub configurations"""
        if key in self.__dict__ and is_config(default):
            self[key].load(value.__dict__, clear=clear)
        else:
            self[key] = value

    def dump(self, target, writer=Guess()):
        """
        Dump the current configuration to a file.

        """
        data = self.asdict()
        return writer.write(target, data)

    def asdict(self):
        """
        Return the current configuration as a plain dict.

        """
        data = {}
        for k, v in self.__dict__.items():
            if hasattr(v, "asdict"):
                v = v.asdict()
            data[k] = v
        return data

    def clear(self):
        """
        Empty the current configuration.

        Note: In case a sub configuration exists, it will not be removed it
              will be cleared recursively.

        """
        for k, v in self.__dict__.items():
            if isinstance(v, (Config, dict)):
                v.clear()
            else:
                del self.__dict__[k]

    def __repr__(self):
        """
        Object represents itself

        """
        return "<{} {} >".format(self.__class__.__name__, pformat(self.__dict__))

    def __nonzero__(self):
        """
        Returns True if some configuration is set. False otherwise.

        """
        return bool(self.__dict__)


# Our 'single' and global configuration instance.
# It's up to the user whether he want's to rely on this.
config = Config()
