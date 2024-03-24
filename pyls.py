import json
import sys
import argparse
import os
import datetime

def print_ls_format(directory,human_readable=False):
    """Recursively print directory contents in 'ls' format."""
    import pdb;pdb.set_trace()
    if human_readable:
        result = []
        for item in directory:
            if not item['name'].startswith('.'):
                perm = item['permissions']
                size = get_readable_size(item.get('size', ''))
                mtime = datetime.datetime.fromtimestamp(item.get('time_modified', 0)).strftime("%b %d %H:%M")    
                print(f"{perm} {size:>5} {mtime} {item['name']}")
    else:
        result = []
        for item in directory:
            if not item['name'].startswith('.'):
                result.append(item['name'])
        print("  ".join(result))

def print_ls_A_format(directory,human_readable=False):
    """Recursively print directory contents in 'ls' format."""
    result = []
    for item in directory:
        result.append(item['name'])
    print("  ".join(result))

def get_readable_size(size):
    suffixes = ['B', 'KB', 'MB', 'GB', 'TB']
    index = 0
    while size >= 1024 and index < len(suffixes) - 1:
        size /= 1024.0
        index += 1
    return f"{size:.1f} {suffixes[index]}"

def print_l_format(directory, indent=0, show_all=False, reverse_order=False,time_order=False,filter_option=None, human_readable=False):
    """Recursively print directory contents in 'ls' format."""
    if reverse_order:
        if time_order:
            directory.sort(key=lambda x: x.get('time_modified', 0), reverse=True)
        else:
            directory = reversed(directory)
    else:
        if time_order:
            directory.sort(key=lambda x: x.get('time_modified', 0))
        else:
            pass

    for item in directory:
        if not show_all and item['name'].startswith('.'):
            continue

        if filter_option == 'file' and 'contents' in item:
            continue
        elif filter_option == 'dir' and 'contents' not in item:
            continue

        perm = item['permissions']
        if human_readable:
            size = get_readable_size(item.get('size', ''))
        else:
            size = item.get('size', '')
        mtime = datetime.datetime.fromtimestamp(item.get('time_modified', 0)).strftime("%b %d %H:%M")    
        # Making size right aligned
        print(f"{perm} {size:>5} {mtime} {item['name']}")

def main():
    import pdb;pdb.set_trace()
    parser = argparse.ArgumentParser(description='Python implementation of ls command')
    parser.add_argument('-A', action='store_true', help='List all entries including those starting with .')
    parser.add_argument('-l', action='store_true', help='Use a long listing format')
    parser.add_argument('-r', action='store_true', help='Reverse the order of the results')
    parser.add_argument('-t', action='store_true', help='Sort by time_modified (oldest first)')
    parser.add_argument('--filter', help='Filter the output based on given option (file or dir)')
    # 'h' is already reserved for history
    parser.add_argument('-H', action='store_true', help='Show human-readable sizes')
    parser.add_argument('--path', help='Path to directory or file (default: current directory)')
    
    args = parser.parse_args()
    import pdb;pdb.set_trace()

    # Validate filter option
    valid_filters = ['file', 'dir']
    if args.filter and args.filter not in valid_filters:
        print(f"error: '{args.filter}' is not a valid filargs.pathter criteria. Available filters are {', '.join(valid_filters)}")
        sys.exit(1)


    try:
        with open('structure.json') as f:
            data = json.load(f)
    except FileNotFoundError:
        print("Error: structure.json file not found.")
        sys.exit(1)


    if args.path:
        # Find the target directory or file in the data    if args.path:

        target_item = None
        for item in data['contents']:  
            if item['name'] == args.path.split('/')[-1]:
                target_item = item
            if 'contents' in item:
                for item1 in item['contents']:
                    if item1['name'] == args.path.split('/')[-1]: 
                        target_item = item1
            if target_item:
                break

        if not target_item:
            print(f"error: cannot access '{args.path}': No such file or directory")
            sys.exit(1)

        if target_item and target_item.get('contents',None):
            if args.l:
                print_l_format(target_item['contents'], show_all=args.A, reverse_order=args.r, filter_option=args.filter,human_readable=args.H)
            elif args.t:
                print_l_format(target_item['contents'], show_all=args.A, reverse_order=args.r, filter_option=args.filter,human_readable=args.H)
            else:
                for subitem in target_item['contents']:
                    if not args.A and subitem['name'].startswith('.'):
                        continue
                    print(subitem['name'])
        else:
            perm = target_item['permissions']
            size = target_item.get('size', '')
            mtime = datetime.datetime.fromtimestamp(target_item.get('time_modified', 0)).strftime("%b %d %H:%M")    
            # Making size right aligned
            print(f"{perm} {size:>5} {mtime} {target_item['name']}")
            
    else:
        if args.l:
            print_l_format(data['contents'],show_all=args.A, reverse_order=args.r,time_order=args.t, filter_option=args.filter,human_readable=args.H)
        elif args.t:
            print_l_format(data['contents'],show_all=args.A,reverse_order=args.r,time_order=args.t, filter_option=args.filter,human_readable=args.H)
        else:
            if args.A:
                print_ls_A_format(data['contents'],human_readable=args.H)
            else:
                print_ls_format(data['contents'],human_readable=args.H)

if __name__ == "__main__":
    main()