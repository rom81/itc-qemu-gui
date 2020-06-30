#ifndef ITC_ADDED_COMMANDS
#define ITC_ADDED_COMMANDS


MemoryMapEntryList *qmp_mtree_helper(MemoryRegion *parent, MemoryMapEntryList *mm_list);
bool itc_check_mapped(int64_t addr);

#endif