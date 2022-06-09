from Chef import Chef


class ChineseChef(Chef):
    # overwrite
    def make_special_dish(self):
        print("The chinese chef makes bbq ribs")

    # expand
    def make_fried_rice(self):
        print("The chef makes fried rice")
