#! /usr/bin/python2
import sys

class Superblock(object):
  def __init__(self, line):
    if len(line) is not 8:
      print len(line)
      print "Error in Superblock...exiting"
      exit(2)
    else:#TODO: make these global??
      self.tot_blocks = line[1]
      self.tot_inodes = line[2]
      self.block_size = line[3]
      self.inode_size = line[4]
      self.blocks_per_group = line[5]
      self.inodes_per_group = line[6]
      self.first_non_reserved_inode = line[7]
  
class Group(object):
  def __init__(self, line):
    if len(line) is not 9:
      print "Error in Group...exiting"
      exit(2)
    else:#TODO: make these global??                                                                                                                  
      self.group_num = line[1]
      self.tot_block_in_group = line[2]
      self.tot_inodes_in_group = line[3]
      self.num_free_blocks = line[4]
      self.num_free_inodes = line[5]
      self.free_block_bitmap = line[6]
      self.free_inode_bitmap = line[7]
      self.first_inode = line[8]

free_blocks = []
class Bfree(object):
  def __init__(self, line):
    if len(line) is not 2:
      print "Error in Bfree...exiting"
      exit(2)
    else: 
      free_blocks.append(line[1])

free_inodes = []
class Ifree(object):
  def __init__(self, line):
    if len(line) is not 2:
      print "Error in Ifree...exiting"
      exit(2)
    else:
      free_inodes.append(line[1])
  
inode_list = []        
class Inode(object):
  def __init__(self, line):
    if len(line) is not 27:
      print "Error in Inode...exiting"
      exit(2)
    else:
      self.inodeNum = line[1]
      self.filetype = line[2]
      self.mode = line[3]
      self.owner = line[4]
      self.group = line[5]
      self.link_count = line[6]
      self.last_change = line[7]
      self.last_mod = line[8]
      self.last_acc = line[9]
      self.file_size = line[10]
      self.num_blocks = line[11]
      self.dir1 = line[12]
      self.dir2 = line[13]
      self.dir3 = line[14]
      self.dir4 = line[15]
      self.dir5 = line[16]
      self.dir6 = line[17]
      self.dir7 = line[18]
      self.dir8 = line[19]
      self.dir9 = line[20]
      self.dir10 = line[21]
      self.dir11 = line[22]
      self.dir12 = line[23]
      self.indir1 = line[24]
      self.indir2 = line[25]
      self.indir3 = line[26]

dirent_list = []
class Dirent(object):
  def __init__(self,line):
    if len(line) is not 7:
      print "Error in Dirent...exiting"
      exit(2)
    else:
      self.parent_inode = line[1]
      self.log_byte_offset = line[2]
      self.inode_num = line[3]
      self.entry_len = line[4]
      self.name_len = line[5]
      self.name = line[6]

indirect_list = []
class Indirect(object):
  def __init__(self, line):
    if len(line) is not 6:
      print "Error in Indirect...exiting"
      exit(2)
    else:
      self.inode_num_owning = line[1]
      self.level = line[2]
      self.log_block_offset = line[3]
      self.block_num_indirect = line[4]
      self.block_num_ref = line[5]

def main():
  f = open(sys.argv[1], 'r')
  for line in f:
      #do something here
      csv = line.split(",")
      if csv[0] == "SUPERBLOCK":
        Superblock(csv)
      elif csv[0] == "GROUP":
        Group(csv)
      elif csv[0] == "BFREE":
        Bfree(csv)
      elif csv[0] == "IFREE":
        Ifree(csv)
      elif csv[0] == "INODE":
        inode_list.append(Inode(csv))
      elif csv[0] == "DIRENT":
        dirent_list.append(Dirent(csv))
      elif csv[0] == "INDIRECT":
        indirect_list.append(Indirect(csv))
      else:
        print csv[0]
        print "Found unknown csv line...exiting"
        exit(2)
  
  print len(free_blocks)
  print len(free_inodes)
  print len(inode_list)
  print len(dirent_list)
  print len(indirect_list)
  f.close()

if __name__ == '__main__':
  if len(sys.argv) < 2:
    print "Requires at least 1 argument..exiting"
    exit(1)
  main()
