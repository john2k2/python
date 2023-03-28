import os
import shutil
import time
import argparse


parser = argparse.ArgumentParser()
parser.add_argument('source_folder', help='path to source folder')
parser.add_argument('replica_folder', help='path to replica folder')
parser.add_argument('interval', help='sync interval in seconds', type=int)
parser.add_argument('log_file', help='path to log file')
args = parser.parse_args()

# This code is used to sync two folders.


def sync(source_folder, replica_folder, interval, log_file):
    while True:
        source_files = os.listdir(source_folder)
        replica_files = os.listdir(replica_folder)
        for file in source_files:
            if file not in replica_files:
                shutil.copy2(os.path.join(source_folder, file), replica_folder)
                with open(log_file, 'a') as log:
                    log.write('File {} copied at {} \n'.format(
                        file, time.ctime()))
            else:
                source_file = os.path.join(source_folder, file)
                replica_file = os.path.join(replica_folder, file)
                if os.path.getmtime(source_file) > os.path.getmtime(replica_file):
                    shutil.copy2(source_file, replica_folder)
                    with open(log_file, 'a') as log:
                        log.write('File {} copied at {} \n'.format(
                            file, time.ctime()))
        for file in replica_files:
            if file not in source_files:
                os.remove(os.path.join(replica_folder, file))
                with open(log_file, 'a') as log:
                    log.write('File {} removed at {} \n'.format(
                        file, time.ctime()))
        print('Synchronizing at {}'.format(time.ctime()))
        time.sleep(interval)


if __name__ == '__main__':
    sync(args.source_folder, args.replica_folder, args.interval, args.log_file)
