import os
import re
import argparse
from collections import defaultdict

def parse_includes(file_path):
    """Extract #include directives from a file."""
    include_pattern = re.compile(r'#include\s+["<](.*?)[">]')
    includes = set()
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            for line in f:
                match = include_pattern.match(line.strip())
                if match:
                    includes.add(match.group(1))
    except Exception as e:
        print(f"Error reading {file_path}: {e}")
    return includes

def build_dependency_graph(driver_path, include_path):
    """Build a dependency graph of file inclusions."""
    dependency_graph = defaultdict(set)
    file_map = {}
    
    # Map all headers in include directory
    for root, _, files in os.walk(include_path):
        for file in files:
            if file.endswith(".h"):
                file_map[file] = os.path.join(root, file)
    
    # Process all driver source and header files
    for root, _, files in os.walk(driver_path):
        for file in files:
            if file.endswith(('.c', '.h')):
                file_path = os.path.join(root, file)
                includes = parse_includes(file_path)
                for inc in includes:
                    if inc in file_map:
                        dependency_graph[file_path].add(file_map[inc])
    
    return dependency_graph

def is_header_included(graph, start_file, target_header, visited=None):
    """Check if target_header is included (directly or indirectly) in start_file."""
    if visited is None:
        visited = set()
    
    if start_file in visited:
        return False  # Avoid cyclic checks
    
    visited.add(start_file)
    for included_file in graph.get(start_file, set()):
        if os.path.basename(included_file) == target_header:
            return True
        if is_header_included(graph, included_file, target_header, visited):
            return True
    return False

def main():
    parser = argparse.ArgumentParser(description="Check if a header file is included in a driver file.")
    parser.add_argument("--driver", required=True, help="Path to the driver source directory")
    parser.add_argument("--include", required=True, help="Path to the include directory")
    parser.add_argument("--file", required=True, help="Driver file to check (absolute or relative path)")
    parser.add_argument("--header", required=True, help="Header file to search for (only the filename, not the full path)")
    
    args = parser.parse_args()
    graph = build_dependency_graph(args.driver, args.include)
    
    if is_header_included(graph, os.path.abspath(args.file), args.header):
        print(f"YES: {args.header} is included in {args.file}")
    else:
        print(f"NO: {args.header} is NOT included in {args.file}")

if __name__ == "__main__":
    main()
