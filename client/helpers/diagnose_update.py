

def diagnose_update(files):
    ok_files = 0
    remove_files = 0
    update_files = 0
    other_files = 0
    for f in files:
        if f["status"] == "remove":
            remove_files += 1
        elif f["status"] == "update":
            update_files += 1
        elif f["status"] == "ok":
            ok_files += 1
        else:
            other_files += 1

    data = {}
    data["ok"] = ok_files
    data["remove_files"] = remove_files
    data["update_files"] = update_files
    data["other_files"] = other_files

    print(str(data))

    fl = open("debug_update.txt","w")
    fl.write(str(data))
    fl.close()