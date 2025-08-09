
def show_time(saved_time):
    saved_time[0] = "2345"

if __name__ == "__main__":
    saved_time_str = "0123"
    saved_time = [saved_time_str]
    show_time(saved_time)
    print(saved_time[0])
