
def save_str(f, text):
    f.write(text)
    f.flush()

if __name__ == "__main__":
    file_name = "/home/pi/test.txt"
    with open(file_name,"w") as f:
        f.write("1234")
        f.flush()
    for i in range(10):
        save_str(f, str(i))
    f.close()