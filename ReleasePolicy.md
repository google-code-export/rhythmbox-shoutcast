# What need to do before put new release on a site #

Ensure everyting working fine, install, click all buttons. Then:

  * test release
    * click all buttons
  * update ${source}/shoutcast.rb-plugin
  * ensure everything commited
    * git status
      * commit / pull / merge
    * git tag rhythmbox-shoutcast-1.0.0
    * git push --tags
  * create documentation
    * release notes wiki page "rhythmbox\_shoutcast\_1\_0\_0"
  * create installer
    * mkdir rhythmbox-shoutcast-1.0.0
    * cp -r src rhythmbox-shoutcast-1.0.0/
    * cp ./setup.sh rhythmbox-shoutcast-1.0.0/
      * or more files, like totem-py-parser library
    * tar -czvf rhythmbox-shoutcast-1.0.0.tgz rhythmbox-shoutcast-1.0.0
    * test
      * from home folder untar ~/{path}/rhythmbox-shoutcast-1.0.0.tgz
      * run
    * upload as rhythmbox-shoutcast-1.0.0
  * notify users
    * update LastVersion wiki page
      * update last version / changelog
    * update main page