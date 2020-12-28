import os
import sys
import string
import io
from configparser import ConfigParser, ParsingError

def safeFilename(filename):
    # Set here the valid chars
    safechars = string.ascii_letters + string.digits + "~ -_.#"
    res = ''
    for c in filter(lambda c: c in safechars, filename):
        res += c
    return res

def write_config(output_dir, cfg_type, name, data):
    type_dir = os.path.join(output_dir, cfg_type)
    if(not os.path.isdir(type_dir)):
        os.mkdir(type_dir)
    
    safe_name = safeFilename(name)
    outfile = os.path.join(type_dir, safe_name + '.ini')
    if(os.path.isfile(output_dir)):
        os.remove(outfile)
        
    parser = ConfigParser(interpolation=None)
    
    parser.add_section('delete_me')
    for key, val in data:
        parser.set('delete_me', key, str(val))
        
    output = io.StringIO()
    parser.write(output)
    
    data = output.getvalue()
    lines = data.split('\n')[1:] # drop bogus config section name
        
    with open(outfile, 'w') as f:
        print('Writing ' + outfile)
        f.write('# Exported by Prusa Slicer Config Splitter - By Adam Haile\n')
        for l in lines:
            f.write(l)
            f.write('\n')

def main(basepath, filename):
    basename = os.path.splitext(os.path.basename(filename))[0]
    output_dir = os.path.join(basepath, basename)
    if(not os.path.isdir(output_dir)):
        os.mkdir(output_dir)
        
    parser = ConfigParser(interpolation=None)
    try:
        parser.read(filename)
    except ParsingError:
        print('Unable to read config bundle!')
        sys.exit(2)
        
    for sec in parser.sections():
        if(sec == 'presets'): 
            continue
        cfg_type, name = sec.split(':')
        write_config(output_dir, cfg_type, name, parser.items(sec))
        
if __name__ == '__main__':
    if(len(sys.argv) != 2):
        print('Usage: pscs.py <config_bundle_ini>')
        sys.exit(2)
    filename = sys.argv[1]
    if(not os.path.isfile(filename)):
        print('{} does not exist!'.format(filename))
        sys.exit(2)
        
    filename = os.path.abspath(filename)
    basepath = os.path.dirname(filename)
    
    if(os.path.splitext(filename)[1] != '.ini'):
        print('Must provide ini config bundle!')
        sys.exit(2)
    
    main(basepath, filename)