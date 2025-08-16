
def save_str(f):
    f.write("3456")
    f.flush()

if __name__ == "__main__":
    file_name = "/home/pi/test.txt"
    with open(file_name,"w") as f:
        f.write("1234")
        f.flush()
    save_str(f)