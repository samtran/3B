#! /usr/bin/python2

class Superblock(line):
  def __init__(self):
    if len (line) is not 8:
      print "Error in Superblock...exiting"
      exit(2)
    else:#TODO: make these global??
      tot_blocks = line[1]
      tot_inodes = line[2]
      block_size = line[3]
      inode_size = line[4]
      blocks_per_group = line[5]
      inodes_per_group = line[6]
      first_non_reserved_inode = line[7]

class Group(line):
  def __init__(self):
    if len (line)is not 9:
      print "Error in Group...exiting"
      exit(2)
    else:#TODO: make these global??                                                                                                                  
      group_num = line[1]
      tot_block_in_group = line[2]
      tot_inodes_in_group = line[3]
      num_free_blocks = line[4]
      num_free_inodes = line[5]
      free_block_bitmap = line[6]
      free_inode_bitmap = line[7]
      first_inode = line[8]

class Bfree(line):
  def __init__(self):
    

def main():
  f = open(sys.argv[1], 'r')
  for line in f:
      #do something here
      csv = line.split(",")
      if csv[0] is "SUPERBLOCK":
        Superblock(line)
      elif csv[0] is "Group":
        Group(line)
      elif csv[0] is "BFREE":
        Bfree(line)
      elif csv[0] is "IFREE":
        Ifree(line)
      elif csv[0] is "INODE":
        Inode(line)
      elif csv[0] is "DIRENT":
        Dirent(line)
      elif csv[0] is "INDIRECT":
        Indirect(line)
      else:
        print "Found unknown csv line...exiting"
        exit(2)
  f.close()

if __name__ == '__main__':
  if len (sys.argv) < 2:
    print "Requires at least 1 argument..exiting"
    exit(1)
  main()
