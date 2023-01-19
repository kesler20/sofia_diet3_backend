import os

root_dir = __file__.split("protocol")[0]
db_path = os.path.join(root_dir, "protocol", "protocol_database", "test.txt")
max_db_size = 1_000_000

print("Max Database Size (bytes)", max_db_size)

def write_to_db(data):
    with open(db_path, "a") as db:
        db.write(str(data) + "\n")
    db_size = os.path.getsize(db_path)
    print("Current db size")
    print(db_size, "bytes")


def refresh_db():
    if os.path.getsize(db_path) > max_db_size:
        os.system(f"del {db_path}")


def read_db():
    with open(db_path) as db:
        content = db.readlines()
        content = [float(line.replace("\n", "")) for line in content]
    return content


if __name__ == "__main__":
    for _ in range(50):
        write_to_db(10)
        write_to_db(1)
        write_to_db(3)
        print(read_db())
        refresh_db()
