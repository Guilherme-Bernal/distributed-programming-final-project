import os
import re

grpc_file = 'backend_service/classes_pb2_grpc.py'

if os.path.exists(grpc_file):
    with open(grpc_file, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Only fix if not already fixed
    if 'from . import classes_pb2' not in content and 'from backend_service import classes_pb2' not in content:
        # Fix the import (only first occurrence)
        content = content.replace(
            'import classes_pb2 as classes__pb2',
            'from . import classes_pb2 as classes__pb2',
            1  # Only replace first occurrence
        )
        
        with open(grpc_file, 'w', encoding='utf-8') as f:
            f.write(content)
        
        print('✓ Fixed gRPC imports!')
    else:
        print('ℹ Imports already fixed!')
else:
    print('✗ File not found. Generate proto files first.')