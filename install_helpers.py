import os
import sys
import shutil


PIVY_HEADER = """\
#ifdef __PIVY__
%%include %s
#endif

"""

def copy_and_swigify_headers(includedir, dirname, files):
        """Copy the header files to the local include directories. Add an
        #include line at the beginning for the SWIG interface files..."""

        # remove dots from dirname
        for file in files:
            if not os.path.isfile(os.path.join(dirname, file)):
                continue

            if file[-2:] == ".i":
                file = os.path.join(dirname, file)

                file_i = file.split(os.path.sep)
                file_i = [i for i in file_i if i != ".."]
                file_i = os.path.join(*file_i)

                file_h = file_i[:-2] + ".h"
                from_file = os.path.join(includedir, file_h)

                file_h = file[:-2] + ".h"
                to_file = os.path.abspath(file_h)

                if os.path.exists(from_file):
                    shutil.copyfile(from_file, to_file)
                    # sys.stdout.write('create fake header: ' + to_file + '\n')
                    fd = open(to_file, 'r+')
                    contents = fd.readlines()

                    ins_line_nr = -1
                    for line in contents:
                        ins_line_nr += 1
                        if line.find("#include ") != -1:
                            break

                    if ins_line_nr != -1:
                        contents.insert(ins_line_nr, PIVY_HEADER % (file_i))
                        fd.seek(0)
                        fd.writelines(contents)
                    else:
                        print("[failed]")
                        sys.exit(1)
                    fd.close
            # fixes for SWIG 1.3.21 and upwards
            # (mostly workarounding swig's preprocessor "function like macros"
            # preprocessor bug when no parameters are provided which then results
            # in no constructors being created in the wrapper)
            elif file[-4:] == ".fix":
                sys.stdout.write(' ' + os.path.join(dirname, file)[:-4])
                shutil.copyfile(os.path.join(dirname, file),
                                os.path.join(dirname, file)[:-4])
            # had to introduce this because windows is a piece of crap
            elif sys.platform == "win32" and file[-6:] == ".win32":
                sys.stdout.write(' ' + os.path.join(dirname, file)[:-6])
                shutil.copyfile(os.path.join(dirname, file),
                                os.path.join(dirname, file)[:-6])


def swigify(interface_dir, include_dir):
    dir_gen = os.walk(os.path.relpath(os.path.join(interface_dir, "Inventor")))
    for _dir, _, names in dir_gen:
        copy_and_swigify_headers(include_dir, _dir, names)