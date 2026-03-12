import clang.cindex

def walk_and_collect(file, cursor, seen):
    #利用set来去重，发现重复结构体直接返回，否则加入set
    if cursor is None or cursor in seen:
        return
    seen.add(cursor)

    members = []
    struct_name = cursor.spelling
    for member in cursor.get_children():
        if member.kind == clang.cindex.CursorKind.FIELD_DECL:
            type_name = member.type.spelling
            members.append((member.spelling, type_name))
    file.write(f"static member_meta {struct_name}_metadata[] = {{\n")
    for name, type_ in members:
        file.write(f"    {{\"{name}\", offsetof({struct_name}, {name}), \"{type_}\", TD_NULL, 0}},\n")
    file.write("};\n")
    
def generate_metadata(header_file, output_file):
    idx = clang.cindex.Index.create()
    tu = idx.parse(header_file, args=['-std=c11'])
    seen = set()

    with open(output_file, 'w') as f:
        for cursor in tu.cursor.walk_preorder():
            if cursor.kind == clang.cindex.CursorKind.STRUCT_DECL:
                walk_and_collect(f, cursor, seen)
            elif cursor.kind == clang.cindex.CursorKind.ENUM_DECL:
                print("skip enum type:",cursor.spelling);

if __name__ == "__main__":
    #generate_metadata("test_header.h", "metadata.h")
    generate_metadata("venc/struct.h", "venc/metadata.h")
    generate_metadata("svac3e/struct.h", "svac3e/metadata.h")
