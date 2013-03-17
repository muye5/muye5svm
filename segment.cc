// Copyright (c) 2012
// Author: Wangyanshi (muyepiaozhou@gmail.com)

#include <iostream>
#include <string>
#include <vector>
#include <dirent.h>
#include <errno.h>
#include<unistd.h>  // for access()
#include <sys/stat.h>   // for mkdir()
#include "ICTCLAS2011.h"

#ifndef OS_LINUX
#pragma comment(lib, "ICTCLAS2011.lib")
#endif

//Linux
#ifdef OS_LINUX
	#define _stricmp(X,Y) strcasecmp((X),(Y))
	#define _strnicmp(X,Y,Z) strncasecmp((X),(Y),(Z))
	#define strnicmp(X,Y,Z)	strncasecmp((X),(Y),(Z))
	#define _fstat(X,Y)     fstat((X),(Y))
	#define _fileno(X)     fileno((X))
	#define _stat           stat
	#define _getcwd         getcwd
	#define _off_t          off_t
	#define PATH_DELEMETER  "/"
#else
	#pragma warning(disable:4786)
	#define PATH_DELEMETER  "\\"
#endif

void Split(const std::string& file_name, std::string out_file)
{
	//初始化分词组件
	if(!ICTCLAS_Init("", UTF8_CODE))//数据在当前路径下，设置为UTF8编码的分词
	{
        std::cerr << "ICTCLAS INIT FAILED!" << std::endl;
		return ;
	}
	ICTCLAS_FileProcess(file_name.c_str(), out_file.c_str());
	ICTCLAS_Exit();
}


bool find_file(const std::string& target, std::vector<std::string>& files_vector) {
    std::string current("."), parent("..");
    DIR *ptr_dir;
    struct dirent *ptr_dir_ent;
    if ((ptr_dir = opendir(target.c_str())) == NULL) {
        std::cerr << "open target dir error" << std::endl;
        return false;
    }

    do {
        errno = 0;
        if((ptr_dir_ent = readdir(ptr_dir)) != NULL) {
            if (current == std::string(ptr_dir_ent->d_name) || parent == std::string(ptr_dir_ent->d_name)) {
                continue;
            }
            if (ptr_dir_ent->d_type == DT_DIR) {
                find_file(target + std::string("/") + std::string(ptr_dir_ent->d_name), files_vector);
                continue;
            }
            files_vector.push_back(target + std::string("/") + std::string(ptr_dir_ent->d_name));
        } else {
            closedir(ptr_dir);
        }
    } while (ptr_dir_ent != NULL);

    if (errno != 0) {
        std::cerr << "reading directory error" << std::endl;
        return false;
    }
    return true;
}

int main(int argc, char **argv)
{
    // argument is the file text directory , support segemnting recursively
    if (argc != 3) {
        std::cout << "Usage: ./segment.cc dir_name out_dir" << std::endl;
        return -1;
    }
    std::vector<std::string> files_vector;
    std::string dir_in(argv[1]);
    std::string dir_out(argv[2]);
    std::string out_file;

    if(!find_file(dir_in, files_vector)) {
        std::cout << "reading files faliure" << std::endl;
        return -1;
    }
    std::cout << "total " << files_vector.size() << " files" << std::endl;
    size_t pos1, pos2;
    for (std::vector<std::string>::iterator it = files_vector.begin(); it != files_vector.end(); ++it) {
        pos1 = it->find_last_of("/");
        if (pos1 == std::string::npos) {
            std::cerr << "dir name: " << *it << " Wrong" << std::endl;
            break;
        }
        pos2 = it->rfind("/", pos1 - 1);
        if (pos2 == std::string::npos) {
            std::cerr << "dir name: " << *it << " Wrong" << std::endl;
            break;
        }
        out_file = dir_out + it->substr(pos2);
        std::string tmp_dir = dir_out + std::string(it->substr(pos2, pos1 - pos2));
        if (access(tmp_dir.c_str(), R_OK) != 0) {
            if(mkdir(tmp_dir.c_str(), S_IREAD | S_IWRITE | S_IEXEC) != 0) {
                std::cerr << "mkdir " << tmp_dir << " failure" << std::endl;
                return -1;
            } else {
                std::cout << "mkdir: " << tmp_dir << "success" << std::endl;
            }
        }
        std::cout << "segemnt file: "<< *it << "\tto: " << out_file << std::endl;
        Split(*it, out_file);
    }
    return 0;
}

