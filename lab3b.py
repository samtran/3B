#! /usr/bin/python2
import sys
from sys import stderr

class Superblock(object):
  def __init__(self, line):
    if len(line) is not 8:
      print "Error in Superblock...exiting"
      exit(2)
    else:
      self.tot_blocks = int(line[1])
      self.tot_inodes = int(line[2])
      self.block_size = int(line[3])
      self.inode_size = int(line[4])
      self.blocks_per_group = int(line[5])
      self.inodes_per_group = int(line[6])
      self.first_non_reserved_inode = int(line[7])

class Group(object):
  def __init__(self, line):
    if len(line) is not 9:
      print "Error in Group...exiting"
      exit(2)
    else:
      self.group_num = int(line[1])
      self.tot_block_in_group = int(line[2])
      self.tot_inodes_in_group = int(line[3])
      self.num_free_blocks = int(line[4])
      self.num_free_inodes = int(line[5])
      self.free_block_bitmap = int(line[6])
      self.free_inode_bitmap = int(line[7])
      self.first_inode = int(line[8])

free_blocks = []
class Bfree(object):
  def __init__(self, line):
    if len(line) is not 2:
      print "Error in Bfree...exiting"
      exit(2)
    else: 
      free_blocks.append(int(line[1]))

free_inodes = []
class Ifree(object):
  def __init__(self, line):
    if len(line) is not 2:
      print "Error in Ifree...exiting"
      exit(2)
    else:
      free_inodes.append(int(line[1]))
  
inode_list = []     
inode_number_list = []   
class Inode(object):
  def __init__(self, line):
    if len(line) is not 27:
      print "Error in Inode...exiting"
      exit(2)
    else:
      self.inode_num = int(line[1])
      self.filetype = line[2]
      self.mode = line[3]
      self.owner = int(line[4])
      self.group = int(line[5])
      self.link_count = int(line[6])
      self.last_change = line[7]
      self.last_mod = line[8]
      self.last_acc = line[9]
      self.file_size = int(line[10])
      self.num_blocks = int(line[11])
      self.dir1 = int(line[12])
      self.dir2 = int(line[13])
      self.dir3 = int(line[14])
      self.dir4 = int(line[15])
      self.dir5 = int(line[16])
      self.dir6 = int(line[17])
      self.dir7 = int(line[18])
      self.dir8 = int(line[19])
      self.dir9 = int(line[20])
      self.dir10 = int(line[21])
      self.dir11 = int(line[22])
      self.dir12 = int(line[23])
      self.indir1 = int(line[24])
      self.indir2 = int(line[25])
      self.indir3 = int(line[26])

dirent_list = []
class Dirent(object):
  def __init__(self,line):
    if len(line) is not 7:
      print "Error in Dirent...exiting"
      exit(2)
    else:
      self.parent_inode = int(line[1])
      self.log_byte_offset = int(line[2])
      self.inode_num = int(line[3])
      self.entry_len = int(line[4])
      self.name_len = int(line[5])
      self.name = line[6].rstrip()

indirect_list = []
class Indirect(object):
  def __init__(self, line):
    if len(line) is not 6:
      print "Error in Indirect...exiting"
      exit(2)
    else:
      self.inode_num_owning = int(line[1])
      self.level = int(line[2])
      self.log_block_offset = int(line[3])
      self.block_num_indirect = int(line[4])
      self.block_num_ref = int(line[5])

#multiple references data structs
direct_blocks = []
single_blocks = []
double_blocks = []
tripple_blocks = []
#def block_audit():
  #check each inode_list, dirent

def inode_audit(superblock):
  #if there's only 1 group, tot_blocks could be < blocks per group 
  if(superblock.tot_blocks < superblock.blocks_per_group):
    total_inodes = superblock.inodes_per_group
  else:#TODO: this would need to be fixed for multiple groups. 
    total_inodes = (superblock.tot_blocks / superblock.blocks_per_group) * (superblock.inodes_per_group)
  #check allocated inodes
  used_inodes = []
  for inode in inode_list:
    if inode.filetype == 'f' or inode.filetype == 'd':
      #it is allocated. check to see if it is also on the free list
      used_inodes.append(inode.inode_num)
      if inode.inode_num in free_inodes:
        print "ALLOCATED INODE",inode.inode_num,"ON FREELIST"
  #check free inodes
  for inode in range(1,total_inodes):
    if inode not in used_inodes:
      #it is an unallocated inode, make sure it is on the free list
      if inode not in free_inodes:
        if inode > 10:
          print "UNALLOCATED INODE",inode,"NOT ON FREELIST"
      
def check_directory_two(superblock):
  one_dot = []
  two_dot = []
  for dir in dirent_list:
    if dir.name[1:-1] is '.':
      one_dot.append(dir.parent_inode) #TODO: should this be inode num of referenced file??
    elif dir.name[1:-1] == '..':
      two_dot.append(dir.parent_inode)
  
  for dir in dirent_list: #make sure each entry is in one dot and two dot
    if dir.parent_inode not in one_dot and dir.parent_inode not in two_dot: 
      print "DIRECTORY INODE",dir.parent_inode,"NAME '..' LINK TO INODE",dir.inode_num,"SHOULD BE",dir.parent_inode
      print "DIRECTORY INODE",dir.parent_inode,"NAME '.' LINK TO INODE",dir.inode_num,"SHOULD BE",dir.parent_inode
    elif dir.parent_inode not in one_dot:
      print "DIRECTORY INODE",dir.parent_inode,"NAME '.' LINK TO INODE",dir.inode_num,"SHOULD BE",dir.parent_inode
    elif dir.parent_inode not in two_dot:
      print "DIRECTORY INODE",dir.parent_inode,"NAME '..' LINK TO INODE",dir.inode_num,"SHOULD BE",dir.parent_inode

def check_inode_linkcount(superblock):
  #total number of inodes
  #if there's only 1 group, tot_blocks could be < blocks per group                                                                               
  if( superblock.tot_blocks < superblock.blocks_per_group):
    total_inodes = superblock.inodes_per_group
  else:#TODO: this would need to be fixed for multiple groups.
    total_inodes = (superblock.tot_blocks / superblock.blocks_per_group) * (superblock.inodes_per_group)
  inode_to_link = {}
  for dir in dirent_list:
    inode = dir.inode_num
    if inode > total_inodes:
      #invalid inode
      print "DIRECTORY INODE",inode,"NAME",dir.name,"INVALID INODE",dir.inode_num 
    if inode in inode_to_link:
      inode_to_link[inode] += 1#already in dictory so increment link counter
    else:
      inode_to_link[inode] = 1#init link counter dictionary entry
    if inode not in inode_number_list: #unallocated inode
      print "DIRECTORY INODE",inode,"NAME",dir.name,"UNALLOCATED INODE",dir.inode_num
  #check dictionary with inode link count values
  for inode in inode_list:
    if inode.inode_num in inode_to_link:
      if inode.link_count != inode_to_link[inode.inode_num]:
        print "INODE",inode.inode_num,"HAS",inode_to_link[inode.inode_num],"BUT LINKCOUNT IS",inode.link_count
    else: 
      if inode.link_count != 0:
        print "INODE",inode.inode_num,"HAS 0 BUT LINKCOUNT IS",inode.link_count
    
def main():
  f = open(sys.argv[1], 'r')
  for line in f:
      csv = line.split(",")
      if csv[0] == "SUPERBLOCK":
        superblock = Superblock(csv)
      elif csv[0] == "GROUP":
        group = Group(csv)
      elif csv[0] == "BFREE":
        Bfree(csv)
      elif csv[0] == "IFREE":
        Ifree(csv)
      elif csv[0] == "INODE":
        inode_temp = Inode(csv)
        inode_list.append(inode_temp)
        inode_number_list.append(inode_temp.inode_num)
      elif csv[0] == "DIRENT":
        dirent_list.append(Dirent(csv))
      elif csv[0] == "INDIRECT":
        indirect_list.append(Indirect(csv))
      else:
        print csv[0]
        print "Found unknown csv line...exiting"
        exit(2)
  f.close()

  #Block consistency audits
  #block_audit()
  #Inode audits
  inode_audit(superblock)
  
  #Directory Consistency audits
  check_inode_linkcount(superblock)
  check_directory_two(superblock)#check for . and ..

if __name__ == '__main__':
  if len(sys.argv) < 2:
    print "Requires at least 1 argument..exiting"
    exit(1)
  main()
