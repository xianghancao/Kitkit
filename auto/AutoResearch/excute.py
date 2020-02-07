# encoding: utf-8
import argparse
import compileall
import os


def remove_file(path, special_str):
    for p in os.listdir(path):
        subpath = os.path.join(path, p)
        if os.path.isdir(subpath):
            remove_file(subpath, special_str)
        else:
            if subpath[-3:] == '.py':
                os.remove(subpath)
                print 'delete %s' %subpath


def main():
    # args
    parser = argparse.ArgumentParser()

    #     
    parser.add_argument("-f", "--file", action="store",
                      dest="filename",
                      required=True,
                      help="file")


    args = parser.parse_args()  
        
        
    f = os.path.realpath(__file__)
    fpath = os.path.dirname(f)
    compileall.compile_dir(fpath)

    remove_file(fpath, '.py')
    os.system('python %s.pyc' %args.filename.split('.')[0])
    return



if __name__ == '__main__':
   
    main()
    

