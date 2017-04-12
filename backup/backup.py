from conf import Config as C
import os
def judge_source_dir():
    source_dir = "d:/source"
    if os.path.exists(source_dir):
        print ("source ok")
    else:
        os.mkdir(source_dir)

def main():
    judge_source_dir()

if __name__ == '__main__':
    main()



