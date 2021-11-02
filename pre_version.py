# libversion, a version header file generator providing infos on the 
# projects git repo.
#
# Copyright (C) 2021 Julian Friedrich
# 
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
# 
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
# 
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>. 
#
# You can file issues at https://github.com/fjulian79/libversion/issues

Import('env')
import os
import time 
import subprocess

if not os.path.exists("version"):
    os.makedirs('version')

targetFileName= os.getcwd() + "/version/version.h"

projectPath = env['PROJECT_DIR']
projectName = os.path.basename(projectPath)

# until now we are in the directory of libversion, have to move to the projects home to work in it's git repo.
os.chdir(projectPath)

# having date and time definitions here causes them to be refreshed at each and very build
build_date = time.strftime("%b %d %Y")
build_time = time.strftime("%H:%M:%S")

# git config --get remote.origin.url           
ret = subprocess.run(["git", "config", "--get", "remote.origin.url"], stdout=subprocess.PIPE, text=True)
git_remote_origin_url = ret.stdout.strip()
if git_remote_origin_url:
  git_issue_url = "*\n * You can file issues at " + git_remote_origin_url.rstrip(".git") + "/issues\n "
else:  
  git_remote_origin_url="n.a."
  git_issue_url = ""

# git branch --show-current                                                   
ret = subprocess.run(["git", "branch", "--show-current"], stdout=subprocess.PIPE, text=True)
git_branch = ret.stdout.strip()
if not git_branch:
  git_branch="n.a."

# git describe --abbrev --dirty --always --tags
ret = subprocess.run(["git", "describe", "--abbrev", "--dirty", "--always", "--tags"], stdout=subprocess.PIPE, text=True)
git_version_long = ret.stdout.strip()
if not git_version_long:
  git_version_long="n.a."

# git describe --abbrev=0 --tags 
ret = subprocess.run(["git", "describe", "--abbrev=0", "--tags"], stdout=subprocess.PIPE, text=True)
git_version_short = ret.stdout.strip()
if not git_version_short:
  git_version_short=git_version_long

file = open(targetFileName, "w")

file.write("""/*
 * Auto generated version header file for project """ + projectName + """.
 *
 * Copyright (C) """ + time.strftime("%Y") + """ Julian Friedrich
 * 
 * This program is free software: you can redistribute it and/or modify
 * it under the terms of the GNU General Public License as published by
 * the Free Software Foundation, either version 3 of the License, or
 * (at your option) any later version.
 * 
 * This program is distributed in the hope that it will be useful,
 * but WITHOUT ANY WARRANTY; without even the implied warranty of
 * MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
 * GNU General Public License for more details.
 * 
 * You should have received a copy of the GNU General Public License
 * along with this program.  If not, see <https://www.gnu.org/licenses/>. 
 """ + git_issue_url + """*/
 
/****************************************************************************** 
 *********** WARNING: AUTO GENERATED FILE, DO NOT EDIT IT MANUALLY! ***********
 *****************************************************************************/

#ifndef VERSION_H_
#define VERSION_H_""")

file.write("""\n\n/**
 * @brief The date when this file has been generated
 */
#define VERSION_PROJECT                         \"""" + projectName + "\"")

file.write("""\n\n/**
 * @brief The date when this file has been generated
 */
#define VERSION_DATE                            \"""" + build_date + "\"")

file.write("""\n\n/**
 * @brief The time when this file has been generated
 */
#define VERSION_TIME                            \"""" + build_time + "\"")

file.write("""\n\n/**
 * @brief The git remote origin url defined when starting the build
 */
#define VERSION_GIT_REMOTE_ORIGIN               \"""" + git_remote_origin_url + "\"")

file.write("""\n\n/**
 * @brief The active git branch when starting the build
 */
#define VERSION_GIT_BRANCH                      \"""" + git_branch + "\"")

file.write("""\n\n/**
* @brief The latest git tag when starting the build.
*
* WARNING: Would be a empty string if there is not at least one tag on the 
*          current branch. In this case GIT_VERSION_SHORT is defined as 
*          GIT_VERSION_LONG to avoid compiler errors.
*/
#define VERSION_GIT_SHORT                       \"""" + git_version_short + "\"")

file.write("""\n\n/**
 * @brief The latest git tag including offset and short hash when starting the 
 * build.
 *
 * If this is equal to GIT_VERSION_SHORT the build is based on a clean tag 
 * without any changes.
 */
#define VERSION_GIT_LONG                        \"""" + git_version_long + "\"")

file.write("\n\n#endif /* VERSION_H_ */\n")

file.close()